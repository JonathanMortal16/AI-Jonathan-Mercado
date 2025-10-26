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
# FUNCIONES AUXILIARES
# ------------------------------------------------------------

def sample_boolean(prob_true):
    """Devuelve True con probabilidad prob_true"""
    return random.random() < prob_true


def likelihood_weighting(evidencia, N=10000):
    """
    Realiza muestreo ponderado.
    """
    pesos_robo_true = 0.0
    pesos_robo_false = 0.0

    for _ in range(N):
        # --- Paso 1: inicializar peso y valores ---
        w = 1.0
        muestra = {}

        # --- Paso 2: muestreo según el orden topológico ---

        # 1. Robo
        muestra["Robo"] = sample_boolean(P_robo[True])

        # 2. Terremoto
        muestra["Terremoto"] = sample_boolean(P_terremoto[True])

        # 3. Alarma depende de Robo y Terremoto
        p_alarma_true = P_alarma[(muestra["Robo"], muestra["Terremoto"])]
        # Si la alarma está en la evidencia, se fija y se pondera
        if "Alarma" in evidencia:
            if evidencia["Alarma"]:
                w *= p_alarma_true
                muestra["Alarma"] = True
            else:
                w *= (1 - p_alarma_true)
                muestra["Alarma"] = False
        else:
            muestra["Alarma"] = sample_boolean(p_alarma_true)

        # 4. Llama depende de Alarma
        p_llama_true = P_llama[muestra["Alarma"]]
        if "Llama" in evidencia:
            if evidencia["Llama"]:
                w *= p_llama_true
                muestra["Llama"] = True
            else:
                w *= (1 - p_llama_true)
                muestra["Llama"] = False
        else:
            muestra["Llama"] = sample_boolean(p_llama_true)

        # --- Paso 3: acumular pesos según valor de Robo ---
        if muestra["Robo"]:
            pesos_robo_true += w
        else:
            pesos_robo_false += w

    # --- Paso 4: normalización ---
    total = pesos_robo_true + pesos_robo_false
    p_robo_true = pesos_robo_true / total
    p_robo_false = pesos_robo_false / total

    return p_robo_true, p_robo_false


# ------------------------------------------------------------
# DEMOSTRACIÓN
# ------------------------------------------------------------
print("=== Ponderación de Verosimilitud ===\n")

evidencia = {"Llama": True}

p_true, p_false = likelihood_weighting(evidencia, N=20000)

print(f"Estimación con 20000 muestras:")
print(f"P(Robo=True | Llama=True)  ≈ {p_true:.4f}")
print(f"P(Robo=False | Llama=True) ≈ {p_false:.4f}")
print(f"Suma total ≈ {p_true + p_false:.4f}")
