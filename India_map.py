# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 12:13:25 2020

@author: gaama
"""
import folium
import pandas as pd
import numpy as np
import regex as re
import branca.colormap as cmp

world_geo = r'world_countries.json'
df_can=pd.read_excel('table-1.xlsx')
df_can.replace(np.nan,' ',inplace=True)
def find_str(text):
    num = re.findall("[a-zA-Z]+",text)
    return " ".join(num)

df_can['Visa requirement']=df_can['Visa requirement'].apply(lambda x: find_str(x))

#%%
in_map=folium.Map(location=(20.5937,78.9629),max_zoom=14,zoom_start=1,tiles='cartodbpositron')
notes = folium.map.FeatureGroup()


in_map.choropleth(
    geo_data=world_geo,
    data=df_can,
    columns=['Country', 'Value'],
    key_on='feature.properties.name',
    fill_color='RdYlBu', 
    nan_fill_colour='red',
    fill_opacity=0.7, 
    line_opacity=0.2,
    legend_name='Ease of access as an Indian Ordinary Passport holder'
)

for lat, lng,Notes,place,Visa,days in zip(df_can.lat,df_can.long,df_can.Notes,df_can.Country,df_can['Visa requirement'],df_can['Allowed stay']):  
    pop_text=str(place)+': '+str(Visa)
    if days!=' ':
        pop_text+=" |Days Granted: "+ str(days)
    if Notes!=' ':
        pop_text+=" |Note: "+str(Notes)
    folium.CircleMarker(
        [lat, lng],
        radius=7, # define how big you want the circle markers to be
        color='yellow',
        fill=True,
        popup=folium.Popup(pop_text, max_width=300,min_width=300),
        fill_color='blue',
        fill_opacity=0.3
    ).add_to(in_map)
in_map.save("in_map4.html")