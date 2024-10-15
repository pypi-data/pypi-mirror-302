import polars as pl
from .models_definition import Definition
from .enums import PropertyAggregateType
from .filter_polars_dataframe_visitor import FilterPolarsDataframeVisitor
from .models_query import LoadOptions, LoadProperty, FilterGroup
from .models_definition import DefinitionProperty


def get_date_columns(d: Definition) -> list[str]:
    """
    Liefert alle DateTime-Spalten (dessen Alias) einer Definition
    :param d: Definition 
    :return: list[str]
    """

    return [col.alias for col in d.properties if col.type == "datetime"]


def convert_to_dataframe(df: pl.DataFrame | pl.LazyFrame) -> pl.DataFrame:
    """
    Falls das übergebene DataFrame ein LazyFrame ist, dann wird dies in ein "normales" DataFrame konvertiert.
    Falls es ein "normales" DataFrame ist, dann wird dieses 1zu1 zurückgegeben.
    :param df: DataFrame oder LazyFrame
    :return: DataFrame
    """

    if isinstance(df, pl.LazyFrame):
        return df.collect()

    return df


def filter_aggregate_convert(options: LoadOptions, df: pl.DataFrame, agg_expressions: list[pl.Expr] | None = None) -> str:
    """
    Kombiniert die Funktionen filter_dataframe, aggregate_dataframe und convert_dataframe_to_result
    :param options: LoadOptions
    :param df: DataFrame
    :param agg_expressions: Angabe von zusätzlichen Aggregate-Expressions. .alias(xxx) muss angegeben werden.
    :return: DataFrame
    """

    df = filter_dataframe(options, df)
    df = aggregate_dataframe(options, df, agg_expressions=agg_expressions)
    df = final_expr_dataframe(options, df)
    return convert_dataframe_to_result(options, df)


def filter_dataframe(options: LoadOptions, df: pl.DataFrame) -> pl.DataFrame:
    """
    Filter das DataFrame auf Basis der Filter in LoadOptions
    :param options: LoadOptions
    :param df: DataFrame
    :return: DataFrame
    """

    visitor = FilterPolarsDataframeVisitor(options.definition, df)

    if options.filter:
        r = options.filter.visit(visitor)
        df = df.filter(r)

    if options.relation_filter:
        # Diese Filter stelle eine Besonderheit dar, da diese fixiert sind in:
        # Wenn es ein FilterList ist, dann wird nur nach einem Element gefilter mit mehreren Werten 
        # => somit kein Problem

        # Wenn es ein FilterGroup ist, dann besteht die Beziehung aus mehreren Eigenschaften
        # => dies könnte theoretisch über die normale Group.Or Logik laufen, allerdings stürzt Polars ab, wenn
        #    es zu viele Filter sind.
        # => daher Logik über struct. Dann kann wieder mit is_in gefiltert werden.

        # Wenn der Relation-Filter allerdings nur für eine Zeile ist, dann kommt keine Gruppe daher
        # => dann kann der Filter direkt angewendet werden

        f = options.relation_filter

        if isinstance(f, FilterGroup):
            group: FilterGroup = f

            if len(group.filters) == 1:
                f = group.filters[0]

        if isinstance(f, FilterGroup) and len(f.filters) > 0 and isinstance(f.filters[0], FilterGroup):
            group: FilterGroup = f

            prop_dict = {p.key: p.alias for p in options.definition.properties}
            rel = [{prop_dict[i.key]: i.value for i in f.filters} for f in group.filters]
            df = df.filter(pl.struct(rel[0].keys()).is_in(rel))

        else:
            df = df.filter(f.visit(visitor))

    return df


def aggregate_dataframe(options: LoadOptions, df: pl.DataFrame, agg_expressions: list[pl.Expr] | None = None) -> pl.DataFrame:
    """
    Aggregiert das DataFrame auf Basis der Properties in LoadOptions.
    Wenn min. ein LoadProperty existiert, dass eine einen aggregate_type != PropertyAggregateType.no hat
    oder ein LoadProperty existiert, dass eine agg_expr hat
    oder wenn der agg_expressions-Parameter Werte enthält,
    wird eine Gruppierung und Aggregierung vorgenommen.
    :param options: LoadOptions
    :param df: DataFrame
    :param agg_expressions: Angabe von zusätzlichen Aggregate-Expressions. .alias(xxx) muss angegeben werden.
    :return: DataFrame
    """

    if agg_expressions is None:
        agg_expressions = []

    aggregates: list[tuple[DefinitionProperty, LoadProperty]] = []
    groups: list[tuple[DefinitionProperty, LoadProperty]] = []

    for p in options.properties:
        prop = options.get_definition_property(p.key)

        if prop.agg_expr is None and prop.final_expr is not None:
            continue

        if p.aggregate_type == PropertyAggregateType.no and prop.agg_expr is None:
            groups.append((prop, p))
        else:
            aggregates.append((prop, p))

    aggregate_count = len(aggregates) + len(agg_expressions)

    if aggregate_count == 0:
        agg_list = []

        for prop, load_prop in groups:
            if prop.agg_expr is not None:
                agg_list.append(prop.agg_expr(options, load_prop, False).alias(load_prop.field_name))

        agg_list += agg_expressions

        if len(agg_list) > 0:
            df = df.with_columns(agg_list)

        return df

    if len(groups) == 0:
        agg_list = []

        for prop, load_prop in aggregates:

            if prop.agg_expr is not None:
                agg_list.append(prop.agg_expr(options, load_prop, True).alias(load_prop.field_name))
            else:
                col = convert_aggregate_type(
                    pl.col(prop.alias).alias(load_prop.field_name),
                    load_prop.aggregate_type)

                agg_list.append(col)

        df = df.select(agg_list)
    else:
        agg_list = []
        group_list = []

        for prop, load_prop in aggregates:
            if prop.agg_expr is not None:
                agg_list.append(prop.agg_expr(options, load_prop, True).alias(load_prop.field_name))
            else:
                agg_list.append(
                    convert_aggregate_type(
                        pl.col(prop.alias),
                        load_prop.aggregate_type
                    )
                    .alias(load_prop.field_name)
                )

        agg_list += agg_expressions

        for prop, load_prop in groups:
            group_list.append(pl.col(prop.alias).alias(load_prop.field_name))

        df = df.group_by(group_list).agg(agg_list)

    return df


def final_expr_dataframe(options: LoadOptions, df: pl.DataFrame) -> pl.DataFrame:
    """
    Führt die Final-Expressions lt. Definition aus
    :param options: LoadOptions
    :param df: DataFrame
    :return: DataFrame
    """

    for p in options.properties:
        prop = options.get_definition_property(p.key)

        if prop.final_expr is None:
            continue

        df = df.with_columns(prop.final_expr(options, p).alias(p.field_name))

    return df


def convert_dataframe_to_result(options: LoadOptions, df: pl.DataFrame) -> str:
    """
    Konvertiert das DataFrame in einen JSON-String, der vom ODM verarbeitet wird
    :param options: LoadOptions
    :param df: DataFrame
    :return: str
    """

    if options.max_rows:
        df = convert_to_dataframe(df).head(options.max_rows)

    column_names = df.collect_schema().names()

    cols = []
    for p in options.properties:
        if p.field_name in column_names:
            cols.append(p.field_name)
            continue

        if p.alias in column_names:
            cols.append(pl.col(p.alias).alias(p.field_name))
            continue

        raise Exception(f"Property {p.key} not found in dataframe")

    df = df.select(cols)

    return convert_to_dataframe(df).serialize(format="json")


def convert_aggregate_type(col: pl.Expr, aggregate_type: PropertyAggregateType) -> pl.Expr:
    """
    Gibt die Polars-Aggregate-Funktion für den ODM PropertyAggregateType zurück
    :param col: expr
    :param aggregate_type: PropertyAggregateType 
    :return: expr
    """

    match aggregate_type:
        case PropertyAggregateType.no:
            return col.first()
        case PropertyAggregateType.sum:
            return col.sum()
        case PropertyAggregateType.count:
            return col.count()
        case PropertyAggregateType.avg:
            return col.mean()
        case PropertyAggregateType.min:
            return col.min()
        case PropertyAggregateType.max:
            return col.max()
        case PropertyAggregateType.stdev:
            return col.std()
