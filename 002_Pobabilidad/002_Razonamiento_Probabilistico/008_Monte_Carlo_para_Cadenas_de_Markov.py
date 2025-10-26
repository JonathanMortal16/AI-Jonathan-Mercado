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


def sample_from_prob(p_true):
    """Regresa True con prob p_true, False con 1-p_true"""
    return random.random() < p_true


def prob_alarma_given(robo, terremoto, alarma_val):
    """P(Alarma = alarma_val | Robo, Terremoto)"""
    p_a_true = P_alarma[(robo, terremoto)]
    return p_a_true if alarma_val else (1 - p_a_true)


def prob_llama_given(alarma_val, llama_val=True):
    """P(Llama = llama_val | Alarma)"""
    p_l_true = P_llama[alarma_val]
    return p_l_true if llama_val else (1 - p_l_true)


def sample_robo_given(terremoto, alarma, llama=True):
    """
    Muestrea Robo ~ P(Robo | Terremoto, Alarma, Llama=True)
    """
    pesos = {}
    for r_val in [True, False]:
        p_r = P_robo[r_val]
        p_a = prob_alarma_given(r_val, terremoto, alarma)
        p_l = prob_llama_given(alarma, llama)
        pesos[r_val] = p_r * p_a * p_l

    total = pesos[True] + pesos[False]
    p_true = pesos[True] / total
    return sample_from_prob(p_true)


def sample_terremoto_given(robo, alarma, llama=True):
    """
    Muestrea Terremoto ~ P(Terremoto | Robo, Alarma, Llama=True)
    """
    pesos = {}
    for t_val in [True, False]:
        p_t = P_terremoto[t_val]
        p_a = prob_alarma_given(robo, t_val, alarma)
        p_l = prob_llama_given(alarma, llama)
        pesos[t_val] = p_t * p_a * p_l

    total = pesos[True] + pesos[False]
    p_true = pesos[True] / total
    return sample_from_prob(p_true)


def sample_alarma_given(robo, terremoto, llama=True):
    """
    Muestrea Alarma ~ P(Alarma | Robo, Terremoto, Llama=True)
    """
    pesos = {}
    for a_val in [True, False]:
        p_a = prob_alarma_given(robo, terremoto, a_val)
        p_l = prob_llama_given(a_val, llama)
        pesos[a_val] = p_a * p_l

    total = pesos[True] + pesos[False]
    p_true = pesos[True] / total
    return sample_from_prob(p_true)


def gibbs_sampling(num_iter=20000, burn_in=2000):
    # 1. Estado inicial (puede ser cualquiera razonable)
    estado = {
        "Robo": False,
        "Terremoto": False,
        "Alarma": True,
        "Llama": True  # Evidencia fija
    }

    conteo_robo_true = 0
    conteo_total = 0

    for i in range(num_iter):
        # Actualizamos cada variable oculta condicionalmente a las otras
        estado["Robo"] = sample_robo_given(
            terremoto=estado["Terremoto"],
            alarma=estado["Alarma"],
            llama=True
        )

        estado["Terremoto"] = sample_terremoto_given(
            robo=estado["Robo"],
            alarma=estado["Alarma"],
            llama=True
        )

        estado["Alarma"] = sample_alarma_given(
            robo=estado["Robo"],
            terremoto=estado["Terremoto"],
            llama=True
        )

        # NOTA: "Llama" la mantenemos fija en True porque es evidencia

        # Después del burn-in empezamos a contar muestras
        if i >= burn_in:
            conteo_total += 1
            if estado["Robo"]:
                conteo_robo_true += 1

    # Estimación final
    p_robo_true = conteo_robo_true / conteo_total
    p_robo_false = 1 - p_robo_true
    return p_robo_true, p_robo_false


# -------- DEMO --------
print("=== Monte Carlo para Cadenas de Markov (Gibbs Sampling) ===\n")
print("Estimando P(Robo | Llama=True)...\n")

p_true, p_false = gibbs_sampling(num_iter=20000, burn_in=2000)

print(f"P(Robo=True | Llama=True)  ≈ {p_true:.4f}")
print(f"P(Robo=False | Llama=True) ≈ {p_false:.4f}")
print(f"Suma total ≈ {(p_true + p_false):.4f} (debe ser ~1.0)")
