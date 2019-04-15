# Davis Busteed -- LING 360 -- Final Project

#-------------------------------------------------------------#
#                                                             #
#   OVERVIEW -- this script creates visualizations to show    #
#               the differences in fuzzy scores in the Bible  #
#                                                             #
#-------------------------------------------------------------#

# libraries
from shared.project_settings import MISC_PATH
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# script will visualize both differences in each chapter, and 
# and the differences averaged for each book
IN_FILES = ['kjv_fuzz_scores.csv', 'kjv_fuzz_scores_by_book.csv']

# create two different groups of plots
figs = []
for c in range(2):
    figs.append( plt.subplots(nrows=3, ncols=2, figsize=(7, 7)) )

# go thru each figure
for c, fig in enumerate(figs):
    # where fig --> (fig, ax)

    # grab the CSV 
    df = pd.read_csv( os.path.join(MISC_PATH, IN_FILES[c]) )

    avgs = []
    x = df.index
    i = list(df.columns).index('ESV-KJV')

    # these loops create indicies for accessing the figure axes on the grid
    for j in range(0,3):
        for k in range(0,2):

            # for the first five plots
            if i < len(df.columns):
                ver = df.columns[i]

                # to be used on the last chart
                avgs.append( [ver, pd.Series.mean(df[ver])] )

                # plot the list of scores
                fig[1][j,k].plot( df[ver] )

                # set the labels
                fig[1][j,k].set_xlabel( f'{ver} / μ: {pd.Series.mean(df[ver]):4.2f} / σ: {pd.Series.std(df[ver]):4.2f}' )
                fig[1][j,k].set_ylabel('avg fuzzy score')
    
            # on the sixth plot, show the avg. bar chart
            else:
                
                # create some dummy x's, and get the avg values into a list
                x = np.arange(5)
                values = [a[1] for a in avgs]

                # set the values into a bar chart
                fig[1][j,k].bar( x, values )

                # the first label gets used up, so put in a 0
                labels = [a[0] for a in avgs]
                labels.insert(0, 0)

                # set the labels
                fig[1][j,k].set_xticklabels( labels )
                fig[1][j,k].set_ylabel('avg fuzzy score')

                # adjust the min and max of the bar chart
                fig[1][j,k].set_ylim([ min(values)-5 , max(values)+5 ])
            
            i += 1

    # make the figure look a little nicer
    fig[0].tight_layout()
    fig[0].suptitle(IN_FILES[c])

# show the plot!
plt.show()