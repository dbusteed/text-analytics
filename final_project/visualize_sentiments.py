import pandas as pd
import matplotlib.pyplot as plt
import numpy

df = pd.read_csv('chapter_sentiments.csv')

x = df.index

fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(7, 7))

i = 0
for j in range(0,3):
    for k in range(0,2):
        ver = df.columns[i]

        xlabel = f'{ver} / μ: {pd.Series.mean(df[ver]):4.2f} / σ: {pd.Series.std(df[ver]):4.2f}'

        ax[j,k].plot( df[ver] )

        z = numpy.polyfit(x, df[ver], 1)
        p = numpy.poly1d(z)
        ax[j,k].plot(x,p(x))

        ax[j,k].set_xlabel(xlabel)
        ax[j,k].set_ylabel('total sentiment')
        
        i += 1

fig.tight_layout()

plt.show()