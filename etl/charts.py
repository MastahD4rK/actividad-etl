import os
import matplotlib.pyplot as plt
import pandas as pd


def generate_plots(df, output_dir="graficos"):
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(10, 6))
    df["TIPO DE AERONAVE"].value_counts().plot(kind="bar", color="#1f77b4")
    plt.title("Distribucion por Tipo de Aeronave")
    plt.xlabel("Tipo de Aeronave")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    path_tipo = os.path.join(output_dir, "tipo_aeronave.png")
    plt.savefig(path_tipo, dpi=150)
    plt.close()

    plt.figure(figsize=(9, 6))
    df["CATEGORIA_OPERADOR"].value_counts().plot(kind="bar", color="#2ca02c")
    plt.title("Distribucion por Categoria de Operador")
    plt.xlabel("Categoria de Operador")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    path_categoria = os.path.join(output_dir, "categoria_operador.png")
    plt.savefig(path_categoria, dpi=150)
    plt.close()

    plt.figure(figsize=(10, 6))
    df["MARCA_UNIFICADA"].value_counts().head(10).sort_values().plot(kind="barh", color="#ff7f0e")
    plt.title("Top 10 Marcas Unificadas")
    plt.xlabel("Cantidad")
    plt.ylabel("Marca")
    plt.tight_layout()
    path_marcas = os.path.join(output_dir, "top10_marcas.png")
    plt.savefig(path_marcas, dpi=150)
    plt.close()

    crosstab = pd.crosstab(df["TIPO DE AERONAVE"], df["CATEGORIA_OPERADOR"])
    ax = crosstab.plot(kind="bar", stacked=True, figsize=(10, 6), colormap="tab20")
    ax.set_title("Tipo de Aeronave por Categoria de Operador")
    ax.set_xlabel("Tipo de Aeronave")
    ax.set_ylabel("Cantidad")
    plt.xticks(rotation=20, ha="right")
    plt.legend(title="Categoria Operador", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    path_cruce = os.path.join(output_dir, "tipo_por_categoria.png")
    plt.savefig(path_cruce, dpi=150)
    plt.close()

    return [path_tipo, path_categoria, path_marcas, path_cruce]
