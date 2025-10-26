# Estados posibles
estados = ["limpio", "sucio"]

# Creencia inicial (qué tan probable creo estar en cada estado)
creencia = {"limpio": 0.5, "sucio": 0.5}

# Modelo de observaciones: O(observacion | estado)
# Supongamos que el sensor puede decir "sensor_limpio" o "sensor_sucio"
O = {
    ("sensor_limpio", "limpio"): 0.8,
    ("sensor_limpio", "sucio"): 0.1,
    ("sensor_sucio", "limpio"): 0.2,
    ("sensor_sucio", "sucio"): 0.9
}

# Transición simple (suponemos que el estado no cambia con la acción "nada")
P = {
    ("limpio", "nada", "limpio"): 1.0,
    ("sucio", "nada", "sucio"): 1.0
}

def actualizar_creencia(creencia, accion, observacion):
    nueva = {}
    for s_prime in estados:
        suma = 0
        for s in estados:
            p_trans = P.get((s, accion, s_prime), 0)
            suma += p_trans * creencia[s]
        nueva[s_prime] = O[(observacion, s_prime)] * suma

    # Normalización
    total = sum(nueva.values())
    for s_prime in estados:
        nueva[s_prime] /= total
    return nueva

# Observación recibida por el sensor
observacion = "sensor_sucio"
accion = "nada"

print("Creencia anterior:", creencia)
nueva_creencia = actualizar_creencia(creencia, accion, observacion)
print(f"Observación recibida: {observacion}")
print("Nueva creencia actualizada:", nueva_creencia)
