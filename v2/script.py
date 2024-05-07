import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Podaci iz prve tablice
mjerenja = {
    "Napon [V]": [5, 6, 7, 8, 9, 10],
    "Struja [A]": [1.49, 1.74, 2.00, 2.28, 2.54, 2.79],
    "Snaga [kW]": [0.007, 0.01, 0.014, 0.018, 0.023, 0.028],
    "v.t.c. tlak [bar]": [30.5, 33.7, 38.2, 43.6, 49.7, 56.1],
    "n.t.c. tlak [bar]": [11.3, 11.2, 11, 10.7, 10.7, 10.5],
    "Stv. mom. [Nm]": [12.3, 15.4, 18.8, 23.2, 28.3, 33.4],
    "Brzina vrtnje [min-1]": [306, 305, 305, 303, 301, 299],
    "Meh. snaga [kW]": [0.4, 0.48, 0.6, 0.74, 0.9, 1.04],
}

# Pretvaranje u DataFrame
df_mjerenja = pd.DataFrame(mjerenja)

df_mjerenja["Q1 [cm³]"] = 51.5

# Dodavanje kolona u DataFrame
df_mjerenja["Pad tlaka [bar]"] = df_mjerenja["v.t.c. tlak [bar]"] - df_mjerenja["n.t.c. tlak [bar]"]
df_mjerenja["Pad tlaka [Pa]"] = df_mjerenja["Pad tlaka [bar]"] * 1e5
df_mjerenja["Q_th [cm³/s]"] = df_mjerenja["Brzina vrtnje [min-1]"] / 60 * df_mjerenja["Q1 [cm³]"]
df_mjerenja["T_th [Nm]"] = df_mjerenja["Q1 [cm³]"] / 1e6 * df_mjerenja["Pad tlaka [Pa]"] / (2 * np.pi)
df_mjerenja["η_hm"] = df_mjerenja["Stv. mom. [Nm]"] / df_mjerenja["T_th [Nm]"]
df_mjerenja["Q_stv [cm³/s]"] = 16 * 1e3 / 60
df_mjerenja["Q_L [cm³/s]"] = df_mjerenja["Q_stv [cm³/s]"] - df_mjerenja["Q_th [cm³/s]"]
df_mjerenja["η_V"] = df_mjerenja["Q_th [cm³/s]"] / df_mjerenja["Q_stv [cm³/s]"]
df_mjerenja["η_t"] = df_mjerenja["η_hm"] * df_mjerenja["η_V"]
df_mjerenja["P_h [kW]"] = df_mjerenja["Q_stv [cm³/s]"] / 1e6 * df_mjerenja["Pad tlaka [Pa]"] / 1e3
df_mjerenja["P_m [kW]"] = df_mjerenja["P_h [kW]"] * df_mjerenja["η_t"]

# Prikaz tablice rezultata
df_mjerenja = df_mjerenja.round(3)
print(df_mjerenja.to_string(index=False))

# save to csv
df_mjerenja.to_csv("mjerenja.csv")

# Kreiranje dijagrama
fig, axes = plt.subplots(3, 2, figsize=(15, 10))

# Pad tlaka na hidromotoru - Brzina vrtnje hidromotora
axes[0, 0].plot(df_mjerenja["Brzina vrtnje [min-1]"], df_mjerenja["Pad tlaka [bar]"])
axes[0, 0].invert_xaxis()
axes[0, 0].set_xlabel("Brzina vrtnje [min-1]")
axes[0, 0].set_ylabel("Pad tlaka [bar]")
axes[0, 0].set_title("Pad tlaka na hidromotoru - Brzina vrtnje hidromotora")

# Stvarni moment hidromotora - Brzina vrtnje hidromotora
axes[0, 1].plot(df_mjerenja["Brzina vrtnje [min-1]"], df_mjerenja["Stv. mom. [Nm]"])
axes[0, 1].invert_xaxis()
axes[0, 1].set_xlabel("Brzina vrtnje [min-1]")
axes[0, 1].set_ylabel("Stv. mom. [Nm]")
axes[0, 1].set_title("Stvarni moment hidromotora - Brzina vrtnje hidromotora")

# Stvarni protok kroz hidromotor - Brzina vrtnje hidromotora
axes[1, 0].plot(df_mjerenja["Brzina vrtnje [min-1]"], df_mjerenja["Q_stv [cm³/s]"])
axes[1, 0].invert_xaxis()
axes[1, 0].set_xlabel("Brzina vrtnje [min-1]")
axes[1, 0].set_ylabel("Stvarni protok [cm³/s]")
axes[1, 0].set_title("Stvarni protok kroz hidromotor - Brzina vrtnje hidromotora")

# Hidraulička snaga hidromotora - Brzina vrtnje hidromotora
axes[1, 1].plot(df_mjerenja["Brzina vrtnje [min-1]"], df_mjerenja["P_h [kW]"])
axes[1, 1].invert_xaxis()
axes[1, 1].set_xlabel("Brzina vrtnje [min-1]")
axes[1, 1].set_ylabel("Hidraulička snaga [kW]")
axes[1, 1].set_title("Hidraulička snaga hidromotora - Brzina vrtnje hidromotora")

# Mehanička snaga hidromotora - Brzina vrtnje hidromotora
axes[2, 0].plot(df_mjerenja["Brzina vrtnje [min-1]"], df_mjerenja["P_m [kW]"])
axes[2, 0].invert_xaxis()
axes[2, 0].set_xlabel("Brzina vrtnje [min-1]")
axes[2, 0].set_ylabel("Meh. snaga [kW]")
axes[2, 0].set_title("Mehanička snaga hidromotora - Brzina vrtnje hidromotora")

# Stupnjevi iskoristivosti hidromotora - Brzina vrtnje hidromotora
axes[2, 1].plot(df_mjerenja["Brzina vrtnje [min-1]"], df_mjerenja["η_hm"], label="Hidromehanički stupanj")
axes[2, 1].plot(df_mjerenja["Brzina vrtnje [min-1]"], df_mjerenja["η_t"], label="Ukupni stupanj")
axes[2, 1].plot(df_mjerenja["Brzina vrtnje [min-1]"], [0.94]*len(df_mjerenja), label="Volumetrijski stupanj")
axes[2, 1].invert_xaxis()
axes[2, 1].set_xlabel("Brzina vrtnje [min-1]")
axes[2, 1].set_ylabel("Stupanj iskoristivosti")
axes[2, 1].set_title("Stupnjevi iskoristivosti hidromotora - Brzina vrtnje hidromotora")
axes[2, 1].legend()

plt.tight_layout()
plt.savefig("dijagrami.png")
