# Actividad ETL - Análisis de Aeronaves Inscritas

## 📋 Descripción General

Este proyecto implementa un proceso **ETL (Extract, Transform, Load)** para procesar y enriquecer datos de aeronaves inscritas. El sistema extrae información de un archivo CSV, aplica transformaciones y limpiezas de datos, y genera múltiples formatos de salida: CSV enriquecido, gráficos analíticos, reportes HTML interactivos y scripts SQL.

## 🎯 Objetivo

Procesar un catálogo de aeronaves inscritas realizando:
- **Limpieza y normalización** de datos
- **Clasificación automática** de operadores
- **Unificación de marcas** de fabricantes
- **Generación de reportes visuales** y analíticos

## 📁 Estructura del Proyecto

```
actividad-etl/
├── AeronavesInscritas.csv          # Datos de entrada (fuente)
├── script.py                       # Orquestador principal del ETL
├── README.md                       # Este archivo
├── etl/                            # Módulo con funcionalidades ETL
│   ├── __init__.py
│   ├── transformations.py          # Extracción y transformación de datos
│   ├── charts.py                   # Generación de gráficos (matplotlib)
│   ├── report_html.py              # Generación de reporte HTML
│   └── sql_export.py               # Exportación a SQL
└── outputs/                        # Carpeta con todos los resultados
    ├── csv/
    │   └── aeronaves_enriquecidas.csv      # ✓ Datos transformados
    ├── graficos/
    │   ├── tipo_aeronave.png               # ✓ Gráfico: tipos de aeronaves
    │   ├── categoria_operador.png          # ✓ Gráfico: categorías operador
    │   ├── top10_marcas.png                # ✓ Gráfico: top 10 marcas
    │   └── tipo_por_categoria.png          # ✓ Gráfico: correlación tipo/categoría
    ├── html/
    │   └── reporte_aeronaves.html          # ✓ Reporte visual interactivo
    └── sql/
        └── aeronaves_enriquecidas.sql      # ✓ Script SQL (CREATE + INSERT)
```

## 🔄 Flujo ETL

### **E - EXTRACT (Extracción)**
- **Entrada**: `AeronavesInscritas.csv`
- **Función**: `extract_data()` en `transformations.py`
- Lee el archivo CSV con encoding UTF-8 y retorna un DataFrame de Pandas

### **T - TRANSFORM (Transformación)**
- **Función**: `transform_data()` en `transformations.py`
- Realiza las siguientes transformaciones:

#### 1. **Normalización de texto**
- Convierte MARCA, MODELO y NOMBRE DEL OPERADOR a MAYÚSCULAS
- Elimina espacios en blanco al inicio/final

#### 2. **Conversión de tipos de datos**
- Convierte campos `_id` y `Ndeg` a enteros (rellena NaN con 0)

#### 3. **Clasificación de Operadores**
Categoriza automáticamente según el nombre del operador:
- **CLUB AEREO**: Si contiene "CLUB" o "PLANEADORES"
- **EMPRESA**: Si contiene "SPA", "S.A.", "LTDA", "LIMITADA"
- **PERSONA NATURAL**: Si contiene comas (formato: "APELLIDO, NOMBRE")
- **OTRO**: Resto de casos

#### 4. **Unificación de Marcas**
Mapea variaciones de nombres de fabricantes:
- `BEECHCRAFT CORP.` → `BEECHCRAFT`
- `BEECH AIRCRAFT CORPORATION` → `BEECHCRAFT`
- `HAWKER BEECHCRAFT CORP.` → `BEECHCRAFT`
- `AIRBUS HELICOPTERS*` → `AIRBUS`

#### 5. **Enriquecimiento**
- Crea campo `MARCA_UNIFICADA` con nombres unificados
- Crea campo `AERONAVE_FULL` combinando marca + modelo

### **L - LOAD (Carga/Exportación)**

#### 📊 **Gráficos** (`charts.py` → `outputs/graficos/`)
Genera 4 visualizaciones usando matplotlib:

1. **tipo_aeronave.png**: Gráfico de barras - Distribución por tipo
2. **categoria_operador.png**: Gráfico de barras - Categorías de operadores
3. **top10_marcas.png**: Gráfico horizontal - Top 10 marcas mas usadas
4. **tipo_por_categoria.png**: Gráfico apilado - Correlación entrecruzada

#### 📄 **Reporte HTML** (`report_html.py` → `outputs/html/`)
Genera `reporte_aeronaves.html` con:
- **Header**: Encabezado con gradiente azul
- **KPIs**: Métricas clave en tarjetas
  - Total de registros
  - Cantidad de tipos únicos
  - Cantidad de categorías
  - Marca más frecuente
- **Sección Gráficos**: Incrustación de 4 imágenes PNG
- **Tabla de Datos**: Muestra primeras 200 filas del dataset
- **Estilos**: CSS moderno y responsive

#### 💾 **Exportación SQL** (`sql_export.py` → `outputs/sql/`)
Genera `aeronaves_enriquecidas.sql` con:

```sql
DROP TABLE IF EXISTS aeronaves_enriquecidas;
CREATE TABLE aeronaves_enriquecidas (
    "_id" INTEGER,
    "Ndeg" INTEGER,
    "MATRICULA" TEXT,
    ...
);

INSERT INTO aeronaves_enriquecidas (...) VALUES
    ('1', '1', 'CCAAA', ...),
    ...;
```

- Detección automática de tipos (INTEGER, REAL, TEXT)
- Manejo de valores NULL y escapado SQL
- Optimizado para ejecución en bases de datos

#### 📥 **Exportación CSV** (`transformations.py` → `outputs/csv/`)
Genera `aeronaves_enriquecidas.csv` con todos los campos transformados

## 🚀 Uso

### Requisitos
```bash
python >= 3.9
pandas >= 1.3.0
matplotlib >= 3.5.0
```

### Instalar dependencias
```bash
pip install pandas matplotlib
```

### Ejecutar el proceso ETL
```bash
python script.py
```

### Salida esperada
```
--- Resumen de Transformacion ---
Total registros procesados: [número]

Distribucion por tipo de operador:
EMPRESA              ###
PERSONA NATURAL      ###
...

Top 5 Marcas mas frecuentes:
CESSNA         ###
BELL           ###
...

Graficos generados:
- outputs/graficos/tipo_aeronave.png
- outputs/graficos/categoria_operador.png
- outputs/graficos/top10_marcas.png
- outputs/graficos/tipo_por_categoria.png

Reporte HTML generado: outputs/html/reporte_aeronaves.html
Archivo SQL generado: outputs/sql/aeronaves_enriquecidas.sql

Proceso ETL completado con exito.
```

## 📊 Salidas Generadas

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `aeronaves_enriquecidas.csv` | CSV | Datos completos transformados |
| `tipo_aeronave.png` | Imagen PNG | Gráfico distribución por tipo |
| `categoria_operador.png` | Imagen PNG | Gráfico distribución operadores |
| `top10_marcas.png` | Imagen PNG | Marcas más frecuentes |
| `tipo_por_categoria.png` | Imagen PNG | Análisis cruzado |
| `reporte_aeronaves.html` | HTML | Reporte interactivo con KPIs y gráficos |
| `aeronaves_enriquecidas.sql` | SQL | Script para importar a base de datos |

## 🔍 Ejemplo de Datos

### Entrada (AeronavesInscritas.csv)
```csv
_id,Ndeg,MATRICULA,USO AERONAVE,MARCA,MODELO,TIPO DE AERONAVE,NOMBRE DEL OPERADOR
1,1,CCAAA,COMERCIAL,BELL,505,HELICOPTERO,PUBLICITARIA PUBLI G SPA
2,2,CCAAB,PRIVADO,BELL,407,HELICOPTERO,TRANSPORTES COSTEROS SPA
3,3,CCAAC,PRIVADO,WERTH-RANS,S-19,AVION,"WERTH STEINERT, RENATO EDUARDO"
```

### Salida (aeronaves_enriquecidas.csv)
```csv
_id,Ndeg,MATRICULA,USO AERONAVE,MARCA,MODELO,TIPO DE AERONAVE,NOMBRE DEL OPERADOR,CATEGORIA_OPERADOR,MARCA_UNIFICADA,AERONAVE_FULL
1,1,CCAAA,COMERCIAL,BELL,505,HELICOPTERO,PUBLICITARIA PUBLI G SPA,EMPRESA,BELL,BELL 505
2,2,CCAAB,PRIVADO,BELL,407,HELICOPTERO,TRANSPORTES COSTEROS SPA,EMPRESA,BELL,BELL 407
3,3,CCAAC,PRIVADO,WERTH-RANS,S-19,AVION,WERTH STEINERT RENATO EDUARDO,PERSONA NATURAL,WERTH-RANS,WERTH-RANS S-19
```

## 📝 Módulos Principales

### `transformations.py`
```python
extract_data(csv_path)          # Lee CSV y retorna DataFrame
transform_data(df)              # Aplica todas las transformaciones
```

### `charts.py`
```python
generate_plots(df, output_dir)  # Genera 4 gráficos y retorna lista de rutas
```

### `report_html.py`
```python
generate_html_report(df, plots, output_file)  # Crea reporte HTML
```

### `sql_export.py`
```python
export_sql(df, output_file, table_name)       # Exporta a SQL script
_sql_type(series)                             # Detecta tipo SQL
_escape_sql_value(value)                      # Escapa valores SQL
```

### `script.py`
Orquestador principal que:
1. Crea estructura de carpetas output
2. Ejecuta extracción y transformación
3. Genera CSV, gráficos, reporte HTML y SQL
4. Imprime resumen de estadísticas

## 🎨 Visualizaciones Generadas

- **Gráficos de barras**: Distribución de tipos y categorías
- **Gráfico horizontal**: Top 10 fabricantes
- **Gráfico apilado**: Análisis cruzado tipo vs categoría
- **Resolución**: 150 DPI para calidad de impresión

## 📈 Consultas SQL Útiles

Una vez importado el script SQL en tu base de datos:

```sql
-- Total de aeronaves por tipo
SELECT TIPO_DE_AERONAVE, COUNT(*) FROM aeronaves_enriquecidas GROUP BY TIPO_DE_AERONAVE;

-- Distribución por categoría de operador
SELECT CATEGORIA_OPERADOR, COUNT(*) FROM aeronaves_enriquecidas GROUP BY CATEGORIA_OPERADOR;

-- Marcas más frecuentes
SELECT MARCA_UNIFICADA, COUNT(*) as cantidad FROM aeronaves_enriquecidas GROUP BY MARCA_UNIFICADA ORDER BY cantidad DESC LIMIT 10;

-- Aeronaves por operador
SELECT NOMBRE_DEL_OPERADOR, COUNT(*) FROM aeronaves_enriquecidas GROUP BY NOMBRE_DEL_OPERADOR ORDER BY COUNT(*) DESC;
```

## 🔧 Mantenimiento

El código está modularizado para facilitar:
- Agregar nuevas transformaciones en `transformations.py`
- Incluir más gráficos en `charts.py`
- Modificar estilos HTML en `report_html.py`
- Cambiar mapeo de marcas actualizando diccionario en `transformations.py`

## 📞 Notas

- El proceso es **idempotente**: ejecutar múltiples veces genera los mismos resultados
- Los archivos anteriores en `outputs/` se sobrescriben
- El encoding es UTF-8 en todas las operaciones
- El reporte HTML contiene links relativos que funcionan localmente

---