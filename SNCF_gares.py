import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./ensemble_gares.csv", encoding="ISO-8859-1")

lng_var = df[(df['lat'] > 35) & (df['lat'] < 60)]["lon"].tolist()
lat_var = df[(df['lat'] > 35) & (df['lat'] < 60)]["lat"].tolist()
plt.scatter(x=lng_var, y=lat_var, marker="o")
plt.show()
