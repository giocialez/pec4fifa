"""Script principal para mostrar por pantalla soluciones de PEC4"""
# Script principal.
import pandas as pd
pd.options.mode.chained_assignment = None

#pylint: disable=wrong-import-position
from funciones import (
    join_datasets_year,
    find_max_col,
    find_rows_query,
    calculate_bmi,
    players_dict
)
#pylint: disable=wrong-import-position
from graficos import (
    plot_barplot_horizontal,
    plot_barplot_vertical_2
)


if __name__ == '__main__':
    print('Inicio de PEC4')

    # EJ 2 #

    print('\nEJ2: Jugadores belgas menores de 25 años con máximo potential: ')

    # Se obtiene un dataframe de la union de todos los dataframes de la carpeta
    # data
    DFO = join_datasets_year("data", [*range(2016, 2023)])
    # Query para hombres, belgas, menores de 25 años.
    QUERYH = (["gender", "nationality_name", "age"], ["M", "Belgium", (0, 24)])
    # COlumnas a reportar.
    COLS_TO_RETURN = ["short_name", "year", "age", "overall", "potential"]
    DFOM = find_rows_query(DFO, QUERYH, COLS_TO_RETURN)
    # Se busca máximo de atributo potential en df filtrado.
    print(find_max_col(DFOM, "potential", COLS_TO_RETURN))

    print('\nEJ2: Porteras de 28 años con overall superior a 85: ')

    # Query para mujeres, porteras, mayores de 28 años.
    QUERYM = (["gender", "player_positions", "age", "overall"], ["F", "GK", (29, 100), (85, 100)])
    print(find_rows_query(DFO, QUERYM, COLS_TO_RETURN))

    # EJ 3 #

    print('\nEJ3: Gráfico BMI máximo por pais: ')
    # Se calcula BMI sobre el df calculado anteriormente y se extrae la columna
    # de las banderas.
    DFO3MAX = calculate_bmi(DFO, "M", 2022, ["club_flag_url"])
    # Finalmente, he realizado la extracción con split y strip, ya que con regex
    # no he podido y con os.path tampoco.
    DFO3MAX["club_flag_url"] = \
        DFO3MAX["club_flag_url"].str.split('/').str[-1].str.strip('/').astype(str)
    DFO3MAX["club_flag_url"] = \
        DFO3MAX["club_flag_url"].str.split('.').str[-2].str.strip('.').astype(str)
    # Se agrupa por país de equipo donde juega y se calcula el máximo BMI para ese país.
    DFO3MAX = DFO3MAX.groupby(["club_flag_url"])['BMI'].max()
    # Se grafica un gráfico de barras horizontal.
    plot_barplot_horizontal(data=DFO3MAX, x_col='BMI', y_col='club_flag_url',
                            title='BMI máximo por país')

    print('\nObservamos que los máximos se encuentran en la banda de sobrepeso,'
          '\npero hay que tener en cuenta que el BMI no distingue entre musculo'
          '\ny grasa corporal. Teniendo en cuenta que el musculo pesa más que'
          '\nla grasa, no me parece raro que haya deportistas con BMI altos.')

    print('\nEJ3: Gráfico comparación BMI hombres de 25 a 34 años en 2020: ')
    # Se calcula BMI sobre el df calculado anteriormente y se extrae la columna
    # de las banderas. Se extrae del 2020, ya que es de cuando son los datos INE.
    DFO3BMI = calculate_bmi(DFO, "M", 2020, ["age"])
    # Se filtra según edad, género se ha hecho anteriormente.
    QUERYSENIOR = (["age"], [(25, 34)])
    DFO3BMISENIOR = find_rows_query(DFO3BMI, QUERYSENIOR, ["BMI", "age"])
    # Se realizan categorías según los valores del enunciado para BMI.
    DFO3BMISENIOR['group'] = pd.to_numeric(pd.cut(DFO3BMISENIOR['BMI'],
                                                  bins=[0, 18.5, 25, 30, 100],
                                                  labels=[1, 2, 3, 4]))
    # Se agrupa según la categoría y se cuenta cuantas pertenecen a la misma.
    DFO3BMISENIORGROUP = DFO3BMISENIOR.groupby(['group'])['group'].count()
    # Se traspasa a una lista.
    LIST_GROUP = list(DFO3BMISENIORGROUP)
    # Se calcula el porcentaje.
    LIST_GROUP = [x / len(DFO3BMISENIOR) for x in LIST_GROUP]
    # Se incorporan en una lista los valores para el mismo rango de edad
    # y género masculino de la INE.
    LIST_M_SPAIN = [31.9, 1408.3, 929.5, 248]
    # Se calcula porcentaje.
    LIST_M_SPAIN = [x / sum(LIST_M_SPAIN) for x in LIST_M_SPAIN]
    # Se realiza una lista con los nombres de las categorías.
    GROUP_BMI = ['underweight', 'normal weight', 'overweight', 'obese']

    # Se grafica.
    plot_barplot_vertical_2(GROUP_BMI,
                            LIST_M_SPAIN,
                            LIST_GROUP,
                            "Distribución del BMI en hombres de 25 a 34 años en 2020")

    # EJ 4 #
    print('\nEJ4: Diccionario bruto: ')
    # Valores enunciado
    IDS = [226328, 192476, 230566]
    COLS_OF_INTEREST = ["short_name", "overall", "potential", "player_positions", "year"]
    DATA_D = join_datasets_year("data", [2016, 2017, 2018])
    # Se crea diccionario bruto
    DATA_DICT = players_dict(DATA_D, IDS, COLS_OF_INTEREST)

    print(DATA_DICT)
