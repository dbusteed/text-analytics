# Davis Busteed -- LING 360 -- HW #11

# This script uses the data created in identify_features.py
# and creates scattor plots with fitted regression lines,
# and shows the corresponding correlation value

# import modules
from identify_features import DATA_FILE, FEATS
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# read the file
df = pd.read_csv(DATA_FILE)

# create a correlation matrix
corr_df = df.corr(method='pearson')

# create a 2x2 figure for the plots 
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(10, 5))

# 'i' is used to keep track of the features
# cause the loop indicies are for plotting the figure
i = 0

# create indicies for creating the 4 plots
# (0,0), (0,1), (1,0), (1,1)
for j in range(0,2):
    for k in range(0,2):

        # assign Series of the certain feature to x
        # and the Series of stars to y, and make a scatter plot
        x = df[FEATS[i]]
        y = df['stars']
        ax[j,k].scatter( x, y )

        # give the plot a label with correlation 
        ax[j,k].set_xlabel(f'Corr of {FEATS[i]} & stars: {corr_df["stars"][FEATS[i]]:4.2f}')

        # create a regression trend line, and plot it
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax[j,k].plot(x,p(x),"r")
    
        # limit the y-axis between 0 and 6
        ax[j,k].set_ylim([0,6])

        i += 1

# this makes it look a little nicer
fig.tight_layout()

# show the chart!
plt.show()