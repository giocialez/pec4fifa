"""Funciones definidas a partir del enunciado de la PEC4"""
# Librerías usadas para resolver el ejercicio 1.

import os.path
import pandas as pd
import numpy as np


def read_add_year_gender(filepath: str, gender: str, year: int) -> pd.DataFrame:
    """Lee un archivo .csv y lo devuelve con dos columnas calculadas

        Parámetros:
            filepath (str): ruta en la que se encuentra el archivo .csv.
            gender (str): valor de la columna "gender" que se quiere añadir (M o F).
            year (int): valor de la columna "year" que se quiere añadir (2016-2022).

        Devuelve:
            El DataFrame leído con dos columnas (gender y year) calculadas.
    """
    dfex = pd.read_csv(filepath, low_memory=False)
    dfex['gender'] = gender
    dfex['year'] = year
    return dfex


def join_male_female(path: str, year: int) -> pd.DataFrame:
    """Lee dos archivo .csv y los devuelve concatenados con dos columnas calculadas

        Parámetros:
            path (str): ruta en la que se encuentran los archivos .csv.
            year (int): valor de la columna "year" que se quiere añadir (2016-2022),
            así como el año de los datos que queremos unir.

        Devuelve:
            Un DataFrame con los datos de todos los jugadores y jugadoras de un mismo año
            con dos columnas (gender y year) calculadas.
    """
    yeardf = str(year)
    dfm = pd.read_csv(os.path.join(path, 'players_' + yeardf[-2:] + '.csv'),
                      low_memory=False)
    # Se añade columna con el género masculino.
    dfm['gender'] = 'M'
    dff = pd.read_csv(os.path.join(path, 'female_players_' + yeardf[-2:] + '.csv'),
                      low_memory=False)
    # Se añade columna con el género femenino.
    dff['gender'] = 'F'
    # Se unen los dos DataFrame y a continuación se añade columna con año.
    dftotal = pd.concat([dfm, dff], ignore_index=True, sort=False)
    dftotal['year'] = year
    return dftotal


def join_datasets_year(path: str, years: list) -> pd.DataFrame:
    """Lee los archivos .csv de los años proporcionados mediante una lista y devuelve
    DataFrame con todos los datos de los jugadores indicando en columnas calculadas
    el género y el año de la información.

        Parámetros:
            path (str): ruta en la que se encuentran los archivos .csv.
            years (list): Lista de los años para los que se requiere la información

        Devuelve:
            Un DataFrame con los datos de todos los jugadores y jugadoras de los años
            proporcionados en una lista con dos columnas (gender y year) calculadas.
    """
    # Se realiza un for para los años de la lista aprovechando el código de las
    # funciones anteriores.
    dfs = pd.DataFrame()
    for year in years:
        yeardf = str(year)
        dfm = pd.read_csv(os.path.join(path, 'players_' + yeardf[-2:] + '.csv'),
                          low_memory=False)
        dfm['gender'] = 'M'
        dff = pd.read_csv(os.path.join(path, 'female_players_' + yeardf[-2:] + '.csv'),
                          low_memory=False)
        dff['gender'] = 'F'
        dftotal = pd.concat([dfm, dff], ignore_index=True, sort=False)
        dftotal['year'] = year
        dfs = pd.concat([dfs, dftotal], ignore_index=True, sort=False)

    return dfs


def find_max_col(dfo: pd.DataFrame, filter_col: str, cols_to_return: list) -> pd.DataFrame:
    """Con un DataFrame proporcionado devuelve un DataFrame con las columnas proporcionadas
    en una lista, según las filas que tengan el valor máximo de una columna proporcionada.

        Parámetros:
            dfo (pd.DataFrame): DataFrame a analizar.
            filter_col (str): Columna de la que se quiere mostrar aquellas filas que
            tengan el valor máximo.
            cols_to_return (list): Lista de columnas que se quieren devolver en el DataFrame.

        Devuelve:
            Un DataFrame con las filas que tengan valor máximo en filter_col, con las columnas
            proporcionadas en cols_to_return
    """
    df1 = dfo[dfo[filter_col] == dfo[filter_col].max()]
    # Se utiliza np.intersect1d para mostrar las columnas que nos interesan.
    # Visto en https://cutt.ly/VJ16Bis
    return df1[np.intersect1d(dfo.columns, cols_to_return)]


def find_rows_query(dfo: pd.DataFrame, query: tuple, cols_to_return: list) -> pd.DataFrame:
    """Con un DataFrame proporcionado devuelve un DataFrame con las columnas proporcionadas
    en una lista, según los valores de unas columnas proporcionados en una tupla.

        Parámetros:
            dfo (pd.DataFrame): DataFrame a analizar.
            query (tuple): tupla con las condiciones a filtrar, la primera lista contiene
            las columnas a filtrar y la segunda los valores.
            cols_to_return (list): Lista de columnas que se quieren devolver en el DataFrame.

            Devuelve:
            Un DataFrame con los filtros de la query y con las columnas
            proporcionadas en cols_to_return
    """
    # Se asigna el dataframe a df_final desde el que iniciaremos haciendo filtros.
    df_final = dfo
    # Se realiza un diccionario, ya que es la manera que he encontrado para poder
    # iterar sobre la tupla.
    test_keys = query[0]
    test_values = query[1]
    query_d = {test_keys[i]: test_values[i] for i in range(len(test_keys))}
    # Se itera sobre el diccionario:
    for column, value in query_d.items():
        # Se hace un if para diferenciar si la columna (que es el valor de la key) es
        # un objeto comprobar que es igual a un valor y si es un número
        # se filtra según lo que está en dos valores. (Se ha comprobado todos los tipos
        # que existen en el .csv)
        if dfo.dtypes[column] == np.object:
            df_final = df_final[df_final[column] == value]
        else:
            df_final = df_final[(df_final[column] >= value[0]) & (df_final[column] <= value[1])]

    return df_final[np.intersect1d(df_final.columns, cols_to_return)]


def calculate_bmi(dfo: pd.DataFrame, gender: str, year: int, cols_to_return: list) -> pd.DataFrame:
    """Con un DataFrame proporcionado devuelve un DataFrame con las columnas proporcionadas
    en una lista y el Indice de masa Corporal,  según el género y año proporcionado.

        Parámetros:
            dfo (pd.DataFrame): DataFrame a analizar.
            gender (str): Género a analizar.
            cols_to_return (list): Lista de columnas que se quieren devolver en el DataFrame.

            Devuelve:
            Un DataFrame el índice de masa Corporal calculado y con las columnas
            proporcionadas en cols_to_return, según el género y año proporcionado.
    """
    # Se filtra el df original según género y año proporcionado.
    dfo_bmi = dfo[(dfo['gender'] == gender) & (dfo['year'] == year)]
    # Se calcula la altura en metros.
    dfo_bmi['height_m'] = dfo_bmi['height_cm']/100
    # Cálculo del BMI
    dfo_bmi['BMI'] = dfo_bmi['weight_kg']/(dfo_bmi['height_m'])**2
    # Se añada a las columnas a solicitar el BMI.
    cols_to_return.append('BMI')
    return dfo_bmi[np.intersect1d(dfo_bmi.columns, cols_to_return)]


def players_dict(dfo: pd.DataFrame, ids: list, cols: list) -> dict:
    """Con un DataFrame proporcionado devuelve un DataFrame con las columnas proporcionadas
    en una lista y el Indice de masa Corporal,  según el género y año proporcionado.

    Parámetros:
            dfo (pd.DataFrame): DataFrame a analizar.
            ids (list): sofifa_id de los que se quiere hacer el diccionario.
            cols (list): columnas del dataframe que se quieren incluir en diccionario.

            Devuelve:
            Un diccionario que tiene como key los id y dentro de estos otro
            diccionario con key nombre de la columna y valores una lista con
            los que tieneese id.
    """
    # Se realiza un df solo con los id's solicitados.
    dfo_ids = dfo[dfo['sofifa_id'].isin(ids)]
    # Se añade sofifa_id para que lo muestre como columna.
    cols.append('sofifa_id')
    # Se realiza df con las columnas solicitadas.
    dfo_dict = dfo_ids[np.intersect1d(dfo_ids.columns, cols)]
    # Se elimina sofifa_id para que no lo use en el for.
    cols.remove('sofifa_id')
    # Se realiza diccionario iterando por ids y dentro de ids
    # por los valores de la columna, haciendo un listado
    # por lo que pueden haber valores duplicados.
    dict_p = {}
    list_id = list(set(dfo_dict['sofifa_id']))
    for id_p in list_id:
        dict_p[id_p] = {}
        for col in cols:
            dict_p[id_p][col] = list(dfo_dict[col][dfo_dict['sofifa_id'] == id_p])

    return dict_p
