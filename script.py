from etl.transformations import extract_data, transform_data
from etl.charts import generate_plots
from etl.report_html import generate_html_report
from etl.sql_export import export_sql
import os


def main():
        ruta_origen = "AeronavesInscritas.csv"

        output_base = "outputs"
        csv_dir = os.path.join(output_base, "csv")
        charts_dir = os.path.join(output_base, "graficos")
        html_dir = os.path.join(output_base, "html")
        sql_dir = os.path.join(output_base, "sql")

        for folder in [csv_dir, charts_dir, html_dir, sql_dir]:
                os.makedirs(folder, exist_ok=True)

        ruta_destino = os.path.join(csv_dir, "aeronaves_enriquecidas.csv")
        ruta_html = os.path.join(html_dir, "reporte_aeronaves.html")
        ruta_sql = os.path.join(sql_dir, "aeronaves_enriquecidas.sql")

        df_original = extract_data(ruta_origen)
        df_final = transform_data(df_original)

        df_final.to_csv(ruta_destino, index=False, encoding="utf-8")
        generated_plots = generate_plots(df_final, output_dir=charts_dir)
        html_report_path = generate_html_report(df_final, generated_plots, output_file=ruta_html)
        sql_file_path = export_sql(df_final, output_file=ruta_sql)

        print("--- Resumen de Transformacion ---")
        print(f"Total registros procesados: {len(df_final)}")
        print("\nDistribucion por tipo de operador:")
        print(df_final["CATEGORIA_OPERADOR"].value_counts())
        print("\nTop 5 Marcas mas frecuentes:")
        print(df_final["MARCA_UNIFICADA"].value_counts().head(5))

        print("\nGraficos generados:")
        for plot_path in generated_plots:
                print(f"- {plot_path}")

        print(f"\nReporte HTML generado: {html_report_path}")
        print(f"Archivo SQL generado: {sql_file_path}")
        print("\nProceso ETL completado con exito.")


if __name__ == "__main__":
        main()