# Estados ocultos
estados = ["Soleado", "Lluvioso"]

# Observaciones
observaciones_nombres = ["Seco", "Mojado"]

# Matriz de transición (A)
A = [
    [0.8, 0.4],  # Siguiente = Soleado | [Soleado, Lluvioso]
    [0.2, 0.6]   # Siguiente = Lluvioso | [Soleado, Lluvioso]
]

# Matriz de emisión (B)
B = [
    [0.9, 0.2],  # P(Seco | [Soleado, Lluvioso])
    [0.1, 0.8]   # P(Mojado | [Soleado, Lluvioso])
]

# Distribución inicial (π)
pi = [0.5, 0.5]

# Secuencia de observaciones: 0=Seco, 1=Mojado, 1=Mojado
observaciones = [0, 1, 1]

# Número de estados y observaciones
N = len(estados)
T = len(observaciones)

# ------------------------------------------------------------
# Algoritmo de Viterbi
# ------------------------------------------------------------
delta = [[0.0 for _ in range(N)] for _ in range(T)]
psi = [[0 for _ in range(N)] for _ in range(T)]

# Inicialización (t=0)
for i in range(N):
    delta[0][i] = pi[i] * B[observaciones[0]][i]
    psi[0][i] = 0

# Recursión
for t in range(1, T):
    for i in range(N):
        max_prob = -1
        max_estado = 0
        for j in range(N):
            prob = delta[t-1][j] * A[i][j]
            if prob > max_prob:
                max_prob = prob
                max_estado = j
        delta[t][i] = max_prob * B[observaciones[t]][i]
        psi[t][i] = max_estado

# Terminación
P_final = max(delta[T-1])
estado_final = delta[T-1].index(P_final)

# Reconstruir la secuencia de estados más probable
secuencia_estados = [estado_final]
for t in range(T-1, 0, -1):
    estado_final = psi[t][estado_final]
    secuencia_estados.insert(0, estado_final)

# ------------------------------------------------------------
# Mostrar resultados
# ------------------------------------------------------------
print("=== MODELO OCULTO DE MARKOV ===")
print("Secuencia de observaciones:", [observaciones_nombres[o] for o in observaciones])
print("\nSecuencia más probable de estados:")
for t in range(T):
    print(f"Día {t+1}: {estados[secuencia_estados[t]]}")

print("\nProbabilidad total del camino:", round(P_final, 5))
