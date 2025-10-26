# Probabilidades a priori (antes de ver evidencia)
P_lluvia = 0.3          # P(Lluvia)
P_no_lluvia = 1 - P_lluvia  # P(NoLluvia) = 0.7

# Modelo del mundo / sensor:
# Qué tan probable es ver el suelo mojado bajo cada hipótesis
P_mojado_dado_lluvia = 0.9      # P(Mojado | Lluvia)
P_mojado_dado_no_lluvia = 0.2   # P(Mojado | NoLluvia)

# Paso 1:
# Calculamos valores "no normalizados" (puntuaciones)
score_lluvia = P_mojado_dado_lluvia * P_lluvia
score_no_lluvia = P_mojado_dado_no_lluvia * P_no_lluvia

print("Score lluvia (no normalizado):    ", round(score_lluvia, 4))
print("Score no lluvia (no normalizado): ", round(score_no_lluvia, 4))
print()

# Paso 2:
# Normalización.
normalizador = score_lluvia + score_no_lluvia

P_lluvia_dado_mojado = score_lluvia / normalizador
P_no_lluvia_dado_mojado = score_no_lluvia / normalizador

# Paso 3:
# Mostramos la distribución final condicionada
print("Distribución normalizada dado 'suelo mojado':")
print("P(Lluvia | Mojado)    =", round(P_lluvia_dado_mojado, 3))
print("P(NoLluvia | Mojado)  =", round(P_no_lluvia_dado_mojado, 3))

# Comprobación rápida:
print()
print("Suma total =", round(P_lluvia_dado_mojado + P_no_lluvia_dado_mojado, 3))
