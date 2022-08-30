# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 10:30:17 2022

@author: gaama
"""

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
#df_can=pd.read_excel('table-1.xlsx')
df_can=pd.read_excel('table-1.xlsx',sheet_name='Final')
df_can.replace(np.nan,' ',inplace=True)
def find_str(text):
    num = re.findall("[a-zA-Z]+",text)
    return " ".join(num)

df_can['Visa requirement']=df_can['Visa requirement'].apply(lambda x: find_str(x))

#%%
in_map=folium.Map(location=(20.5937,78.9629),max_zoom=14,zoom_start=2,tiles=None)
tile_layer=folium.TileLayer('cartodbpositron',name='Base',control=False)
tile_layer.add_to(in_map)

    
default=folium.Choropleth(
    geo_data=world_geo,
    data=df_can,
    columns=['Country', 'Default'],
    key_on='feature.properties.name',
    fill_color='RdYlBu', 
    nan_fill_colour='red',
    name='Indian Passport Only',
    fill_opacity=0.7, 
    line_opacity=0.2,
    overlay=False,
    legend_name='Ease of access as an Indian Ordinary Passport holder'
)
default.add_to(in_map)
us=folium.Choropleth(
    geo_data=world_geo,
    data=df_can,
    columns=['Country', 'US'],
    key_on='feature.properties.name',
    fill_color='RdYlBu', 
    nan_fill_colour='red',
    name='USA B1/2 visa held',
    fill_opacity=0.7, 
    line_opacity=0.2,
    overlay=False,
    show=False
)
for key in us._children:
    if key.startswith('color_map'):
        del(us._children[key])
us.add_to(in_map)
uk=folium.Choropleth(
    geo_data=world_geo,
    data=df_can,
    columns=['Country', 'UK'],
    key_on='feature.properties.name',
    fill_color='RdYlBu', 
    nan_fill_colour='red',
    name='UK Visa held',
    fill_opacity=0.7, 
    line_opacity=0.2,
    overlay=False
)
for key in uk._children:
    if key.startswith('color_map'):
        del(uk._children[key])
uk.add_to(in_map)

schengen=folium.Choropleth(
    geo_data=world_geo,
    data=df_can,
    columns=['Country', 'Schengen'],
    key_on='feature.properties.name',
    fill_color='RdYlBu', 
    nan_fill_colour='red',
    name='Schengen Visa held',
    fill_opacity=0.7, 
    line_opacity=0.2,
    overlay=False
)
for key in schengen._children:
    if key.startswith('color_map'):
        del(schengen._children[key])
schengen.add_to(in_map)

canada=folium.Choropleth(
    geo_data=world_geo,
    data=df_can,
    columns=['Country', 'Canada'],
    key_on='feature.properties.name',
    fill_color='RdYlBu', 
    nan_fill_colour='red',
    name='Canadian Visa held',
    fill_opacity=0.7, 
    line_opacity=0.2,
    overlay=False
)
for key in canada._children:
    if key.startswith('color_map'):
        del(canada._children[key])
canada.add_to(in_map)
layers=[default,us,uk,canada,schengen]
layers=[default]
for s in layers:
    for lat, lng,Notes,place,Visa,days in zip(df_can.lat,df_can.long,df_can.Notes,df_can.Country,df_can['Visa requirement'],df_can['Allowed stay']):  
        print(str(place),lat,lng)
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
        ).add_to(s)

folium.LayerControl(collapsed=False).add_to(in_map)
in_map.save("map.html")


