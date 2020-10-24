import urllib
import requests
import json
import pandas as pd #Uso de DataFrame
from sodapy import Socrata #Petición HTTP
import numpy as ny #Manejo de Vectores
import matplotlib.pyplot as pt #Uso de Gráficas



urlDatos = 'https://datosabiertos.bogota.gov.co/api/3/action/datastore_search_sql?'
urlDatosSQL = 'sql=SELECT "LOCALIDAD_ASIS", count(*) as Cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "LOCALIDAD_ASIS" order by "LOCALIDAD_ASIS"'

req = requests.get(url=urlDatos+urlDatosSQL)
reqJson = req.json() #Organizar datos

for x in reqJson['result']['records']:
    print(x)

