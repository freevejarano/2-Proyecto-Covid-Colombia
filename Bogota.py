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
urlDatosSQL2 = 'sql=SELECT "FECHA_DIAGNOSTICO" as fecha, "LOCALIDAD_ASIS" as localidad, count(*) as cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "FECHA_DIAGNOSTICO","LOCALIDAD_ASIS" order by "FECHA_DIAGNOSTICO","LOCALIDAD_ASIS"'
urlDatosSQL3 = 'sql=SELECT "SEXO" as gen, count(*) as cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "SEXO","LOCALIDAD_ASIS" order by "SEXO","LOCALIDAD_ASIS"'
urlDatosSQL4 = 'sql=SELECT "EDAD" as edad, "LOCALIDAD_ASIS" as localidad, count(*) as cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "EDAD","LOCALIDAD_ASIS" order by "EDAD","LOCALIDAD_ASIS"'
urlDatosSQL5 = 'sql=SELECT "ESTADO" as estado, "LOCALIDAD_ASIS" as localidad, count(*) as cantidad from "b64ba3c4-9e41-41b8-b3fd-2da21d627558" group by "ESTADO","LOCALIDAD_ASIS" order by "ESTADO","LOCALIDAD_ASIS"'



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
#plt.savefig(fname, bbox_inches='tight')

#Petición de datos, conversión de json a lista de diccionarios
req5 = requests.get(url=urlDatos+urlDatosSQL5)
reqJson5 = req5.json()
ndict5=reqJson5['result']['records']

#Claisificación del estado de los casos de Covid en Bogotá
recu=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
leve=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
mode=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
grave=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
falle=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
falleNo=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for k in range(len(localidad)):
 for x in ndict5:
   if(x['localidad']==localidad[k]):
    if(x['estado']=='Recuperado'):
        recu[k]+=int(x['cantidad'])
    elif (x['estado']=='Leve'):
        leve[k]+=int(x['cantidad'])
    elif (x['estado']=='Moderado'):
        mode[k]+=int(x['cantidad'])
    elif (x['estado']=='Grave'):
        grave[k]+=int(x['cantidad'])
    elif (x['estado']=='Fallecido'):
        falle[k]+=int(x['cantidad'])
    elif (x['estado']=='Fallecido No aplica No Causa Directa'):
        falleNo[k]+=int(x['cantidad'])

x = np.arange(len(localidad))  # the label locations
width = 0.35  # the width of the bars
estado=['Recuperado','Leve','Moderado','Grave','Fallecido','Fallecido No Aplica No Causa Directa']
fig, ax = plt.subplots(figsize=(20,10))
rects1 = ax.bar(x + width*1.2, recu, width, label='Recuperado')
rects2 = ax.bar(x + width*1.8, leve, width, label='Leve')
rects3 = ax.bar(x + width*2.2, mode, width, label='Moderado')
rects4 = ax.bar(x + width*2.4, grave, width, label='Grave')
rects5 = ax.bar(x + width*2.4, falle, width, label='Fallecido')
rects6 = ax.bar(x + width*2.4, falleNo, width, label='Fallecido No Causa Directa')

ax.set_ylabel('Cantidad de Casos')
ax.set_title('Casos Por Estado En Las Localidades de Bogotá')
ax.set_xticks(x)
ax.set_xticklabels(localidad,rotation='vertical')
ax.legend()


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom')


fig.tight_layout()



#Petición de datos, conversión de json a lista de diccionarios
req2 = requests.get(url=urlDatos+urlDatosSQL2)
reqJson2 = req2.json()
ndict2=reqJson2['result']['records']

#Correción formato de fecha
lis2=[]
#Organización casos por día en casos por mes
mar=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
abr=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
may=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
jun=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
jul=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ago=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
sep=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
oct=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
nov=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for k in range(len(localidad)):
  for x in ndict2:
    if(isinstance(x['fecha'],str) and x['localidad']==localidad[k]):
     d=datetime.datetime.strptime(x['fecha'], "%d/%m/%Y").strftime("%Y-%m-%d")
     e=date.fromisoformat(d)
     if (e.month == 3):
         mar[k] += int(x['cantidad'])
     elif (e.month == 4):
         abr[k] += int(x['cantidad'])
     elif (e.month == 5):
         may[k] += int(x['cantidad'])
     elif (e.month == 6):
         jun[k] += int(x['cantidad'])
     elif (e.month == 7):
         jul[k] += int(x['cantidad'])
     elif (e.month == 8):
         ago[k] += int(x['cantidad'])
     elif (e.month == 9):
         sep[k] += int(x['cantidad'])
     elif (e.month == 10):
         oct[k] += int(x['cantidad'])
     elif (e.month == 11):
         nov[k] += int(x['cantidad'])


x = np.arange(len(localidad))  # the label locations
width = 0.35  # the width of the bars
meses=['Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre']

fig, ax = plt.subplots(figsize=(20,10))
rects1 = ax.bar(x + width*1.2, mar, width, label='Marzo')
rects2 = ax.bar(x + width*1.4, abr, width, label='Abril')
rects3 = ax.bar(x + width*1.8, may, width, label='Mayo')
rects4 = ax.bar(x + width*2.2, jun, width, label='Junio')
rects5 = ax.bar(x + width*2.4, jul, width, label='Julio')
rects6 = ax.bar(x + width*2.6, ago, width, label='Agosto')
rects7 = ax.bar(x + width*2.8, sep, width, label='Septiembre')
rects8 = ax.bar(x + width*3, oct, width, label='Octubre')
rects9 = ax.bar(x + width*3.2, nov, width, label='Noviembre')


ax.set_ylabel('Cantidad de Casos')
ax.set_title('Casos Por Meses En Las Localidades de Bogotá')
ax.set_xticks(x)
ax.set_xticklabels(localidad,rotation='vertical')
ax.legend()


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 5, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom')
fig.tight_layout()

#Petición de datos, conversión de json a lista de diccionarios
req4 = requests.get(url=urlDatos+urlDatosSQL4)
reqJson4 = req4.json()
ndict4=reqJson4['result']['records']
#Clasificación de Edades Por Segmentos
menores=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
adolescentes=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
jovenes=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
adultos=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ancianos=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for k in range(len(localidad)):
  for x in ndict4:
    if (isinstance(x['edad'], str) and (x['localidad']==localidad[k])):
        aux= int(x['edad'])
        aux2= int(x['cantidad'])
        if aux<=18:
            menores[k]+=aux2
        elif (aux>=19 and aux<=35):
            jovenes[k]+=aux2
        elif (aux>36 and aux<=59):
            adultos[k]+=aux2
        else :
            ancianos[k]+=aux2


x = np.arange(len(localidad))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(20,10))
rects1 = ax.bar(x + width*1.2, menores, width, label='Menores de Edad (0-18 años)')
rects2 = ax.bar(x + width*1.8, jovenes, width, label='Jóvenes (19-35 años)')
rects3 = ax.bar(x + width*2.2, adultos, width, label='Adultos (36-59 años)')
rects4 = ax.bar(x + width*2.4, ancianos, width, label='Ancianos (60+ años)')


ax.set_ylabel('Cantidad de Casos')
ax.set_title('Casos Por Edades En Las Localidades de Bogotá')
ax.set_xticks(x)
ax.set_xticklabels(localidad,rotation='vertical')
ax.legend()


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom')


fig.tight_layout()
plt.show()





#"""
