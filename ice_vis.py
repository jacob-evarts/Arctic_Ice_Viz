#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 14:07:13 2020

@author: Jacob Evarts
@email: jevarts@uoregon.edu
"""

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from sklearn import metrics
import seaborn as sns
import itertools
import datetime as dt
import matplotlib.dates as mdates
from matplotlib.offsetbox import AnchoredText
plt.style.use('ggplot')

"""--- DATA ACQUISITION ---"""
# Importing the dataset
dataset = pd.read_csv('seaice.csv')

df = dataset.copy()
df.rename(index=str, columns={"Year" : "Year", " Month" : "Month", " Day" : "Day", \
                              "     Extent" : "Extent", "    Missing" : "Missing", 
                              " Source Data" : "Source Data", "hemisphere" : "Hemisphere"}, inplace=True)
df.drop(['Source Data'], axis=1, inplace=True)


df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
df.set_index(["Date"], inplace=True)

north = df[df['Hemisphere'] == 'north']
south = df[df['Hemisphere'] == 'south']

""" Ice extent through the years """
plt.figure(figsize=(9,3))
plt.plot(north.index, north['Extent'], label="Northern Hemisphere")
plt.plot(south.index, south['Extent'], label="Southern Hemisphere")

plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.ylabel('Sea ice extent (10^6 sq km)')
plt.xlabel('Date')



# define date range to plot between
start = 1978
end = dt.datetime.now().year + 1

# define plot
f, axarr = plt.subplots(2, sharex=True, figsize=(9,6))


# organise plot axes (set x axis to months only and cycle colours according to gradient)
month_fmt = mdates.DateFormatter('%b')
axarr[0].xaxis.set_major_formatter(month_fmt)
axarr[0].set_prop_cycle(plt.cycler('color', 
                                   plt.cm.ocean(np.linspace(0, 1, len(range(start, end))))))
axarr[1].set_prop_cycle(plt.cycler('color', 
                                   plt.cm.ocean(np.linspace(0, 1, len(range(start, end))))))

# add plot legend and titles
axarr[0].set_ylabel('Sea ice extent (10^6 sq km)')
axarr[1].set_ylabel('Sea ice extent (10^6 sq km)')
axarr[1].set_xlabel('Month')
axarr[0].set_title('Annual change in sea-ice extent');
axarr[0].add_artist(AnchoredText('Northern Hemisphere', loc=3))
axarr[1].add_artist(AnchoredText('Southern Hemisphere', loc=2))

# loop for every year between the start year and current
for year in range(start, end):
    # create new dataframe for each year, 
    # and set the year to 1972 so all are plotted on the same axis
    nyeardf = north[['Extent', 'Day', 'Month']][north['Year'] == year]
    nyeardf['Year'] = 1972
    nyeardf['Date'] = pd.to_datetime(nyeardf[['Year','Month','Day']])
    nyeardf.index = nyeardf['Date'].values
    
    syeardf = south[['Extent', 'Day', 'Month']][south['Year'] == year]
    syeardf['Year'] = 1972
    syeardf['Date'] = pd.to_datetime(syeardf[['Year','Month','Day']])
    syeardf.index = syeardf['Date'].values
    
    # plot each year individually
    axarr[0].plot(nyeardf.index,nyeardf['Extent'], label = year)
    axarr[1].plot(syeardf.index,syeardf['Extent'])