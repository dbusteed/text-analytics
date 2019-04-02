import pandas as pd
from identify_features import DATA_FILE, feature_1, feature_2
import matplotlib.pyplot as plt

df = pd.read_csv(DATA_FILE)

print(df.corr(method='pearson'))

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(5, 5))

ax[0].scatter( df[feature_1], df['stars'] )
ax[1].scatter( df[feature_2], df['stars'] )

fig.tight_layout()

plt.show()
