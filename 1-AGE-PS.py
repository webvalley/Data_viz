#!/usr/bin/env python
# coding: utf-8

# In[2]:


#!pip install -U holoviews
#!pip install -U bokeh
#!pip install -U plotly


# In[3]:


import bokeh
#bokeh.sampledata.download()
print("done")
from bokeh.plotting import figure, output_notebook, show
output_notebook()


# In[4]:


import bokeh
bokeh.__version__


# In[5]:


import pandas as pd
import numpy as np
import holoviews as hv

from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import Slider, Button
from bokeh.sampledata import gapminder
from holoviews import dim
from holoviews import opts

from holoviews.plotting.bokeh import BokehRenderer


# In[109]:


l = ["#40fe10","#fffe10","#f25000","#ff0f00"]


# ### Gapminder test

# In[7]:


renderer = hv.renderer('bokeh')
hv.extension('plotly')
hv.extension('bokeh')


# In[85]:


df = pd.read_csv("/home/atez/Scrivania/web valley/milano_cleaned.csv")


# In[86]:


df['visit:visit'].unique()


# In[104]:


#print(df.columns.values)


# In[87]:


df_medical = df[['cod_pz','visit:visit','ana:age','lab:total_cholesterol','esa_obi:sbp','ScoreClass']]


# ### Traiettorie

# In[88]:


df_Trajectories = pd.read_csv("/home/atez/Scrivania/web valley/traj.csv", sep = ' ')


# In[89]:


df_medical.index = df_medical['cod_pz']
df_Trajectories.index = df_Trajectories['ID']


# In[90]:


df_Trajectories.head()


# In[91]:


gapminder_df = df_medical.join(df_Trajectories)


# ### Gruoped

# In[93]:


agr_1 = gapminder_df.groupby(['visit:visit','code'])[['ana:age','esa_obi:sbp','ScoreClass','lab:total_cholesterol']].median()
agr_2 = gapminder_df.groupby(['visit:visit','code'])['cod_pz'].count()


# In[94]:


df_group = agr_1.join(agr_2)


# In[96]:


df_group.reset_index(inplace=True)


# ### HV

# In[69]:


ds = hv.Dataset(df_group)


# In[70]:


# Apply dimension labels and ranges
kdims = ['ana:age', 'esa_obi:sbp']
#vdims = ['Country', 'Population', 'Group']
vdims = ['code', 'cod_pz', 'ScoreClass']

dimensions = {
    'ana:age' : dict(label='Age patient', range=(30, 100)),
    'esa_obi:sbp' : dict(label='systolic blood pressure', range=(90, 200)),
    'cod_pz': ('Numero Pazineti', 'cod_pz')
}


# In[71]:


# Create Points plotting age vs sbp indexed by visit
gapminder_ds = ds.redim(**dimensions).to(hv.Points, kdims, vdims, 'visit:visit')

# Define annotations
text = gapminder_ds.clone({yr: hv.Text(1.2, 25, str(int(yr)), fontsize=30)
                           for yr in gapminder_ds.keys()})


# In[99]:


hvgapminder = (gapminder_ds * text).opts(
    opts.Points(alpha=0.5, color='ScoreClass', cmap = l, line_color='black',
                size=np.sqrt((dim('cod_pz'))*20), width=1200, height=800,
                tools=['hover'], title='Graph of the correlation between age and blod pressure, grouped by degeneration of the disease.'),
    opts.Text(text_font_size='52pt', text_color='lightgray'))


# In[73]:


# Define custom widgets
def animate_update():
    year = slider.value + 1
    if year > end:
        year = start
    slider.value = year


# In[74]:


# Update the holoviews plot by calling update with the new year.
def slider_update(attrname, old, new):
    hvplot.update((new,))

callback_id = None

def animate():
    global callback_id
    if button.label == '► Play':
        button.label = '❚❚ Pause'
        callback_id = doc.add_periodic_callback(animate_update, 200)
    else:
        button.label = '► Play'
        doc.remove_periodic_callback(callback_id)

start = 0;
end = 3;
slider = Slider(start=start, end=end, value=start, step=1, title='Visit')
slider.on_change('value', slider_update)

button = Button(label='► Play', width=60)
button.on_click(animate)


# In[75]:


# Get HoloViews plot and attach document
doc = curdoc()
hvplot = renderer.get_plot(hvgapminder, doc)
hvplot.update((1964,))

# Make a bokeh layout and add it as the Document root
plot = layout([[hvplot.state], [slider, button]], sizing_mode='fixed')
doc.add_root(plot)


# In[ ]:





# In[ ]:





# In[ ]:




