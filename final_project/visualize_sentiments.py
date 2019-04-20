# Davis Busteed -- LING 360 -- Final Project

#-------------------------------------------------------------#
#                                                             #
#   OVERVIEW -- this script creates visualizations to show    #
#               the differences in sentiment scores           #
#               in the Bible                                  #
#                                                             #
#-------------------------------------------------------------#

# libraries
from shared.project_settings import MISC_PATH
import pandas as pd
import matplotlib.pyplot as plt
import numpy
import os

# make a dateframe from the CSV
IN_FILE = 'chapter_sentiments.csv'
df = pd.read_csv( os.path.join(MISC_PATH, IN_FILE) )

# Xs from 0 to whatever it may be
x = df.index

# 3x2 plot space
fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(7, 7))

# have the first column be ESV, the beginning of the sent scores
i = list(df.columns).index('ESV')

# these loops create indicies for accessing the figure axes on the grid
for j in range(0,3):
    for k in range(0,2):

        # get that versions scores
        ver = df.columns[i]

        # calc the stats
        xlabel = f'{ver} / μ: {pd.Series.mean(df[ver]):4.2f} / σ: {pd.Series.std(df[ver]):4.2f}'

        # plot the points
        ax[j,k].plot( df[ver] )

        # use the Xs from before to make a reg line
        z = numpy.polyfit(x, df[ver], 1)
        p = numpy.poly1d(z)
        ax[j,k].plot(x,p(x))

        # set the labels
        ax[j,k].set_xlabel(xlabel)
        ax[j,k].set_ylabel('avg sentiment')
        
        # increment i
        i += 1

# this just makes it look a little nicer
fig.tight_layout()

# show it!
plt.show()