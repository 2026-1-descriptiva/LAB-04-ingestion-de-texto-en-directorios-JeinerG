# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""
import zipfile
import os
import pandas as pd


def extraer_archivos(origen_zip, destino_extracto):
    """
    Descomprime un archivo ZIP en la carpeta destino.
    """
    with zipfile.ZipFile(origen_zip, 'r') as manejador_zip:
        manejador_zip.extractall(destino_extracto)


def leer_texto_desde_archivo(ruta_completa):
    """
    Lee el contenido de un archivo de texto y lo retorna como string limpio.
    """
    with open(ruta_completa, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read().strip()
    return contenido


def construir_dataframe_desde_carpetas(ruta_carpeta_principal):
    """
    Recorre las subcarpetas (positivo, negativo, neutral) y construye un DataFrame.
    """
    registros = []
    categorias = ["positive", "negative", "neutral"]

    for categoria in categorias:
        directorio_categoria = os.path.join(ruta_carpeta_principal, categoria)

        for nombre_archivo in sorted(os.listdir(directorio_categoria)):
            ruta_completa = os.path.join(directorio_categoria, nombre_archivo)
            texto_frase = leer_texto_desde_archivo(ruta_completa)

            registros.append({
                "phrase": texto_frase,
                "target": categoria
            })

    return pd.DataFrame(registros)


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """
    """
    Genera los datasets de entrenamiento y prueba a partir del ZIP original.
    """
    # 1. Descomprimir el archivo
    extraer_archivos("files/input.zip", "files")

    # 2. Crear los DataFrames para train y test
    df_entrenamiento = construir_dataframe_desde_carpetas("files/input/train")
    df_prueba = construir_dataframe_desde_carpetas("files/input/test")

    # 3. Crear carpeta de salida si no existe
    os.makedirs("files/output", exist_ok=True)

    # 4. Guardar los archivos CSV
    df_entrenamiento.to_csv("files/output/train_dataset.csv", index=False)
    df_prueba.to_csv("files/output/test_dataset.csv", index=False)