import random
# --------------------------
# 1. Parámetro REAL del mundo
# --------------------------
prob_real_cara = 0.7  # 70% de probabilidad de salir CARA

# --------------------------
# 2. Prior inicial
# --------------------------
alpha = 1
beta = 1

# Contadores útiles solo para imprimir
caras_observadas = 0
cruces_observadas = 0

print("=== Aprendizaje Bayesiano de una moneda ===")
print(f"Valor REAL oculto de la moneda (θ real): {prob_real_cara:.2f}")
print("Prior inicial: Beta(alpha=1, beta=1) -> creencia totalmente uniforme\n")

# --------------------------
# 3. Función para simular un lanzamiento de moneda
# --------------------------
def lanzar_moneda(prob_cara):
    """Regresa 'C' para cara o 'X' para cruz, usando la probabilidad dada."""
    r = random.random()  # número entre 0.0 y 1.0
    if r < prob_cara:
        return 'C'  # cara
    else:
        return 'X'  # cruz

# --------------------------
# 4. Observamos lanzamientos uno por uno
# --------------------------
num_lanzamientos = 20  # Puedes cambiarlo para más evidencia

for i in range(1, num_lanzamientos + 1):

    # Simulamos evidencia nueva:
    resultado = lanzar_moneda(prob_real_cara)

    # Actualizamos contadores "reales"
    if resultado == 'C':
        caras_observadas += 1
        alpha += 1   # ver una CARA incrementa alpha
    else:
        cruces_observadas += 1
        beta += 1    # ver una CRUZ incrementa beta

    # Estimación Bayesiana actual de θ = P(CARA)
    # (El valor esperado de la Beta actualizada)
    theta_estimado = alpha / (alpha + beta)

    # Imprimir el estado después de este dato
    print(f"Lanzamiento {i:2d}: {resultado}")
    print(f"  Caras   observadas: {caras_observadas}")
    print(f"  Cruces  observadas: {cruces_observadas}")
    print(f"  Posterior actual: Beta(alpha={alpha}, beta={beta})")
    print(f"  Estimación Bayesiana de P(CARA): {theta_estimado:.3f}\n")

# --------------------------
# 5. Interpretación final
# --------------------------
print("=== Resumen Final ===")
print(f"Después de {num_lanzamientos} lanzamientos:")
print(f"  Caras totales:  {caras_observadas}")
print(f"  Cruces totales: {cruces_observadas}")
print(f"  Distribución posterior final: Beta({alpha}, {beta})")

theta_final = alpha / (alpha + beta)
print(f"  Nuestra mejor estimación (media posterior) de θ = P(CARA): {theta_final:.3f}")
print(f"  Valor real oculto era: {prob_real_cara:.3f}")
print("\nObserva cómo la estimación se va acercando al valor real con más datos.")
