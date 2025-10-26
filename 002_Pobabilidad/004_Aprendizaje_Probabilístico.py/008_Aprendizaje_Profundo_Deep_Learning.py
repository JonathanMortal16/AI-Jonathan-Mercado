import math
import random
# -----------------------------
# Funciones auxiliares
# -----------------------------
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def derivada_sigmoid(x):
    s = sigmoid(x)
    return s * (1 - s)

# -----------------------------
# Datos de entrenamiento
# -----------------------------
# Clase 0: puntos cerca de (1,1)
# Clase 1: puntos cerca de (4,4)
random.seed(0)
datos = []
for _ in range(10):
    datos.append(([random.uniform(0.5, 1.5), random.uniform(0.5, 1.5)], [0]))
for _ in range(10):
    datos.append(([random.uniform(3.5, 4.5), random.uniform(3.5, 4.5)], [1]))

# -----------------------------
# Arquitectura de la red
# -----------------------------
input_size = 2
hidden1_size = 3
hidden2_size = 2
output_size = 1
tasa_aprendizaje = 0.1

# Inicialización de pesos (pequeños valores aleatorios)
def random_matrix(rows, cols):
    return [[random.uniform(-1, 1) for _ in range(cols)] for _ in range(rows)]

W1 = random_matrix(hidden1_size, input_size)
W2 = random_matrix(hidden2_size, hidden1_size)
W3 = random_matrix(output_size, hidden2_size)

# Sesgos
b1 = [0.0] * hidden1_size
b2 = [0.0] * hidden2_size
b3 = [0.0] * output_size

# -----------------------------
# Funciones de red
# -----------------------------
def forward(x):
    # Capa 1
    z1 = [sum(W1[i][j]*x[j] for j in range(input_size)) + b1[i] for i in range(hidden1_size)]
    a1 = [sigmoid(z) for z in z1]
    # Capa 2
    z2 = [sum(W2[i][j]*a1[j] for j in range(hidden1_size)) + b2[i] for i in range(hidden2_size)]
    a2 = [sigmoid(z) for z in z2]
    # Salida
    z3 = [sum(W3[i][j]*a2[j] for j in range(hidden2_size)) + b3[i] for i in range(output_size)]
    a3 = [sigmoid(z) for z in z3]
    return (a1, a2, a3, z1, z2, z3)

# -----------------------------
# Entrenamiento con Backpropagation
# -----------------------------
for epoca in range(1000):
    error_total = 0
    for x, y in datos:
        # FORWARD
        a1, a2, a3, z1, z2, z3 = forward(x)
        salida = a3[0]
        error = y[0] - salida
        error_total += error**2

        # BACKWARD
        # Derivadas
        delta3 = [error * derivada_sigmoid(z3[0])]
        delta2 = [delta3[0] * W3[0][i] * derivada_sigmoid(z2[i]) for i in range(hidden2_size)]
        delta1 = []
        for i in range(hidden1_size):
            suma = 0
            for j in range(hidden2_size):
                suma += delta2[j] * W2[j][i]
            delta1.append(suma * derivada_sigmoid(z1[i]))

        # Actualización de pesos y sesgos
        for i in range(output_size):
            for j in range(hidden2_size):
                W3[i][j] += tasa_aprendizaje * delta3[i] * a2[j]
            b3[i] += tasa_aprendizaje * delta3[i]

        for i in range(hidden2_size):
            for j in range(hidden1_size):
                W2[i][j] += tasa_aprendizaje * delta2[i] * a1[j]
            b2[i] += tasa_aprendizaje * delta2[i]

        for i in range(hidden1_size):
            for j in range(input_size):
                W1[i][j] += tasa_aprendizaje * delta1[i] * x[j]
            b1[i] += tasa_aprendizaje * delta1[i]

    # Mostrar progreso cada 200 épocas
    if epoca % 200 == 0:
        print(f"Época {epoca}: Error total = {error_total:.4f}")

# -----------------------------
# Evaluación
# -----------------------------
print("\n=== PRUEBA DE LA RED ===")
puntos_prueba = [
    [1,1],
    [4,4],
    [2,2],
    [3.5,3.5]
]

for p in puntos_prueba:
    _, _, salida, _, _, _ = forward(p)
    print(f"Punto {p} -> salida = {salida[0]:.3f}")
