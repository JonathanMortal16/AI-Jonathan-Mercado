import numpy as np

# Estados ocultos
estados = ["Soleado", "Lluvioso"]

# Posibles observaciones
observaciones = ["Seco", "Mojado"]

# Matriz de transición entre estados (T[next][current])
T = np.array([
    [0.8, 0.4],  # Soleado mañana
    [0.2, 0.6]   # Lluvioso mañana
])

# Matriz de emisión (E[obs][state])
E = np.array([
    [0.9, 0.2],  # Prob de observar "Seco"
    [0.1, 0.8]   # Prob de observar "Mojado"
])

# Distribución inicial (día 0)
P_inicial = np.array([0.5, 0.5])  # No sabemos si hoy es Soleado o Lluvioso

# Secuencia de observaciones
# 0 = Seco, 1 = Mojado
observaciones_dias = [0, 1, 1]  # Ejemplo: Día1 Seco, Día2 Mojado, Día3 Mojado

def normalizar(vector):
    """Ajusta el vector para que las probabilidades sumen 1."""
    return vector / np.sum(vector)

# --- FILTRADO (Forward) ---
P_actual = P_inicial

print("=== FILTRADO (estimando el estado actual con las observaciones) ===")
for t, obs in enumerate(observaciones_dias):
    # 1. Predicción: aplicamos la matriz de transición
    P_predicho = T @ P_actual
    # 2. Incorporamos la evidencia (observación)
    P_filtrado = E[obs, :] * P_predicho
    # 3. Normalizamos
    P_filtrado = normalizar(P_filtrado)
    P_actual = P_filtrado

    print(f"Día {t+1} | Obs: {observaciones[obs]}")
    print(f"  Prob(Soleado) = {P_actual[0]:.3f}")
    print(f"  Prob(Lluvioso) = {P_actual[1]:.3f}")
    print("------------------------------------------------------------")

# --- PREDICCIÓN ---
print("\n=== PREDICCIÓN (estado futuro sin nueva observación) ===")
P_futuro = T @ P_actual
print(f"Prob(Soleado mañana) = {P_futuro[0]:.3f}")
print(f"Prob(Lluvioso mañana) = {P_futuro[1]:.3f}")
