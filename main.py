import requests
import pandas as pd #Uso de DataFrame
#from sodapy import Socrata #Petición HTTP
import numpy as np #Manejo de Vectores
import matplotlib.pyplot as plt #Uso de Gráficas
import ogr
import shapely
from shapely.geometry import *
import geopandas as gpd
import IPython.display as display
import gdal



urlDatos = 'https://datosabiertos.bogota.gov.co/api/3/action/datastore_search_sql?'
urlDatosSQL = 'sql=SELECT "LOCALIDAD_ASIS", count(*) as Cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "LOCALIDAD_ASIS" order by "LOCALIDAD_ASIS"'

#req = requests.get(url=urlDatos+urlDatosSQL)
#reqJson = req.json() #Organizar datos

df_bogota = gpd.read_file('data/uber/bogota_cadastral.json')
df_bogota.MOVEMENT_ID = df_bogota.MOVEMENT_ID.astype(np.int64)

