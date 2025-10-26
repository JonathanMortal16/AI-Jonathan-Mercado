# Probabilidades conocidas
P_lluvia = 0.3                    # P(H): probabilidad a priori de lluvia
P_no_lluvia = 1 - P_lluvia        # P(~H)

P_mojado_dado_lluvia = 0.9        # P(E | H): si llueve, el suelo está mojado
P_mojado_dado_no_lluvia = 0.2     # P(E | ~H): si no llueve, a veces igual se moja

# Paso 1: Calcular la probabilidad total de ver el suelo mojado
P_mojado = (
    P_mojado_dado_lluvia * P_lluvia +
    P_mojado_dado_no_lluvia * P_no_lluvia
)

# Paso 2: Aplicar Regla de Bayes
P_lluvia_dado_mojado = (
    P_mojado_dado_lluvia * P_lluvia
) / P_mojado

# Paso 3: También podemos calcular P(~H | E)
P_no_lluvia_dado_mojado = (
    P_mojado_dado_no_lluvia * P_no_lluvia
) / P_mojado

# Mostrar resultados
print("=== Regla de Bayes ===")
print(f"P(Lluvia) = {P_lluvia}")
print(f"P(No Lluvia) = {P_no_lluvia}")
print()
print(f"P(Mojado | Lluvia) = {P_mojado_dado_lluvia}")
print(f"P(Mojado | No Lluvia) = {P_mojado_dado_no_lluvia}")
print()
print(f"P(Mojado) = {round(P_mojado, 3)}")
print()
print(f"P(Lluvia | Mojado) = {round(P_lluvia_dado_mojado, 3)}")
print(f"P(No Lluvia | Mojado) = {round(P_no_lluvia_dado_mojado, 3)}")
