#!/usr/bin/env python
# coding: utf-8

# # PART2

# In[23]:


# Import librairies

import pandas as pd
import numpy as np
import wikipedia as wp
import requests
import io


# In[24]:


# enter the h1 element in wp.page(h1)
html = wp.page("List of postal codes of Canada: M").html().encode("UTF-8")

# determine the index of your table
dataf = pd.read_html(html, header = 0)[0]
dataf.head()


# In[25]:


# Ignore cells with a borough that is Not assigned

dataf = dataf[dataf.Borough != 'Not assigned']


# In[26]:


# More than one neighborhood can exist in one postal code area

dataf = dataf.groupby(['Postcode', 'Borough'])['Neighbourhood'].apply(list).apply(lambda x:', '.join(x)).to_frame().reset_index()


# In[27]:


# If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the boroughfor index
for index, row in dataf.iterrows():
    if row['Neighbourhood'] == 'Not assigned':
        row['Neighbourhood'] = row['Borough']


# In[28]:


# in order to utilize the Foursquare location data, we need to get the latitude and the longitude coordinates of each neighborhood.
url="http://cocl.us/Geospatial_data"
req =requests.get(url).content
data_r=pd.read_csv(io.StringIO(req.decode('utf-8')))

# rename the first column to allow merging dataframes on Postcode
data_r.columns = ['Postcode', 'Latitude', 'Longitude']
dataf = pd.merge(data_r, dataf, on='Postcode')

# reorder column names and show the dataframe
dataf = dataf[['Postcode', 'Borough', 'Neighbourhood', 'Latitude', 'Longitude']]
dataf.head()


# # PART3

# In[29]:


from geopy.geocoders import Nominatim 

#Use geopy library to get the latitude and longitude values of Toronto
address = 'Toronto,ON'

geolocator = Nominatim()
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of ',address,' are {}, {}.'.format(latitude, longitude))


# In[31]:


import folium # map rendering library

# create map of Toronto using latitude and longitude values
map_toronto = folium.Map(location=[latitude, longitude], zoom_start=10)

# add markers to map
for lat, lng, borough, neighbourhood in zip(dataf['Latitude'], dataf['Longitude'], dataf['Borough'], dataf['Neighbourhood']):
    label = '{}, {}'.format(neighbourhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
            
map_toronto


# In[ ]:




