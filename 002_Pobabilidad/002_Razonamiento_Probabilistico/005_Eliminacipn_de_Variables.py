from itertools import product

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

def factor_alarma(robo, terremoto):
    """Devuelve un factor: P(Alarma=True | R,T) y P(Alarma=False | R,T)"""
    p_true = P_alarma[(robo, terremoto)]
    return {True: p_true, False: 1 - p_true}


def factor_llama(alarma):
    """Devuelve un factor: P(Llama=True|A)"""
    p_true = P_llama[alarma]
    return {True: p_true, False: 1 - p_true}


def eliminar_variable(variable, factores):
    pass  # Solo explicativo — se hará explícito en los pasos siguientes.


# ------------------------------------------------------------
# 1) PRIMERA ELIMINACIÓN: eliminar Terremoto
# ------------------------------------------------------------
def eliminar_terremoto(robo, alarma):
    suma = 0
    for terremoto in [True, False]:
        p_t = P_terremoto[terremoto]
        p_a = factor_alarma(robo, terremoto)[alarma]
        suma += p_t * p_a
    return suma  # Este es el nuevo factor reducido P(A | R)

# ------------------------------------------------------------
# 2) ELIMINAR ALARMA
# ------------------------------------------------------------

def eliminar_alarma(robo, llama=True):
    suma = 0
    for alarma in [True, False]:
        p_l = factor_llama(alarma)[llama]
        p_a_dado_r = eliminar_terremoto(robo, alarma)
        suma += p_l * p_a_dado_r
    return suma  # factor reducido P(Llama | R)

# ------------------------------------------------------------
# 3) Calcular la probabilidad posterior normalizada
# ------------------------------------------------------------

def posterior_eliminacion(llama=True):
    numerador_true = P_robo[True] * eliminar_alarma(True, llama)
    numerador_false = P_robo[False] * eliminar_alarma(False, llama)

    alpha = numerador_true + numerador_false
    p_true = numerador_true / alpha
    p_false = numerador_false / alpha

    return p_true, p_false


# ------------------------------------------------------------
# DEMOSTRACIÓN
# ------------------------------------------------------------
print("=== Eliminación de Variables ===\n")
print("Queremos calcular: P(Robo | LlamaVecino = True)\n")

p_true, p_false = posterior_eliminacion(True)

print(f"P(Robo=True | Llama=True)  = {p_true:.5f}")
print(f"P(Robo=False | Llama=True) = {p_false:.5f}")
print(f"Suma total = {p_true + p_false:.5f}")
