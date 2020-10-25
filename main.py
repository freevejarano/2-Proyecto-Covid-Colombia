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

#URL API Datos Abiertos de Bogotá
urlDatos = 'https://datosabiertos.bogota.gov.co/api/3/action/datastore_search_sql?'

#Consulta SQL a la API
urlDatosSQL1 = 'sql=SELECT "LOCALIDAD_ASIS" as localidad, count(*) as cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "LOCALIDAD_ASIS" order by "LOCALIDAD_ASIS"'
urlDatosSQL2 = 'sql=SELECT "FECHA_DIAGNOSTICO", count(*) as cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "FECHA_DIAGNOSTICO" order by "FECHA_DIAGNOSTICO"'
urlDatosSQL3 = 'sql=SELECT "SEXO" as gen, count(*) as cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "SEXO" order by "SEXO"'



#Petición de datos, conversión de json a lista de diccionarios
req1 = requests.get(url=urlDatos+urlDatosSQL1)
reqJson1 = req1.json()
ndict1=reqJson1['result']['records']

#Organización de localidades, correción de los casos "sin dato"
localidad=[]
cantloca=[]
for x in ndict1:
    if x['localidad']!=None:
        localidad.append(x['localidad'])
        cantloca.append(int(x['cantidad']))
    else:
        aux=localidad.index('Sin dato')
        cantloca[aux]+=int(x['cantidad'])

#Gráfico de Torta Casos Por Localidad
fig1, ax1 = plt.subplots(figsize=(20,20))
plt.title("CASOS CONFIRMADOS POR LOCALIDAD DE COVID-19 EN BOGOTÁ\n", fontdict={'fontsize':15})
ax1.pie(cantloca, labels=localidad, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')
#fname="GraficoTorta_Localidad_Covid_Bogota_"+hoy+".png"
#plt.savefig(fname, bbox_inches='tight')


#Petición de datos, conversión de json a lista de diccionarios
req2 = requests.get(url=urlDatos+urlDatosSQL2)
reqJson2 = req2.json()
ndict2=reqJson2['result']['records']

#Correción formato de fecha
lis2=[]
for x in ndict2:
    fecha = x['FECHA_DIAGNOSTICO']
    if(isinstance(fecha,str)):
     d=datetime.datetime.strptime(fecha, "%d/%m/%Y").strftime("%Y-%m-%d")
     e=date.fromisoformat(d)
     dit={}
     dit['fecha']=e
     dit['cantidad']=int(x['cantidad'])
     lis2.append(dit)

#Organización casos por día en casos por mes
cant=[0,0,0,0,0,0,0,0]
fech=[]
meses=['Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre']
for x in lis2:
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

#Gráfica de Barras Casos Por Mes
fig, ax = plt.subplots(figsize=(9, 7))
ax.set_ylabel('NÚMERO DE CASOS')
ax.set_title('CASOS CONFIRMADOS DE COVID-19 EN BOGOTÁ POR MESES')
plt.bar(meses, cant)
#fname="GraficoBarras_Mes_Covid_Bogota_"+hoy+".png"
#plt.savefig(fname, bbox_inches='tight')
plt.tight_layout()


#Petición de datos, conversión de json a lista de diccionarios
req3 = requests.get(url=urlDatos+urlDatosSQL3)
reqJson3 = req3.json()
ndict3=reqJson3['result']['records']

#Organización de Datos por Género
genero=['Mujeres','Hombres']
cantgen=[int(ndict3[0]['cantidad']),int(ndict3[1]['cantidad'])]


#Gráfico de Torta Casos Por Género
fig1, ax1 = plt.subplots(figsize=(9,7))
plt.title("CASOS CONFIRMADOS POR GÉNERO DE COVID-19 EN BOGOTÁ\n", fontdict={'fontsize':15})
ax1.pie(cantgen, labels=genero, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')

#fname="GraficoTorta_Genero_Covid_Bogota_"+hoy+".png"
#plt.savefig(fname, bbox_inches='tight')

#Muestra todos los gráficos
plt.show()


