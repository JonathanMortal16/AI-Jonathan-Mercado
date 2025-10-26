# ============================================================
# Red Multicapa (MLP) para resolver el problema XOR
# ============================================================

import numpy as np

# -------------------------------
# Funciones de activación y derivadas
# -------------------------------
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)  # se aplica sobre la salida ya activada

# -------------------------------
# Datos de entrenamiento: XOR
# -------------------------------
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

# Salidas esperadas
y = np.array([
    [0],
    [1],
    [1],
    [0]
])

# -------------------------------
# Inicialización de parámetros
# -------------------------------
np.random.seed(1)  # para reproducibilidad

# 2 entradas → 2 neuronas ocultas
W1 = np.random.uniform(-1, 1, (2, 2))
b1 = np.zeros((1, 2))

# 2 neuronas ocultas → 1 neurona de salida
W2 = np.random.uniform(-1, 1, (2, 1))
b2 = np.zeros((1, 1))

learning_rate = 0.5
epochs = 10000

# -------------------------------
# Entrenamiento
# -------------------------------
for epoch in range(epochs):
    # ---- Propagación hacia adelante ----
    z1 = np.dot(X, W1) + b1
    a1 = sigmoid(z1)              # salida capa oculta
    z2 = np.dot(a1, W2) + b2
    a2 = sigmoid(z2)              # salida capa final (predicción)

    # ---- Cálculo del error ----
    error = y - a2

    # ---- Retropropagación ----
    d2 = error * sigmoid_derivative(a2)
    d1 = np.dot(d2, W2.T) * sigmoid_derivative(a1)

    # ---- Actualización de pesos y sesgos ----
    W2 += np.dot(a1.T, d2) * learning_rate
    b2 += np.sum(d2, axis=0, keepdims=True) * learning_rate
    W1 += np.dot(X.T, d1) * learning_rate
    b1 += np.sum(d1, axis=0, keepdims=True) * learning_rate

    # Mostrar progreso cada 1000 épocas
    if epoch % 1000 == 0:
        loss = np.mean(np.square(error))
        print(f"Época {epoch} | Error promedio: {loss:.6f}")

# -------------------------------
# Resultados finales
# -------------------------------
print("\nPruebas después del entrenamiento:")
for i in range(len(X)):
    print(f"Entrada: {X[i]} -> Predicción: {a2[i][0]:.4f}")
