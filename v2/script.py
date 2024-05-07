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
    "Brzina vrtnje [min⁻¹]": [306, 305, 305, 303, 301, 299],
    "Meh. snaga [kW]": [0.4, 0.48, 0.6, 0.74, 0.9, 1.04],
}

# Pretvaranje u DataFrame
df_mjerenja = pd.DataFrame(mjerenja)

df_mjerenja["Q1 [cm³]"] = 51.5

# Dodavanje kolona u DataFrame
df_mjerenja["Pad tlaka [bar]"] = df_mjerenja["v.t.c. tlak [bar]"] - df_mjerenja["n.t.c. tlak [bar]"]
df_mjerenja["Pad tlaka [Pa]"] = df_mjerenja["Pad tlaka [bar]"] * 1e5
df_mjerenja["Q_th [cm³/s]"] = df_mjerenja["Brzina vrtnje [min⁻¹]"] / 60 * df_mjerenja["Q1 [cm³]"]
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
df_mjerenja.to_csv("mjerenja.csv")

# Grafovi
fig1, ax1 = plt.subplots()
ax1.plot(df_mjerenja["Brzina vrtnje [min⁻¹]"], df_mjerenja["Pad tlaka [bar]"])
ax1.invert_xaxis()
ax1.set_xlabel("Brzina vrtnje [min⁻¹]")
ax1.set_ylabel("Pad tlaka [bar]")
ax1.set_title("Pad tlaka na hidromotoru - Brzina vrtnje hidromotora")
plt.tight_layout()
plt.savefig("pad_tlaka.png")

fig2, ax2 = plt.subplots()
ax2.plot(df_mjerenja["Brzina vrtnje [min⁻¹]"], df_mjerenja["Stv. mom. [Nm]"])
ax2.invert_xaxis()
ax2.set_xlabel("Brzina vrtnje [min⁻¹]")
ax2.set_ylabel("Stv. mom. [Nm]")
ax2.set_title("Stvarni moment hidromotora - Brzina vrtnje hidromotora")
plt.tight_layout()
plt.savefig("stvarni_moment.png")

fig3, ax3 = plt.subplots()
ax3.plot(df_mjerenja["Brzina vrtnje [min⁻¹]"], df_mjerenja["Q_stv [cm³/s]"])
ax3.invert_xaxis()
ax3.set_xlabel("Brzina vrtnje [min⁻¹]")
ax3.set_ylabel("Stvarni protok [cm³/s]")
ax3.set_title("Stvarni protok kroz hidromotor - Brzina vrtnje hidromotora")
plt.tight_layout()
plt.savefig("stvarni_protok.png")

fig4, ax4 = plt.subplots()
ax4.plot(df_mjerenja["Brzina vrtnje [min⁻¹]"], df_mjerenja["P_h [kW]"])
ax4.invert_xaxis()
ax4.set_xlabel("Brzina vrtnje [min⁻¹]")
ax4.set_ylabel("Hidraulička snaga [kW]")
ax4.set_title("Hidraulička snaga hidromotora - Brzina vrtnje hidromotora")
plt.tight_layout()
plt.savefig("hidraulicka_snaga.png")

fig5, ax5 = plt.subplots()
ax5.plot(df_mjerenja["Brzina vrtnje [min⁻¹]"], df_mjerenja["P_m [kW]"])
ax5.invert_xaxis()
ax5.set_xlabel("Brzina vrtnje [min⁻¹]")
ax5.set_ylabel("Meh. snaga [kW]")
ax5.set_title("Mehanička snaga hidromotora - Brzina vrtnje hidromotora")
plt.tight_layout()
plt.savefig("mehanicka_snaga.png")

fig6, ax6 = plt.subplots()
ax6.plot(df_mjerenja["Brzina vrtnje [min⁻¹]"], df_mjerenja["η_hm"], label="Hidromehanički stupanj")
ax6.plot(df_mjerenja["Brzina vrtnje [min⁻¹]"], df_mjerenja["η_t"], label="Ukupni stupanj")
ax6.plot(df_mjerenja["Brzina vrtnje [min⁻¹]"], df_mjerenja["η_V"], label="Volumetrijski stupanj")
ax6.invert_xaxis()
ax6.set_xlabel("Brzina vrtnje [min⁻¹]")
ax6.set_ylabel("Stupanj iskoristivosti")
ax6.set_title("Stupnjevi iskoristivosti hidromotora - Brzina vrtnje hidromotora")
ax6.legend()
plt.tight_layout()
plt.savefig("stupnjevi_iskoristivosti.png")
