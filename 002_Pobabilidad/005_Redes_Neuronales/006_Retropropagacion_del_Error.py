# ============================================================
# Retropropagación del Error - Red Multicapa (MLP)
# ============================================================

import numpy as np

# -------------------------------
# Funciones de activación
# -------------------------------
def sigmoid(x):
    """Función sigmoide"""
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    """Derivada de la sigmoide (se aplica sobre la salida activada)"""
    return x * (1 - x)

# -------------------------------
# Datos de entrenamiento (XOR)
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
# Inicialización aleatoria de pesos y sesgos
# -------------------------------
np.random.seed(42)
W1 = np.random.uniform(-1, 1, (2, 2))  # capa oculta
b1 = np.zeros((1, 2))
W2 = np.random.uniform(-1, 1, (2, 1))  # capa de salida
b2 = np.zeros((1, 1))

learning_rate = 0.5
epochs = 10000

# -------------------------------
# Entrenamiento con retropropagación
# -------------------------------
for epoch in range(epochs):
    # -------- FORWARD --------
    z1 = np.dot(X, W1) + b1          # Entrada * pesos + bias (capa 1)
    a1 = sigmoid(z1)                 # Activación capa oculta
    z2 = np.dot(a1, W2) + b2         # Salida capa oculta -> entrada capa salida
    a2 = sigmoid(z2)                 # Activación final (predicción)

    # -------- ERROR --------
    error = y - a2                   # Diferencia entre salida esperada y salida real
    loss = np.mean(np.square(error)) # Error cuadrático medio (MSE)

    # -------- BACKWARD --------
    # Derivadas (gradientes)
    d2 = error * sigmoid_derivative(a2)         # Gradiente capa de salida
    d1 = np.dot(d2, W2.T) * sigmoid_derivative(a1)  # Gradiente capa oculta

    # Actualización de pesos (descenso del gradiente)
    W2 += np.dot(a1.T, d2) * learning_rate
    b2 += np.sum(d2, axis=0, keepdims=True) * learning_rate
    W1 += np.dot(X.T, d1) * learning_rate
    b1 += np.sum(d1, axis=0, keepdims=True) * learning_rate

    # Mostrar progreso
    if epoch % 1000 == 0:
        print(f"Época {epoch} | Error promedio: {loss:.6f}")

# -------------------------------
# Resultados finales
# -------------------------------
print("\nPruebas después del entrenamiento:")
for i in range(len(X)):
    print(f"Entrada: {X[i]} -> Predicción: {a2[i][0]:.4f}")
