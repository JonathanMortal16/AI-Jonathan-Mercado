import random
import math
def normal_pdf(x, mu, sigma):
    """
    Calcula la densidad de probabilidad de una Normal(mu, sigma^2)
    en el punto x.
    Fórmula:
       f(x) = (1/(sqrt(2*pi)*sigma)) * exp( - (x-mu)^2 / (2*sigma^2) )
    """
    coef = 1.0 / (math.sqrt(2.0 * math.pi) * sigma)
    exp_term = math.exp(- ((x - mu) ** 2) / (2.0 * sigma * sigma))
    return coef * exp_term

# ------------------------------------------------------------
# 1. Generamos datos sintéticos SIN etiquetas verdaderas
# ------------------------------------------------------------
# Para prueba, vamos a simular que TENEMOS dos "grupos reales":
mu1_real = 160.0  # por ejemplo "grupo 1" ~ personas bajitas
mu2_real = 180.0  # "grupo 2" ~ personas altas
sigma1_real = 5.0
sigma2_real = 5.0

# Mezcla real: porcentaje del grupo 1
pi1_real = 0.4   # 40% de los datos vienen del grupo 1
pi2_real = 1.0 - pi1_real

random.seed(0)   # semilla para reproducibilidad

def generar_punto():
    """
    Genera UN punto según la mezcla real.
    Con prob pi1_real viene de N(mu1_real, sigma1_real^2),
    y con prob pi2_real viene de N(mu2_real, sigma2_real^2).
    """
    r = random.random()
    if r < pi1_real:
        # grupo 1
        return random.gauss(mu1_real, sigma1_real)
    else:
        # grupo 2
        return random.gauss(mu2_real, sigma2_real)

# Creamos un dataset sin etiquetas (solo números)
datos = [generar_punto() for _ in range(30)]

# ------------------------------------------------------------
# 2. Inicializamos parámetros del modelo que QUEREMOS APRENDER
# ------------------------------------------------------------
# Adivina medias iniciales (mal, a propósito)
mu1 = 150.0
mu2 = 190.0

# Suponemos desviaciones conocidas (simples, fijas)
sigma1 = 5.0
sigma2 = 5.0

# Peso inicial de mezcla
pi1 = 0.5  # empezamos creyendo que ambos grupos son mitad y mitad

# ------------------------------------------------------------
# 3. Algoritmo EM iterativo
# ------------------------------------------------------------
for iteracion in range(1, 11):  # 10 iteraciones de EM

    # ======== E-STEP ========
    # Calculamos responsabilidades:
    r1_list = []
    r2_list = []

    for x in datos:
        # probabilidad conjunta de x con cada grupo:
        # pi1 * N(x | mu1, sigma1^2)
        p1 = pi1 * normal_pdf(x, mu1, sigma1)

        # pi2 * N(x | mu2, sigma2^2)
        p2 = (1.0 - pi1) * normal_pdf(x, mu2, sigma2)

        # normalizamos para obtener prob condicional
        total = p1 + p2
        if total == 0:
            # caso numéricamente raro, pero por seguridad
            r1 = 0.5
            r2 = 0.5
        else:
            r1 = p1 / total
            r2 = p2 / total

        r1_list.append(r1)
        r2_list.append(r2)

    # ======== M-STEP ========
    # Actualizamos parámetros usando las responsabilidades como pesos

    # pi1 nuevo = promedio de r1[i]
    sum_r1 = sum(r1_list)
    N = len(datos)
    pi1 = sum_r1 / N  # "qué fracción esperada es grupo 1"

    # mu1 nuevo = promedio ponderado de los datos con peso r1[i]
    # mu1 = (sum_i r1[i] * x_i) / (sum_i r1[i])
    if sum_r1 == 0:
        # Evitar división entre cero si r1_list es todo 0
        mu1 = mu1
    else:
        num_mu1 = 0.0
        for x, r1 in zip(datos, r1_list):
            num_mu1 += r1 * x
        mu1 = num_mu1 / sum_r1

    # mu2 nuevo = promedio ponderado de los datos con peso r2[i]
    sum_r2 = sum(r2_list)
    if sum_r2 == 0:
        mu2 = mu2
    else:
        num_mu2 = 0.0
        for x, r2 in zip(datos, r2_list):
            num_mu2 += r2 * x
        mu2 = num_mu2 / sum_r2

    # (Si quisiéramos también aprender sigma1 y sigma2,
    #  aquí calcularíamos la varianza ponderada. Para mantenerlo
    #  simple no lo hacemos.)

    # Imprimir cómo va la convergencia
    print(f"Iteración {iteracion}:")
    print(f"  pi1 estimado  = {pi1:.3f}  (fracción del grupo 1)")
    print(f"  mu1 estimado  = {mu1:.3f}")
    print(f"  mu2 estimado  = {mu2:.3f}")
    print("")

# ------------------------------------------------------------
# 4. Interpretación final
# ------------------------------------------------------------
print("=== Valores reales vs estimados ===")
print(f"pi1 real = {pi1_real:.3f}")
print(f"mu1 real = {mu1_real:.3f}")
print(f"mu2 real = {mu2_real:.3f}")
print("")
print("Nota:")
print("- pi1 debería acercarse a ~0.4 (40%).")
print("- mu1 debería acercarse a ~160.")
print("- mu2 debería acercarse a ~180.")
print("Aunque empezamos con valores malos, EM los fue corrigiendo.")
