import random
import math

# Número de partículas
N = 1000

# Estado real inicial (posición verdadera del robot)
x_real = 30.0

# Distribución inicial de partículas (hipótesis)
particulas = [random.uniform(0, 100) for _ in range(N)]

# Función de movimiento (modelo dinámico)
def mover(x):
    # El robot se mueve hacia la derecha con ruido
    return x + 1.0 + random.gauss(0, 0.5)

# Función de sensor (medición)
def medir(x):
    # El sensor mide distancia al centro (50) con ruido
    medicion_real = 50 - x  # distancia al centro
    return medicion_real + random.gauss(0, 2.0)

# Probabilidad de una medición dado un estado
def probabilidad_sensor(medicion, x):
    # Distribución gaussiana centrada en el valor esperado
    esperado = 50 - x
    error = medicion - esperado
    sigma = 2.0
    return math.exp(- (error ** 2) / (2 * sigma ** 2))

# ------------------------------------------------------------
# Bucle de simulación
# ------------------------------------------------------------
for paso in range(10):
    # ---- Paso real ----
    x_real = mover(x_real)
    z = medir(x_real)

    # ---- 1. PREDICCIÓN ----
    particulas = [mover(p) for p in particulas]

    # ---- 2. ACTUALIZACIÓN (PESOS) ----
    pesos = [probabilidad_sensor(z, p) for p in particulas]

    # Normalizar los pesos
    total = sum(pesos)
    if total == 0:
        pesos = [1 / N for _ in pesos]
    else:
        pesos = [w / total for w in pesos]

    # ---- 3. RE-MUESTREO ----
    nuevas_particulas = random.choices(particulas, weights=pesos, k=N)
    particulas = nuevas_particulas

    # ---- 4. ESTIMACIÓN ----
    estimado = sum(particulas) / N

    # ---- Mostrar resultados ----
    print(f"Paso {paso+1}")
    print(f"  Posición real: {x_real:.2f}")
    print(f"  Medición: {z:.2f}")
    print(f"  Estimación por filtro de partículas: {estimado:.2f}")
    print("------------------------------------------------------------")
