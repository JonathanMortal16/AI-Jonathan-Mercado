# Estados:
#   0 = Soleado
#   1 = Lluvioso
estados = ["Soleado", "Lluvioso"]

# Observaciones:
#   0 = Seco
#   1 = Mojado
observaciones_nombres = ["Seco", "Mojado"]

# Matriz de transición T[next][current]
T = [
    [0.8, 0.4],  # Prob de ir a Soleado (0) desde [Soleado, Lluvioso]
    [0.2, 0.6]   # Prob de ir a Lluvioso (1) desde [Soleado, Lluvioso]
]

# Matriz de emisión E[observacion][estado]
E = [
    [0.9, 0.2],  # Prob de ver "Seco" (0) si [Soleado, Lluvioso]
    [0.1, 0.8]   # Prob de ver "Mojado" (1) si [Soleado, Lluvioso]
]

# Distribución inicial sobre los estados ocultos
P_inicial = [0.5, 0.5]

# Secuencia de observaciones registradas en el tiempo
# Día1 = Seco(0), Día2 = Mojado(1), Día3 = Mojado(1)
observaciones_dias = [0, 1, 1]


def normalizar(vec):
    s = sum(vec)
    if s == 0:
        return [0 for _ in vec]
    return [v / s for v in vec]


# ------------------------------------------------------------
# 1. FORWARD: calcular alpha[t][estado]
# ------------------------------------------------------------
alpha = []

# Paso inicial t = 0
obs0 = observaciones_dias[0]
alpha_0 = [
    P_inicial[i] * E[obs0][i]   # P(estado_i inicial) * P(obs0 | estado_i)
    for i in range(2)
]
alpha_0 = normalizar(alpha_0)
alpha.append(alpha_0)

# Pasos siguientes t = 1..T-1
for t in range(1, len(observaciones_dias)):
    obs_t = observaciones_dias[t]
    alpha_t = []
    for i in range(2):  # i = estado actual
        # sum_j alpha[t-1][j] * P(i | j)
        suma_caminos = 0.0
        for j in range(2):  # j = estado anterior
            suma_caminos += alpha[t-1][j] * T[i][j]

        # ahora multiplicar por la prob de observar lo que vimos hoy
        val = E[obs_t][i] * suma_caminos
        alpha_t.append(val)

    alpha_t = normalizar(alpha_t)
    alpha.append(alpha_t)

# ------------------------------------------------------------
# 2. BACKWARD: calcular beta[t][estado]
# ------------------------------------------------------------
T_total = len(observaciones_dias)
beta = [None] * T_total

# Paso final: beta[T-1] = [1, 1] (no queda futuro)
beta[T_total - 1] = [1.0, 1.0]

# Pasos hacia atrás
for t in range(T_total - 2, -1, -1):  # desde T-2 hasta 0
    beta_t = []
    for i in range(2):  # estado actual i en tiempo t
        suma_futuros = 0.0
        for j in range(2):  # estado siguiente j en tiempo t+1
            suma_futuros += T[j][i] * E[observaciones_dias[t+1]][j] * beta[t+1][j]
        beta_t.append(suma_futuros)

    beta_t = normalizar(beta_t)
    beta[t] = beta_t

# ------------------------------------------------------------
# 3. SUAVIZADO GAMMA: combinar alpha y beta
# ------------------------------------------------------------
gamma = []
for t in range(T_total):
    producto = [
        alpha[t][i] * beta[t][i]
        for i in range(2)
    ]
    gamma_t = normalizar(producto)
    gamma.append(gamma_t)

# ------------------------------------------------------------
# 4. MOSTRAR RESULTADOS
# ------------------------------------------------------------
print("=== Resultados del Algoritmo Hacia Delante-Atrás ===\n")

for t in range(T_total):
    obs_name = observaciones_nombres[observaciones_dias[t]]
    print(f"Tiempo t = {t+1}, Observación = {obs_name}")
    print(f"  alpha (filtrado hasta aquí):")
    print(f"    P(Soleado) = {alpha[t][0]:.3f} | P(Lluvioso) = {alpha[t][1]:.3f}")
    print(f"  beta  (info futura hacia atrás):")
    print(f"    P(futuro | Soleado) = {beta[t][0]:.3f} | P(futuro | Lluvioso) = {beta[t][1]:.3f}")
    print(f"  gamma (suavizado final):")
    print(f"    P(Soleado en t | TODAS las obs) = {gamma[t][0]:.3f}")
    print(f"    P(Lluvioso en t | TODAS las obs) = {gamma[t][1]:.3f}")
    print("------------------------------------------------------------")
