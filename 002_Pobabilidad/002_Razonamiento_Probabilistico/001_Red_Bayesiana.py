# 1) Probabilidades a priori (nodos sin padres)
P_robo = {
    True:  0.01,   # P(Robo = True)
    False: 0.99    # P(Robo = False)
}

P_terremoto = {
    True:  0.02,   # P(Terremoto = True)
    False: 0.98    # P(Terremoto = False)
}

# 2) Probabilidades condicionales de la Alarma
P_alarma_given = {
    (True,  True):  0.95,
    (True,  False): 0.94,
    (False, True):  0.29,
    (False, False): 0.001
}

def joint_probability(robo, terremoto, alarma):
    # Probabilidad base de Robo y Terremoto
    p_r = P_robo[robo]
    p_t = P_terremoto[terremoto]

    # Probabilidad de Alarma dada Robo y Terremoto
    p_a_true = P_alarma_given[(robo, terremoto)]
    if alarma:
        p_a = p_a_true
    else:
        p_a = 1 - p_a_true  # porque P(A=False|...)=1-P(A=True|...)

    return p_r * p_t * p_a


def prob_alarma_true():
   #Calcula P(Alarma = True)
    total = 0.0
    for r in [True, False]:
        for t in [True, False]:
            total += joint_probability(r, t, True)
    return total


def prob_robo_and_alarma(robo_value):
    """
    Calcula P(Robo = robo_value, Alarma = True)
    """
    total = 0.0
    for t in [True, False]:
        total += joint_probability(robo_value, t, True)
    return total


def posterior_robo_given_alarma():
    """
    Calcula P(Robo=True | Alarma=True) y P(Robo=False | Alarma=True)
    """

    # Probabilidad total de que la alarma suene
    p_alarm = prob_alarma_true()

    # Prob conjunta de (Robo=True, Alarma=True)
    p_robo_true_alarm = prob_robo_and_alarma(True)

    # Prob conjunta de (Robo=False, Alarma=True)
    p_robo_false_alarm = prob_robo_and_alarma(False)

    # Aplicar Bayes (básicamente dividir entre P(Alarma=True))
    p_robo_true_given_alarm = p_robo_true_alarm / p_alarm
    p_robo_false_given_alarm = p_robo_false_alarm / p_alarm

    # Empaquetar resultados y regresarlos
    return {
        True:  p_robo_true_given_alarm,
        False: p_robo_false_given_alarm,
        "P(Alarma=True)": p_alarm,
        "P(Robo=True,Alarma=True)": p_robo_true_alarm,
        "P(Robo=False,Alarma=True)": p_robo_false_alarm
    }


# ----------------- EJECUCIÓN / DEMO -----------------

print("=== Red Bayesiana: Robo -> Alarma, Terremoto -> Alarma ===\n")

print("Probabilidades base:")
print(f"P(Robo=True) = {P_robo[True]}")
print(f"P(Robo=False) = {P_robo[False]}")
print(f"P(Terremoto=True) = {P_terremoto[True]}")
print(f"P(Terremoto=False) = {P_terremoto[False]}\n")

print("Tabla condicional de la alarma (P(Alarma=True | Robo, Terremoto)):")
for combo, val in P_alarma_given.items():
    r, t = combo
    print(f"  Robo={r}, Terremoto={t} -> {val}")
print()

# Calculamos la probabilidad total de que la alarma suene
p_alarm_true = prob_alarma_true()
print(f"P(Alarma=True) = {p_alarm_true}\n")

# Calculamos las probabilidades posteriores P(Robo | Alarma=True)
posterior = posterior_robo_given_alarma()

print("Posterior después de oír la alarma (Alarma=True):")
print(f"P(Robo=True | Alarma=True)  = {posterior[True]}")
print(f"P(Robo=False | Alarma=True) = {posterior[False]}\n")

print("Chequeo de normalización (debe dar ~1.0):")
print(posterior[True] + posterior[False])
