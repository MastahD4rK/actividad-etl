from datetime import datetime
import os


def generate_html_report(df, plots, output_file="reporte_aeronaves.html"):
    total_registros = len(df)
    tipos_unicos = df["TIPO DE AERONAVE"].nunique()
    operadores_unicos = df["CATEGORIA_OPERADOR"].nunique()
    marca_top = df["MARCA_UNIFICADA"].value_counts().idxmax()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_dir = os.path.dirname(os.path.abspath(output_file))
    img_tipo = os.path.relpath(os.path.abspath(plots[0]), start=html_dir).replace("\\", "/")
    img_categoria = os.path.relpath(os.path.abspath(plots[1]), start=html_dir).replace("\\", "/")
    img_marcas = os.path.relpath(os.path.abspath(plots[2]), start=html_dir).replace("\\", "/")
    img_cruce = os.path.relpath(os.path.abspath(plots[3]), start=html_dir).replace("\\", "/")

    # Generar tabla simplificada con solo 10 filas
    tabla_rows = ""
    for idx, row in df.head(10).iterrows():
        cols = "".join(f"<td>{val}</td>" for val in row)
        tabla_rows += f"<tr>{cols}</tr>"
    
    tabla_html = f"""
    <table style="width:100%; border-collapse:collapse; font-size:12px;">
      <thead><tr style="background:#f3f4f6;">
        {''.join(f"<th style='border:1px solid #e5e7eb; padding:8px; text-align:left;'>{col}</th>" for col in df.columns)}
      </tr></thead>
      <tbody>
        {tabla_rows}
      </tbody>
    </table>
    """

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Reporte ETL Aeronaves</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: Arial, sans-serif; background: #f5f5f5; color: #333; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
    .header {{ background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
    .header h1 {{ font-size: 28px; margin-bottom: 5px; }}
    .header p {{ font-size: 14px; opacity: 0.9; }}
    .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; margin-bottom: 20px; }}
    .kpi {{ background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #1d4ed8; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
    .kpi .label {{ font-size: 12px; color: #666; text-transform: uppercase; }}
    .kpi .value {{ font-size: 28px; font-weight: bold; color: #1d4ed8; margin-top: 8px; }}
    .section {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
    .section h2 {{ font-size: 20px; margin-bottom: 15px; border-bottom: 2px solid #1d4ed8; padding-bottom: 10px; }}
    .charts {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 15px; }}
    .chart-card {{ text-align: center; }}
    .chart-card h3 {{ font-size: 14px; margin-bottom: 10px; color: #555; }}
    .chart-card img {{ width: 100%; height: auto; border-radius: 6px; border: 1px solid #ddd; }}
    .data-note {{ font-size: 12px; color: #999; margin-top: 10px; font-style: italic; }}
    tbody tr:nth-child(odd) {{ background: #fafafa; }}
    tbody tr:hover {{ background: #f0f0f0; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Reporte ETL - Análisis de Aeronaves</h1>
      <p>Generado el {fecha}</p>
    </div>

    <div class="kpi-grid">
      <div class="kpi"><div class="label">Total Registros</div><div class="value">{total_registros}</div></div>
      <div class="kpi"><div class="label">Tipos Únicos</div><div class="value">{tipos_unicos}</div></div>
      <div class="kpi"><div class="label">Categorías</div><div class="value">{operadores_unicos}</div></div>
      <div class="kpi"><div class="label">Marca Top</div><div class="value">{marca_top}</div></div>
    </div>

    <div class="section">
      <h2>Visualizaciones</h2>
      <div class="charts">
        <div class="chart-card"><h3>Tipo de Aeronave</h3><img src="{img_tipo}" alt="Tipo de Aeronave"></div>
        <div class="chart-card"><h3>Categoría de Operador</h3><img src="{img_categoria}" alt="Categoría de Operador"></div>
        <div class="chart-card"><h3>Top 10 Marcas</h3><img src="{img_marcas}" alt="Top 10 Marcas"></div>
        <div class="chart-card"><h3>Tipo x Categoría</h3><img src="{img_cruce}" alt="Tipo por Categoría"></div>
      </div>
    </div>

    <div class="section">
      <h2>Muestra de Datos</h2>
      {tabla_html}
      <div class="data-note">Mostrando primeras 10 filas. Ver CSV completo para todos los registros.</div>
    </div>
  </div>
</body>
</html>"""

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html)

    return output_file
