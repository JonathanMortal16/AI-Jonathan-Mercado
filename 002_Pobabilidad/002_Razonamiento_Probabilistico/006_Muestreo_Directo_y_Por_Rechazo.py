import random

# Probabilidades base
P_robo = {True: 0.01, False: 0.99}
P_terremoto = {True: 0.02, False: 0.98}

# P(Alarma | Robo, Terremoto)
P_alarma = {
    (True, True): 0.95,
    (True, False): 0.94,
    (False, True): 0.29,
    (False, False): 0.001
}

# P(Llama | Alarma)
P_llama = {True: 0.90, False: 0.05}


# ------------------------------------------------------------
# Funciones de muestreo
# ------------------------------------------------------------

def sample_boolean(prob_true):
    """Devuelve True con probabilidad prob_true"""
    return random.random() < prob_true


def prior_sample():
    robo = sample_boolean(P_robo[True])
    terremoto = sample_boolean(P_terremoto[True])
    alarma = sample_boolean(P_alarma[(robo, terremoto)])
    llama = sample_boolean(P_llama[alarma])
    return {"Robo": robo, "Terremoto": terremoto, "Alarma": alarma, "Llama": llama}


def rejection_sampling(evidencia, N=10000):
    """
    Muestreo por rechazo:
    """
    aceptadas = 0
    conteo_robo_true = 0

    for _ in range(N):
        muestra = prior_sample()
        # Verificar si cumple la evidencia
        consistente = all(muestra[var] == val for var, val in evidencia.items())
        if consistente:
            aceptadas += 1
            if muestra["Robo"]:
                conteo_robo_true += 1

    if aceptadas == 0:
        return None

    p_robo_dado_evidencia = conteo_robo_true / aceptadas
    return p_robo_dado_evidencia, aceptadas


# ------------------------------------------------------------
# DEMOSTRACIÓN
# ------------------------------------------------------------
print("=== Muestreo Directo y por Rechazo ===\n")

# Generar algunas muestras iniciales para ver cómo luce
print("Ejemplos de muestras generadas con muestreo directo:\n")
for i in range(5):
    print(prior_sample())
print()

# Ejecutar muestreo por rechazo con evidencia Llama=True
p_estimada, aceptadas = rejection_sampling({"Llama": True}, N=20000)

print(f"Usando {aceptadas} muestras aceptadas de 20000 totales")
print(f"Estimación: P(Robo=True | Llama=True) ≈ {p_estimada:.3f}")
