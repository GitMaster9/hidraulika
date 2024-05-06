import matplotlib.pyplot as plt

from mjerenje import Mjerenje

mjerenje1 = Mjerenje(1, 5, 1.49, 0.007, 30.5, 11.3, 12.3, 306, 0.4, specificni_protok=50)
mjerenje2 = Mjerenje(2, 6, 1.74, 0.01, 33.7, 11.2, 15.4, 305, 0.48, specificni_protok=50)
mjerenje3 = Mjerenje(3, 7, 2, 0.014, 38.2, 11, 18.8, 305, 0.6, specificni_protok=50)
mjerenje4 = Mjerenje(4, 8, 2.28, 0.018, 43.6, 10.7, 23.2, 303, 0.74, specificni_protok=50)
mjerenje5 = Mjerenje(5, 9, 2.54, 0.023, 49.7, 10.7, 28.3, 301, 0.9, specificni_protok=50)
mjerenje6 = Mjerenje(6, 10, 2.79, 0.028, 56.1, 10.5, 33.4, 299, 1.04, specificni_protok=50)

# mjerenja = [mjerenje1, mjerenje2, mjerenje3, mjerenje4, mjerenje5, mjerenje6]

# brzina_vrtnje_motora = []
# pad_tlaka_na_hidromotoru = []
# stvarni_moment_hidromotora = []
# mehanicka_snaga_hidromotora = []

# for mjerenje in mjerenja:
#     brzina_vrtnje_motora.append(mjerenje.brzina_vrtnje_u_minuti)
#     pad_tlaka_na_hidromotoru.append(mjerenje.pad_tlaka_bar)
#     stvarni_moment_hidromotora.append(mjerenje.stvarni_moment_njutnmetar)
#     mehanicka_snaga_hidromotora.append(mjerenje.mehanicka_snaga_kilovat)

# Pad tlaka
# plt.plot(brzina_vrtnje_motora, pad_tlaka_na_hidromotoru, marker='o')
# plt.title('Pad tlaka na hidromotoru - Brzina vrtnje hidromotora')
# plt.ylabel('Pad tlaka [bar]')

# Stvarni moment
# plt.plot(brzina_vrtnje_motora, stvarni_moment_hidromotora, marker='o')
# plt.title('Stvarni moment hidromotora - Brzina vrtnje hidromotora')
# plt.ylabel('Stvarni moment [Nm]')

# Mehanicka snaga
# plt.plot(brzina_vrtnje_motora, mehanicka_snaga_hidromotora, marker='o')
# plt.title('Mehanička snaga hidromotora - Brzina vrtnje hidromotora')
# plt.ylabel('Mehanička snaga [kW]')

# plt.xlabel('Brzina vrtnje [rpm]')
# plt.grid(True)
# plt.show()

print(mjerenje1.__str__())