from shared.project_settings import MISC_PATH
import pandas as pd
import matplotlib.pyplot as plt
import numpy
import os

IN_FILE = 'chapter_sentiments.csv'

df = pd.read_csv( os.path.join(MISC_PATH, IN_FILE) )

x = df.index

fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(7, 7))

i = 5
for j in range(0,3):
    for k in range(0,2):
        ver = df.columns[i]

        xlabel = f'{ver} / μ: {pd.Series.mean(df[ver]):4.2f} / σ: {pd.Series.std(df[ver]):4.2f}'

        ax[j,k].plot( df[ver] )

        z = numpy.polyfit(x, df[ver], 1)
        p = numpy.poly1d(z)
        ax[j,k].plot(x,p(x))

        ax[j,k].set_xlabel(xlabel)
        ax[j,k].set_ylabel('avg sentiment')
        
        i += 1

fig.tight_layout()

plt.show()