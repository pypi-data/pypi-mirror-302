import numpy as np

# Exemple de vecteur
x = np.array([1, 2, np.nan, 4, 5])

# Calculer le tableau des sommes cumulées
S = np.zeros(len(x) + 1)
S[1:] = np.nancumsum(x)

print(S)
print(np.nansum(x[0:5]))
print(S[5] - S[0])  