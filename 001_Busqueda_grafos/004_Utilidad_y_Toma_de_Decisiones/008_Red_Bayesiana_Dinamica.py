# Estados posibles
estados = ["soleado", "lluvioso"]

# Probabilidades de transición P(X_t+1 | X_t)
transicion = {
    "soleado": {"soleado": 0.7, "lluvioso": 0.3},
    "lluvioso": {"soleado": 0.4, "lluvioso": 0.6}
}

# Probabilidades de observación P(O_t | X_t)
observacion = {
    "soleado": {"despejado": 0.9, "nublado": 0.1},
    "lluvioso": {"despejado": 0.2, "nublado": 0.8}
}

# Creencia inicial sobre el estado (b0)
creencia = {"soleado": 0.5, "lluvioso": 0.5}

def predecir(creencia):
    """Predicción: aplica modelo de transición."""
    nueva = {}
    for s_next in estados:
        suma = 0
        for s in estados:
            suma += creencia[s] * transicion[s][s_next]
        nueva[s_next] = suma
    return nueva

def actualizar(creencia_predicha, observacion_recibida):
    """Actualización: aplica modelo de observación."""
    nueva = {}
    for s in estados:
        nueva[s] = observacion[s][observacion_recibida] * creencia_predicha[s]
    total = sum(nueva.values())
    for s in estados:
        nueva[s] /= total
    return nueva

# Simulamos 3 pasos temporales
obs = ["despejado", "nublado", "nublado"]
print("Creencia inicial:", creencia)

for t, o in enumerate(obs, start=1):
    pred = predecir(creencia)
    creencia = actualizar(pred, o)
    print(f"\nTiempo {t}: observación = {o}")
    print(f"Creencia actualizada: {creencia}")
