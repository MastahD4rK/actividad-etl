import pandas as pd


def extract_data(csv_path):
    # Lee los datos desde un archivo CSV y retorna un DataFrame de pandas.
    return pd.read_csv(csv_path, sep=",", encoding="utf-8")


def transform_data(df):
    # Aplica transformaciones y limpieza de datos al DataFrame.
    df_clean = df.copy()

    # Estandarizar columnas de texto: quitar espacios y convertir a mayúsculas
    for col in ["MARCA", "MODELO", "NOMBRE DEL OPERADOR"]:
        df_clean[col] = df_clean[col].astype(str).str.strip().str.upper()

    # Llenar valores nulos con 0 y convertir a entero para las columnas numéricas
    df_clean["_id"] = df_clean["_id"].fillna(0).astype(int)
    df_clean["Ndeg"] = df_clean["Ndeg"].fillna(0).astype(int)

    def clasificar_operador(nombre):
        # Clasifica el tipo de operador basándose en palabras clave en su nombre.
        nombre = str(nombre)
        if any(word in nombre for word in ["CLUB", "PLANEADORES"]):
            return "CLUB AEREO"
        if any(word in nombre for word in ["SPA", "S.A.", "LTDA", "LIMITADA", "S.A"]):
            return "EMPRESA"
        if "," in nombre:
            return "PERSONA NATURAL"
        return "OTRO"

    # Aplicar la clasificación de operador
    df_clean["CATEGORIA_OPERADOR"] = df_clean["NOMBRE DEL OPERADOR"].apply(clasificar_operador)

    # Unificar nombres de marcas que son la misma empresa
    mapeo_marcas = {
        "BEECHCRAFT CORP.": "BEECHCRAFT",
        "BEECH AIRCRAFT CORPORATION": "BEECHCRAFT",
        "HAWKER BEECHCRAFT CORP.": "BEECHCRAFT",
        "AIRBUS HELICOPTERS": "AIRBUS",
        "AIRBUS HELICOPTERS DEUTSCHLAND GMBH": "AIRBUS",
    }
    df_clean["MARCA_UNIFICADA"] = df_clean["MARCA"].replace(mapeo_marcas)
    
    # Crear una nueva columna concatenando marca unificada y modelo
    df_clean["AERONAVE_FULL"] = df_clean["MARCA_UNIFICADA"] + " " + df_clean["MODELO"]

    return df_clean
