from itertools import product

# 1. Probabilidades base (a priori)
P_robo = {True: 0.01, False: 0.99}
P_terremoto = {True: 0.02, False: 0.98}

# 2. Probabilidades condicionales de Alarma
P_alarma = {
    (True, True): 0.95,     # P(Alarma|Robo,Terremoto)
    (True, False): 0.94,
    (False, True): 0.29,
    (False, False): 0.001
}

# 3. Probabilidades condicionales de que el Vecino llame
P_llama = {
    True: 0.90,   # P(Llama|Alarma=True)
    False: 0.05   # P(Llama|Alarma=False)
}

# ------------------------------------------------------------
# Funciones auxiliares
# ------------------------------------------------------------
def joint_prob(robo, terremoto, alarma, llama):
    """
    Calcula la probabilidad conjunta:
    """
    p_r = P_robo[robo]
    p_t = P_terremoto[terremoto]
    p_a = P_alarma[(robo, terremoto)] if alarma else (1 - P_alarma[(robo, terremoto)])
    p_l = P_llama[alarma] if llama else (1 - P_llama[alarma])
    return p_r * p_t * p_a * p_l

def inferencia_por_enumeracion(llama_valor=True):
    """
    Calcula P(Robo=True | Llama=llama_valor)
    """
    # Sumamos sobre todos los casos posibles
    numerador_true = 0.0
    numerador_false = 0.0
    for terremoto, alarma in product([True, False], [True, False]):
        numerador_true  += joint_prob(True, terremoto, alarma, llama_valor)
        numerador_false += joint_prob(False, terremoto, alarma, llama_valor)

    # Normalización
    alpha = numerador_true + numerador_false
    p_true_given = numerador_true / alpha
    p_false_given = numerador_false / alpha

    return p_true_given, p_false_given

# ------------------------------------------------------------
# DEMO
# ------------------------------------------------------------
print("=== Inferencia por Enumeración ===\n")
print("Queremos calcular: P(Robo | LlamaVecino = True)\n")

p_true, p_false = inferencia_por_enumeracion(llama_valor=True)

print(f"P(Robo=True | Llama=True)  = {p_true:.5f}")
print(f"P(Robo=False | Llama=True) = {p_false:.5f}")
print(f"Suma total = {p_true + p_false:.5f} (debe ser ≈1)")
