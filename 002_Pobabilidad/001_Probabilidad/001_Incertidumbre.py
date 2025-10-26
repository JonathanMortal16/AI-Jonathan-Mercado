# Probabilidades iniciales (a priori)
P_lluvia = 0.3          # Probabilidad de que llueva
P_no_lluvia = 1 - P_lluvia

# Comportamiento del "sensor"
P_mojado_dado_lluvia = 0.9      # Si llueve, casi siempre el suelo está mojado
P_mojado_dado_no_lluvia = 0.2   # Si no llueve, a veces igual se moja (lavado, fuga, etc.)

# Probabilidad total de que el suelo esté mojado
P_mojado = (
    P_mojado_dado_lluvia * P_lluvia +
    P_mojado_dado_no_lluvia * P_no_lluvia
)

# Regla de Bayes: probabilidad de lluvia dado que el suelo está mojado
P_lluvia_dado_mojado = (
    P_mojado_dado_lluvia * P_lluvia
) / P_mojado

# Probabilidad contraria
P_no_lluvia_dado_mojado = (
    P_mojado_dado_no_lluvia * P_no_lluvia
) / P_mojado

# Resultados
print("Probabilidad de lluvia:", round(P_lluvia, 3))
print("Probabilidad de NO lluvia:", round(P_no_lluvia, 3))
print()
print("Probabilidad total de ver suelo mojado:", round(P_mojado, 3))
print()
print("Prob(lluvia | suelo mojado):", round(P_lluvia_dado_mojado, 3))
print("Prob(NO lluvia | suelo mojado):", round(P_no_lluvia_dado_mojado, 3))