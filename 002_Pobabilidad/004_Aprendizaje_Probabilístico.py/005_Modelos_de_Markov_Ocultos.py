import math
# ----------------------------
# 1. Definición del modelo HMM
# ----------------------------
estados = ['Soleado', 'Lluvioso']
observaciones = ['Caminar', 'Comprar', 'Limpiar']

# Probabilidades iniciales π
pi = {
    'Soleado': 0.6,
    'Lluvioso': 0.4
}

# Matriz de transición A: P(estado_actual | estado_anterior)
A = {
    'Soleado': {'Soleado': 0.7, 'Lluvioso': 0.3},
    'Lluvioso': {'Soleado': 0.4, 'Lluvioso': 0.6}
}

# Matriz de emisión B: P(observación | estado)
B = {
    'Soleado': {'Caminar': 0.4, 'Comprar': 0.4, 'Limpiar': 0.2},
    'Lluvioso': {'Caminar': 0.1, 'Comprar': 0.3, 'Limpiar': 0.6}
}

# Secuencia observada
observaciones_secuencia = ['Caminar', 'Comprar', 'Limpiar']

# ----------------------------
# 2. Algoritmo de Viterbi
# ----------------------------
def viterbi(obs, estados, pi, A, B):
    """
    Implementa el algoritmo de Viterbi para encontrar
    la secuencia de estados más probable dada una secuencia de observaciones.
    """
    delta = []
    psi = []

    # Inicialización
    delta_t = {}
    psi_t = {}
    for s in estados:
        delta_t[s] = pi[s] * B[s][obs[0]]
        psi_t[s] = None
    delta.append(delta_t)
    psi.append(psi_t)

    # Recursión
    for t in range(1, len(obs)):
        delta_t = {}
        psi_t = {}
        for s in estados:
            # Para cada estado s, buscamos el mejor estado previo s'
            max_prob = -1
            mejor_estado = None
            for s_prev in estados:
                prob = delta[t - 1][s_prev] * A[s_prev][s] * B[s][obs[t]]
                if prob > max_prob:
                    max_prob = prob
                    mejor_estado = s_prev
            delta_t[s] = max_prob
            psi_t[s] = mejor_estado
        delta.append(delta_t)
        psi.append(psi_t)

    # Terminación: mejor estado final
    prob_final = max(delta[-1].values())
    ultimo_estado = max(delta[-1], key=delta[-1].get)

    # Retroceso para encontrar la secuencia óptima
    secuencia_estados = [ultimo_estado]
    for t in range(len(obs) - 1, 0, -1):
        ultimo_estado = psi[t][ultimo_estado]
        secuencia_estados.insert(0, ultimo_estado)

    return secuencia_estados, prob_final

# ----------------------------
# 3. Ejecutar el algoritmo
# ----------------------------
secuencia, probabilidad = viterbi(observaciones_secuencia, estados, pi, A, B)

# ----------------------------
# 4. Mostrar resultados
# ----------------------------
print("=== MODELO DE MARKOV OCULTO ===\n")
print("Secuencia de observaciones:", observaciones_secuencia)
print("Secuencia más probable de estados ocultos:")
print(" → ".join(secuencia))
print(f"\nProbabilidad total: {probabilidad:.6f}")
