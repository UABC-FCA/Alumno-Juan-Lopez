import pandas as pd
from mysql.connector import Error
from sqlalchemy import create_engine
from enum import Enum


class DataBD(Enum):
    USER = "root"
    PASSWORD = ""
    NAME_BD = "olimpiadas"
    SERVER = "localhost"


datos = pd.read_csv("data_olimpic.csv", index_col=0)

countries = datos.country.unique()
years = datos.year.unique()
genders = datos.gender.unique()

df_genders = pd.DataFrame(genders, columns=["nombre"])
df_genders["cat_id"] = df_genders.nombre.astype("category")
# print(df_genders)
# print(df_genders.cat_id.cat.codes)
# df_genders["id"] = df_genders.index + 1



try:
    cadena = (f"mysql+mysqlconnector://{DataBD.USER.value}:{DataBD.PASSWORD.value}"
              f"@{DataBD.SERVER.value}/{DataBD.NAME_BD.value}")
    engine = create_engine(cadena)
    conexion = engine.connect()

    print(conexion)
    print(df_genders)

    #df_genders.to_sql("Genero", conexion, if_exists= "append", index=False)
    df = pd.read_sql("Genero", conexion)
    pd.read_sql_query()
    print(df)

except Error as e:
    conexion.rollback()
    print(e)


