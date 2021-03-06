# -*- coding: utf-8 -*-
"""Trab_Dan_def.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KAZej0iKI_1425DK3oVS9kTVcZaLDtqt
"""

import requests
import pandas as pd
import numpy as np
import hashlib
from timeit import default_timer as timer
import json

#obtener todas las regiones existentes

url = "https://restcountries-v1.p.rapidapi.com/all"

headers = {
    'x-rapidapi-host': "restcountries-v1.p.rapidapi.com",
    'x-rapidapi-key': "f070363071msh074ba04166e2635p1337abjsnc1795de9a63a"
    }

response = requests.request("GET", url, headers=headers)
df=pd.read_json(response.text)
df = df.drop(df[df['region']==''].index)

regiones = df['region'].drop_duplicates().tolist()
#Obtener los paises 
url2 = "https://restcountries.eu/rest/v2/all"


response1 = requests.request("GET", url2, headers=headers)

df1=pd.read_json(response1.text)
#Obtener un pais por region de las regiones encontradas anteriormente 
paises_df =[]
for i in range(len(regiones)):
  paises_df.append(df1[df1['region']== regiones[i]])
  paises_df[i] = paises_df[i].set_index(np.arange(0,len(paises_df[i])))

paises=[]
for i in range(len(regiones)):
  paises.append(paises_df[i]['name'][0])

#obtener el idioma que habla el país  
idiomas=[]
for i in range(len(paises)):
  idiomas.append(paises_df[i][paises_df[i].name==paises[i]].languages[0][0].get('name'))

#encriptar el lenguaje del pais con SHA1
h=[]
lang_sha1=[]
for i in range(len(idiomas)):
  h.append(hashlib.sha1())
  h[i].update(idiomas[i].encode('utf-8'))
  lang_sha1.append(h[i].hexdigest())

#Generar el DataFrame con el tiempo que se tarda cada fila 
filas=[]
for i in range(len(regiones)):
  start = timer()
  fila = {'Region':regiones[i],'Pais':paises[i],'Idioma': lang_sha1[i]}
  end = timer()
  fila['time ($\mu$s)'] = (end-start)*1e6
  filas.append(fila)

filas=pd.DataFrame(filas)
filas

#análisis de la columna time  con pandas 
t_total = filas['time ($\\mu$s)'].sum()
t_promedio = filas['time ($\\mu$s)'].mean()
t_max =filas['time ($\\mu$s)'].max()
t_min =filas['time ($\\mu$s)'].min()

print('t_total:',t_total,'\n','t_promedio', t_promedio,
      '\n','t_max:', t_max , '\n', 't_min', t_min)

#generar archivo .jason
data = json.loads(filas.to_json())

with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)





"""# Sción nueva"""