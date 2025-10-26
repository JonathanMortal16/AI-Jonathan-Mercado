import math

# ------------------------------------------------------------
# Definición de modelos HMM simplificados
# ------------------------------------------------------------

# Palabra 1: "sí"
modelo_si = {
    "transiciones": [[0.7, 0.3],
                     [0.0, 1.0]],
    "emisiones": [[0.9, 0.1],  # Estado 0 emite obs=0 con 0.9
                  [0.2, 0.8]], # Estado 1 emite obs=1 con 0.8
    "inicial": [0.6, 0.4]
}

# Palabra 2: "no"
modelo_no = {
    "transiciones": [[0.6, 0.4],
                     [0.3, 0.7]],
    "emisiones": [[0.3, 0.7],
                  [0.8, 0.2]],
    "inicial": [0.5, 0.5]
}

# Secuencia de observaciones (ej. patrones acústicos discretos)
# 0 = sonido bajo, 1 = sonido alto
observaciones = [0, 1, 1]

# ------------------------------------------------------------
# Función de evaluación: probabilidad P(O|modelo)
# Usamos el algoritmo de Viterbi (como en HMM)
# ------------------------------------------------------------
def viterbi(modelo, observaciones):
    A = modelo["transiciones"]
    B = modelo["emisiones"]
    pi = modelo["inicial"]
    N = len(A)
    T = len(observaciones)

    # Inicialización
    delta = [[0.0] * N for _ in range(T)]
    for i in range(N):
        delta[0][i] = pi[i] * B[i][observaciones[0]]

    # Recursión
    for t in range(1, T):
        for i in range(N):
            delta[t][i] = max(delta[t-1][j] * A[j][i] for j in range(N)) * B[i][observaciones[t]]

    # Probabilidad final
    return max(delta[T-1])

# ------------------------------------------------------------
# Evaluación de las dos palabras
# ------------------------------------------------------------
prob_si = viterbi(modelo_si, observaciones)
prob_no = viterbi(modelo_no, observaciones)

# Normalizar (opcional)
suma = prob_si + prob_no
prob_si /= suma
prob_no /= suma

# ------------------------------------------------------------
# Resultado final
# ------------------------------------------------------------
print("=== RECONOCIMIENTO DEL HABLA (Simplificado) ===\n")
print(f"Secuencia de observaciones: {observaciones}")
print(f"P('sí' | O) = {prob_si:.4f}")
print(f"P('no' | O) = {prob_no:.4f}")

if prob_si > prob_no:
    print("\n Palabra reconocida: 'sí'")
else:
    print("\n Palabra reconocida: 'no'")
