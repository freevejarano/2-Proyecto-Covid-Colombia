import requests
import pandas as pd #Uso de DataFrame
import numpy as np #Manejo de Vectores
import matplotlib.pyplot as plt #Uso de Gráficas
import ogr
import shapely
from shapely.geometry import *
import geopandas as gpd
import IPython.display as display
import gdal
import datetime
import time
from datetime import date
#Se obtiene la fecha actual para el nombre del PNG generado por cada gráfica
hoy=time.strftime("%d-%m-%y")


urlDatos = 'https://datosabiertos.bogota.gov.co/api/3/action/datastore_search_sql?'
#urlDatosSQL = 'sql=SELECT "LOCALIDAD_ASIS", count(*) as Cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "LOCALIDAD_ASIS" order by "LOCALIDAD_ASIS"'
urlDatosSQL = 'sql=SELECT "FECHA_DIAGNOSTICO", count(*) as cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "FECHA_DIAGNOSTICO" order by "FECHA_DIAGNOSTICO"'

req = requests.get(url=urlDatos+urlDatosSQL)
reqJson = req.json() #Organizar datos
#aux=reqJson['result']['records']
#print(reqJson)
ndict=reqJson['result']['records']
lis=[]
for x in ndict:
    fecha = x['FECHA_DIAGNOSTICO']
    if(isinstance(fecha,str)):
     d=datetime.datetime.strptime(fecha, "%d/%m/%Y").strftime("%Y-%m-%d")
     e=date.fromisoformat(d)
     dit={}
     dit['fecha']=e
     dit['cantidad']=int(x['cantidad'])
     lis.append(dit)

cant=[0,0,0,0,0,0,0,0]
fech=[]
meses=['Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre']
for x in lis:
    if (x['fecha'].month==3):
        cant[0]+=x['cantidad']
    elif (x['fecha'].month==4):
        cant[1]+=x['cantidad']
    elif (x['fecha'].month==5):
        cant[2]+=x['cantidad']
    elif (x['fecha'].month==6):
        cant[3]+=x['cantidad']
    elif (x['fecha'].month==7):
        cant[4]+=x['cantidad']
    elif (x['fecha'].month==8):
        cant[5]+=x['cantidad']
    elif (x['fecha'].month==9):
        cant[6]+=x['cantidad']
    elif (x['fecha'].month==10):
        cant[7]+=x['cantidad']

h=0
for x in range(len(cant)):
    print(meses[x]," ",cant[x])
    h+=cant[x]

print(h)

fig, ax = plt.subplots(figsize=(9, 7))
ax.set_ylabel('NÚMERO DE CASOS')
ax.set_title('CASOS CONFIRMADOS DE COVID-19 EN BOGOTÁ POR MESES')
plt.bar(meses, cant)
#fname="GraficoBarras_Edad_Covid_Colombia_"+hoy+".png"
#plt.savefig(fname, bbox_inches='tight')
plt.tight_layout()

plt.show()




#t = date.fromisoformat('2020-12-04')
#f= date.fromisoformat('2020-12-05')
#print(f.year)




#df_bogota = gpd.read_file('data//bogota_cadastral.json')
#df_bogota.MOVEMENT_ID = df_bogota.MOVEMENT_ID.astype(np.int64)




