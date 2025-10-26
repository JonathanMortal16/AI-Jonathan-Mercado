import random
import math
# -----------------------------
# 1. Datos de entrenamiento (supervisados)
# -----------------------------
# Dos clases separables más o menos linealmente
random.seed(0)
datos = []

# Clase +1 (roja)
for _ in range(10):
    x = random.uniform(1, 3)
    y = random.uniform(1, 3)
    datos.append((x, y, 1))

# Clase -1 (azul)
for _ in range(10):
    x = random.uniform(4, 6)
    y = random.uniform(4, 6)
    datos.append((x, y, -1))

# -----------------------------
# 2. Funciones auxiliares
# -----------------------------
def dot(v1, v2):
    """Producto punto"""
    return sum(a*b for a,b in zip(v1,v2))

def sign(x):
    return 1 if x >= 0 else -1

# -----------------------------
# 3. Entrenamiento lineal (muy simplificado)
# -----------------------------
# Usamos un perceptrón como aproximación didáctica de una SVM lineal
w = [0.0, 0.0]  # pesos
b = 0.0         # sesgo
tasa_aprendizaje = 0.1

for epoca in range(15):  # pocas iteraciones
    errores = 0
    for x, y, etiqueta in datos:
        entrada = [x, y]
        pred = sign(dot(w, entrada) + b)
        if pred != etiqueta:
            # Actualización (regla del perceptrón)
            w[0] += tasa_aprendizaje * etiqueta * x
            w[1] += tasa_aprendizaje * etiqueta * y
            b += tasa_aprendizaje * etiqueta
            errores += 1
    if errores == 0:
        break

print("=== SVM LINEAL (perceptrón como analogía) ===")
print(f"Pesos finales: w = {w}")
print(f"Sesgo b = {b}")
print()

# -----------------------------
# 4. Clasificación con "núcleo" polinomial
# -----------------------------
# Definimos una función de núcleo (kernel)
def kernel_polinomial(x1, x2, grado=2):
    """
    Núcleo polinomial: (x1·x2 + 1)^grado
    Simula una proyección no lineal de los datos.
    """
    return (dot(x1, x2) + 1) ** grado

# Simulación de clasificación con kernel
# (No implementamos SVM real con kernel, solo ilustramos)
p1 = [2, 2]  # debería ser clase +1
p2 = [5, 5]  # debería ser clase -1
k_val = kernel_polinomial(p1, p2)

print("=== NÚCLEO POLINOMIAL ===")
print(f"Producto punto original entre {p1} y {p2}: {dot(p1, p2):.3f}")
print(f"Producto punto con kernel polinomial grado 2: {k_val:.3f}")
print()
print("Interpretación: el 'núcleo' transforma los datos a un espacio donde")
print("las fronteras no lineales pueden verse lineales.")
