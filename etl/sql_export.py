def _sql_type(series):
    # Infiere el tipo de dato SQL adecuado según el tipo de dato de pandas.
    kind = series.dtype.kind
    if kind in ("i", "u"):
        return "INTEGER"
    if kind == "f":
        return "REAL"
    return "TEXT"


def _escape_sql_value(value):
    # Escapa comillas simples y maneja valores nulos para la inserción SQL.
    if value is None:
        return "NULL"

    text = str(value)
    if text.lower() == "nan":
        return "NULL"

    return "'" + text.replace("'", "''") + "'"


def export_sql(df, output_file="aeronaves_enriquecidas.sql", table_name="aeronaves_enriquecidas"):
    # Exporta un DataFrame a un script SQL que crea la tabla y carga los datos.
    columns = df.columns.tolist()

    # Construir sentencias de creación de tabla
    create_lines = []
    for col in columns:
        sql_col_type = _sql_type(df[col])
        create_lines.append(f'    "{col}" {sql_col_type}')

    create_stmt = (
        f"DROP TABLE IF EXISTS {table_name};\n"
        f"CREATE TABLE {table_name} (\n"
        + ",\n".join(create_lines)
        + "\n);\n\n"
    )

    # Construir sentencias de inserción de datos
    insert_prefix = f"INSERT INTO {table_name} (" + ", ".join([f'"{c}"' for c in columns]) + ") VALUES\n"

    value_rows = []
    for row in df.itertuples(index=False, name=None):
        values = ", ".join(_escape_sql_value(v) for v in row)
        value_rows.append(f"({values})")

    insert_stmt = insert_prefix + ",\n".join(value_rows) + ";\n"

    # Guardar las sentencias en el archivo SQL
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(create_stmt)
        file.write(insert_stmt)

    return output_file
