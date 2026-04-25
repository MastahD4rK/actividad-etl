from datetime import datetime
import os


def generate_html_report(df, plots, output_file="reporte_aeronaves.html"):
    total_registros = len(df)
    tipos_unicos = df["TIPO DE AERONAVE"].nunique()
    operadores_unicos = df["CATEGORIA_OPERADOR"].nunique()
    marca_top = df["MARCA_UNIFICADA"].value_counts().idxmax()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    tabla_html = df.head(200).to_html(index=False, classes="data-table", border=0)

    html_dir = os.path.dirname(os.path.abspath(output_file))
    img_tipo = os.path.relpath(os.path.abspath(plots[0]), start=html_dir).replace("\\", "/")
    img_categoria = os.path.relpath(os.path.abspath(plots[1]), start=html_dir).replace("\\", "/")
    img_marcas = os.path.relpath(os.path.abspath(plots[2]), start=html_dir).replace("\\", "/")
    img_cruce = os.path.relpath(os.path.abspath(plots[3]), start=html_dir).replace("\\", "/")

    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Reporte ETL de Aeronaves</title>
  <style>
    body {{
      margin: 0;
      font-family: Segoe UI, Tahoma, sans-serif;
      background: #f6f8fb;
      color: #1f2937;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 24px;
    }}
    .header {{
      background: linear-gradient(120deg, #0f172a, #1d4ed8);
      color: #ffffff;
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 20px;
    }}
    .header h1 {{ margin: 0 0 8px 0; }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }}
    .kpi {{
      background: #ffffff;
      border: 1px solid #e5e7eb;
      border-radius: 10px;
      padding: 14px;
    }}
    .kpi .label {{ font-size: 13px; color: #6b7280; }}
    .kpi .value {{ font-size: 24px; font-weight: 700; margin-top: 6px; }}
    .section {{
      background: #ffffff;
      border: 1px solid #e5e7eb;
      border-radius: 10px;
      padding: 16px;
      margin-bottom: 16px;
    }}
    .charts {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 14px;
    }}
    .chart-card img {{
      width: 100%;
      height: auto;
      border: 1px solid #e5e7eb;
      border-radius: 8px;
      background: #fff;
    }}
    .data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      background: #ffffff;
    }}
    .data-table th, .data-table td {{
      border: 1px solid #e5e7eb;
      padding: 8px;
      text-align: left;
      vertical-align: top;
    }}
    .data-table th {{
      background: #f3f4f6;
      position: sticky;
      top: 0;
    }}
    .table-wrap {{
      max-height: 420px;
      overflow: auto;
      border: 1px solid #e5e7eb;
      border-radius: 8px;
    }}
    .foot {{
      margin-top: 10px;
      color: #6b7280;
      font-size: 12px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Reporte ETL de Aeronaves</h1>
      <p>Generado automaticamente el {fecha}</p>
    </div>

    <div class="kpi-grid">
      <div class="kpi"><div class="label">Total registros</div><div class="value">{total_registros}</div></div>
      <div class="kpi"><div class="label">Tipos de aeronave</div><div class="value">{tipos_unicos}</div></div>
      <div class="kpi"><div class="label">Categorias de operador</div><div class="value">{operadores_unicos}</div></div>
      <div class="kpi"><div class="label">Marca mas frecuente</div><div class="value">{marca_top}</div></div>
    </div>

    <div class="section">
      <h2>Graficos</h2>
      <div class="charts">
        <div class="chart-card"><h3>Tipo de Aeronave</h3><img src="{img_tipo}" alt="Tipo de Aeronave"></div>
        <div class="chart-card"><h3>Categoria de Operador</h3><img src="{img_categoria}" alt="Categoria de Operador"></div>
        <div class="chart-card"><h3>Top 10 Marcas</h3><img src="{img_marcas}" alt="Top 10 Marcas"></div>
        <div class="chart-card"><h3>Tipo por Categoria</h3><img src="{img_cruce}" alt="Tipo por Categoria"></div>
      </div>
    </div>

    <div class="section">
      <h2>Muestra de Datos (200 filas)</h2>
      <div class="table-wrap">
        {tabla_html}
      </div>
      <p class="foot">La tabla muestra solo una muestra para mantener el archivo HTML liviano.</p>
    </div>
  </div>
</body>
</html>
"""

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html)

    return output_file
