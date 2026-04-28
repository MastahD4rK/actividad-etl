from etl.transformations import extract_data, transform_data
from etl.charts import generate_plots
from etl.report_html import generate_html_report
from etl.sql_export import export_sql
import os


def main():
        # Función principal que orquesta el proceso ETL:
        # 1. Extracción (CSV)
        # 2. Transformación (Limpieza y enriquecimiento)
        # 3. Carga (Exportación a CSV, generación de gráficos, reporte HTML y SQL)
        # Definir la ruta del archivo de origen
        ruta_origen = "AeronavesInscritas.csv"

        # Definir las rutas de los directorios de salida
        output_base = "outputs"
        csv_dir = os.path.join(output_base, "csv")
        charts_dir = os.path.join(output_base, "graficos")
        html_dir = os.path.join(output_base, "html")
        sql_dir = os.path.join(output_base, "sql")

        # Crear los directorios de salida si no existen
        for folder in [csv_dir, charts_dir, html_dir, sql_dir]:
                os.makedirs(folder, exist_ok=True)

        # Definir las rutas de los archivos generados
        ruta_destino = os.path.join(csv_dir, "aeronaves_enriquecidas.csv")
        ruta_html = os.path.join(html_dir, "reporte_aeronaves.html")
        ruta_sql = os.path.join(sql_dir, "aeronaves_enriquecidas.sql")

        # Fase de Extracción y Transformación
        df_original = extract_data(ruta_origen)
        df_final = transform_data(df_original)

        # Fase de Carga (Exportar y generar reportes)
        df_final.to_csv(ruta_destino, index=False, encoding="utf-8")
        generated_plots = generate_plots(df_final, output_dir=charts_dir)
        html_report_path = generate_html_report(df_final, generated_plots, output_file=ruta_html)
        sql_file_path = export_sql(df_final, output_file=ruta_sql)

        # Imprimir resumen de la ejecución en consola
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