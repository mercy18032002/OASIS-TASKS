#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

import datetime as dt
import calendar


# In[2]:


ds=pd.read_csv('Unemployment_Rate_upto_11_2020.csv')


# In[3]:


ds.columns=["state","date","frequency","estimated unemployment rate","estimated employed","estimated labour participation rate","region", "longitude", "latitude"]


# In[4]:


ds.head()


# In[5]:


ds.shape


# In[6]:


ds.info()


# In[7]:


round(ds.describe().T)


# In[8]:


ds.isnull().sum()


# In[9]:


ds.state.value_counts()


# In[10]:


ds['date'] = pd.to_datetime(ds['date'], dayfirst=True)
ds['month_int'] =  ds['date'].dt.month
ds['month'] =  ds['month_int'].apply(lambda x: calendar.month_abbr[x])
ds.head()


# In[11]:


IND =  ds.groupby(["month"])[['estimated unemployment rate', "estimated employed", "estimated labour participation rate"]].mean()
IND = pd.DataFrame(IND).reset_index()


# In[12]:


month = IND.month
unemployment_rate = IND["estimated unemployment rate"]
labour_participation_rate = IND["estimated labour participation rate"]

fig = go.Figure()

fig.add_trace(go.Bar(x = month, y = unemployment_rate, name= "Unemployment Rate"))
fig.add_trace(go.Bar(x = month, y = labour_participation_rate, name= "Labour Participation Rate"))

fig.update_layout(title="Uneployment Rate and Labour Participation Rate",
                  xaxis={"categoryorder":"array", "categoryarray":["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]})

fig.show()


# In[13]:


fig = px.bar(IND, x='month',y='estimated employed', color='month',
             category_orders = {"month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]}, 
             title='estimated employed people from Jan 2020 to Oct 2020')

fig.show()


# In[14]:


state = ds.groupby(["state"])[["estimated unemployment rate", "estimated employed", "estimated labour participation rate"]].mean()
state = pd.DataFrame(state).reset_index()


# In[15]:


fig = px.box(ds,x='state',y='estimated unemployment rate',color='state',title='Unemployment rate')
fig.update_layout(xaxis={'categoryorder':'total descending'})
fig.show()


# In[16]:


# average unemployment rate bar plot
fig = px.bar(state, x='state', y="estimated unemployment rate", color="state", title="Average unemploment Rate (State)")
fig.update_layout(xaxis={'categoryorder':'total descending'})

fig.show()


# In[17]:


fig = px.bar(ds, x='state',y='estimated unemployment rate', animation_frame = 'month', color='state',
            title='Unemployment rate from Jan 2020 to Oct 2020 (State)')

fig.update_layout(xaxis={'categoryorder':'total descending'})

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"]=2000

fig.show()


# In[18]:


fig = px.scatter_geo(ds,'longitude', 'latitude', color="state",
                     hover_name="state", size="estimated unemployment rate",
                     animation_frame="month",scope='asia',title='Impack of lockdown on employement in India')

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000

fig.update_geos(lataxis_range=[5,40], lonaxis_range=[65, 100],oceancolor="lightblue",
    showocean=True)

fig.show()


# In[19]:


ds.region.unique()


# In[20]:


region = ds.groupby(["region"])[['estimated unemployment rate', "estimated employed", "estimated labour participation rate"]].mean()
region = pd.DataFrame(region).reset_index()


# In[21]:


# scatter plot

fig = px.scatter_matrix(ds, dimensions=['estimated unemployment rate','estimated employed','estimated labour participation rate'], color='region')
fig.show()


# In[22]:


# Average Unemployment Rate

fig = px.bar(region, x="region", y="estimated unemployment rate", color="region", title="Average Unemployment Rate (Region)")
fig.update_layout(xaxis={'categoryorder':'total descending'})
fig.show()


# In[23]:


fig = px.bar(ds, x='region',y='estimated unemployment rate', animation_frame = 'month', color='state',
            title='Unemployment rate from Jan 2020 to Oct 2020')

fig.update_layout(xaxis={'categoryorder':'total descending'})
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000

fig.show()


# In[24]:


unemployment = ds.groupby(['region','state'])['estimated unemployment rate'].mean().reset_index()

unemployment.head()


# In[25]:


fig = px.sunburst(unemployment, path=['region','state'], values='estimated unemployment rate',
                  title= 'Unemployment rate in every State and Region', height=650)
fig.show()


# In[29]:


af_lockdown = after_lockdown.groupby('state')['estimated unemployment rate'].mean().reset_index()

lockdown = before_lockdown.groupby('state')['estimated unemployment rate'].mean().reset_index()
lockdown['unemployment rate before lockdown'] = af_lockdown['estimated unemployment rate']

lockdown.columns = ['state','unemployment rate before lockdown','unemployment rate after lockdown']

before_lockdown = ds[(ds['month_int'] >= 1) & (ds['month_int'] <4)]
after_lockdown = ds[(ds['month_int'] >= 4) & (ds['month_int'] <=6)]
lockdown.head()


# In[30]:


lockdown['rate change in unemployment'] = round(lockdown['unemployment rate before lockdown'] - lockdown['unemployment rate before lockdown']
                                                /lockdown['unemployment rate after lockdown'],2)


# In[31]:


fig = px.bar(lockdown, x='state',y='rate change in unemployment',color='rate change in unemployment',
            title='Percentage change in Unemployment rate in each state after lockdown', template="ggplot2")
fig.update_layout(xaxis={'categoryorder':'total ascending'})
fig.show()


# In[ ]:




