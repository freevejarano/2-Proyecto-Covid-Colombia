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
urlDatosSQL4 = 'sql=SELECT "EDAD" as edad, count(*) as cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "EDAD" order by "EDAD"'
urlDatosSQL5 = 'sql=SELECT "ESTADO" as estado, count(*) as cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "ESTADO" order by "ESTADO"'


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
fname="GraficoTorta_Localidad_Covid_Bogota_"+hoy+".png"
plt.savefig(fname, bbox_inches='tight')


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
fname="GraficoBarras_Mes_Covid_Bogota_"+hoy+".png"
plt.savefig(fname, bbox_inches='tight')
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

fname="GraficoTorta_Genero_Covid_Bogota_"+hoy+".png"
plt.savefig(fname, bbox_inches='tight')



#Petición de datos, conversión de json a lista de diccionarios
req4 = requests.get(url=urlDatos+urlDatosSQL4)
reqJson4 = req4.json()
ndict4=reqJson4['result']['records']

#Clasificación de Edades Por Segmentos
agecant=[0,0,0,0,0]
age=['NIÑOS\n0-12\naños','ADOLESCENTES\n13-18\naños','JOVENES\n19-26\naños','ADULTOS\n26-59\naños','ANCIANOS\n60+\naños']
for x in ndict4:
    if (isinstance(x['edad'], str)):
        aux= int(x['edad'])
        aux2= int(x['cantidad'])
        if aux<12:
            agecant[0]+=aux2
        elif (aux>=12 and aux<=18):
            agecant[1]+=aux2
        elif (aux>18 and aux<=26):
            agecant[2]+=aux2
        elif (aux>26 and aux<=59):
            agecant[3] += aux2
        else :
            agecant[4]+=aux2

#Gráfica de Barras de Casos Por Edad
fig, ax = plt.subplots(figsize=(10,10))
ax.set_ylabel('Número de Casos')
ax.set_title('CASOS CONFIRMADOS DE COVID-19 EN BOGOTÁ POR EDAD')
plt.bar(age, agecant)
fname="GraficoBarras_Edad_Covid_Bogota_"+hoy+".png"
plt.savefig(fname, bbox_inches='tight')


#Petición de datos, conversión de json a lista de diccionarios
req5 = requests.get(url=urlDatos+urlDatosSQL5)
reqJson5 = req5.json()
ndict5=reqJson5['result']['records']

#Claisificación del estado de los casos de Covid en Bogotá
estado=['Recuperado','Leve','Moderado','Grave','Fallecido','Fallecido No Aplica\nNo Causa Directa']
estCant=[0,0,0,0,0,0]
for x in ndict5:
    if(x['estado']=='Recuperado'):
        estCant[0]+=int(x['cantidad'])
    elif (x['estado']=='Leve'):
        estCant[1]+=int(x['cantidad'])
    elif (x['estado']=='Moderado'):
        estCant[2]+=int(x['cantidad'])
    elif (x['estado']=='Grave'):
        estCant[3]+=int(x['cantidad'])
    elif (x['estado']=='Fallecido'):
        estCant[4]+=int(x['cantidad'])
    elif (x['estado']=='Fallecido No aplica No Causa Directa'):
        estCant[5]+=int(x['cantidad'])

#Gráfica de Barras de Casos Por Estado
fig, ax = plt.subplots(figsize=(9,7))
ax.set_ylabel('Número de Casos')
ax.set_title('ESTADO DE CASOS CONFIRMADOS DE COVID-19 EN BOGOTÁ')
plt.bar(estado, estCant)
fname="GraficoBarras_Estado_Covid_Bogota_"+hoy+".png"
plt.savefig(fname, bbox_inches='tight')


#Muestra todos los gráficos
plt.show()
