'''Fórmulas usadas para crear gráficos'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_barplot_horizontal(data: pd.DataFrame, x_col: str, y_col: str, title: str) -> None:
    """Dibuja un gráfico de barras horizontal.

    Parameters:
        data (DataFrame): Dataframe del cual se grafican datos.
        x_col (str): Nombre de la columna en eje x.
        y_col (str): Nombre de la columna en eje y.
        title (str): Título de gráfico.
    """
    axis = data.plot(kind='barh', x=x_col, y=y_col, title=title, legend=False)
    axis.set_ylabel('')
    plt.tight_layout()
    # Se muestra
    plt.show()


def plot_barplot_vertical_2(axis: list, x_col1: list, x_col2: list,
                            title: str) -> None:
    # Adaptación código visto en https://cutt.ly/HJ9h7X9
    """Dibuja un gráfico de barras vertical con dos grupos.

    Parameters:
        axis(list): Lista con las categorías observados.
        x_col1 (list): Valores del grupo Españoles.
        x_col2 (list): Valores del grupo Futbolistas.
        x_lab1 (str): Nombre etiqueta primer grupo.
        x_lab2 (str): Nombre etiqueta segundo grupo.
        title (str): Título de gráfico.
    """
    x_axis = np.arange(len(axis))

    # Multi bar Chart
    plt.bar(x_axis + 0.20, x_col1, width=0.2, label="Españoles")
    plt.bar(x_axis + 0.20 * 2, x_col2, width=0.2, label="Futbolistas")

    # Nombres grupos
    plt.xticks(x_axis, axis)

    # Se añade leyenda.
    plt.legend()

    # Se añade título:
    plt.title(title)

    # Se añade título:
    plt.ylabel('Distribución')

    # Se muestra
    plt.show()
