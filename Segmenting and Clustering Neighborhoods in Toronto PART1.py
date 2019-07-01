#!/usr/bin/env python
# coding: utf-8

# # PART 1
# 

# In[34]:


# import the librairies
import pandas as pd
import numpy as np
import lxml.html as lh
import requests


# In[35]:


# Wikipedia link
wikipedia_link = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'

# Create a handle, wikipedia_page, to handle the contents of the website
wikipedia_page = requests.get(wikipedia_link)

#Store the contents of the website under wikipedia_page
wikipedia_page = lh.fromstring(wikipedia_page.content)

#Parse data that are stored between <tr>..</tr> of HTML
tr_wiki = wikipedia_page.xpath('//tr')

#Check the length of the first 12 rows
[len(T) for T in tr_wiki[:12]]


# In[36]:


tr_wiki = wikipedia_page.xpath('//tr')

#Create empty list
col = []

i = 0
#For each row, store each first element (header) and an empty list
for t in tr_wiki[0]:
    i += 1
    name = t.text_content()
    print(name)
    col.append((name,[]))


# In[37]:


#Since out first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_wiki)):
    #T is our j'th row
    T = tr_wiki[j]
    
    #If row is not of size 3, the //tr data is not from our table 
    if len(T)!= 3:
        break
    
    #i is the index of our column
    i = 0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data = t.text_content() 
        #Check if row is empty
        if i > 0:
        #Convert any numerical value to integers
            try:
                data = int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
    
        i += 1


# In[38]:


[len(C) for (title,C) in col]


# In[39]:


# Transforming the dictionary on a dataframe
Dict = {title : column for (title,column) in col}
data = pd.DataFrame(Dict)


# In[40]:


# Cleaning 
data = data.replace(r'\n','', regex=True)
data.columns = ['Postcode', 'Borough', 'Neighbourhood']
data.head()


# In[41]:


# Removing Not assigned and fixing data index
data.drop(data[data['Borough'] == 'Not assigned'].index, inplace=True)
data.index = range(len(data))
data.head()


# In[42]:


data.shape


# In[ ]:




