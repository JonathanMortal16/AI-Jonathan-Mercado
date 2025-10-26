# =====================================================
# Separabilidad Lineal en 2D: AND vs XOR
# =====================================================

import random
import numpy as np
import matplotlib.pyplot as plt

class Perceptron:
    def __init__(self, num_inputs, lr=0.1):
        self.weights = np.random.uniform(-1, 1, num_inputs)
        self.bias = random.uniform(-1, 1)
        self.lr = lr

    def activation(self, x):
        return 1 if x >= 0 else 0

    def predict(self, inputs):
        total = np.dot(self.weights, inputs) + self.bias
        return self.activation(total)

    def train(self, X, y, epochs=20):
        for _ in range(epochs):
            for xi, target in zip(X, y):
                pred = self.predict(xi)
                error = target - pred
                # regla de aprendizaje del perceptrón
                self.weights += self.lr * error * xi
                self.bias += self.lr * error

# ---------------------------
# Dataset AND (sí separable)
# ---------------------------
X_and = np.array([[0,0],[0,1],[1,0],[1,1]])
y_and = np.array([0,0,0,1])

per_and = Perceptron(num_inputs=2, lr=0.1)
per_and.train(X_and, y_and, epochs=20)

# ---------------------------
# Dataset XOR (no separable)
# ---------------------------
X_xor = np.array([[0,0],[0,1],[1,0],[1,1]])
y_xor = np.array([0,1,1,0])

per_xor = Perceptron(num_inputs=2, lr=0.1)
per_xor.train(X_xor, y_xor, epochs=20)

# ---------------------------
# Función para graficar resultados
# ---------------------------
def plot_dataset_and_boundary(X, y, model, title):
    # Graficar puntos
    for point, label in zip(X, y):
        if label == 0:
            plt.scatter(point[0], point[1], marker='o', label='Clase 0', edgecolors='black', facecolor='white')
        else:
            plt.scatter(point[0], point[1], marker='s', label='Clase 1', edgecolors='black', facecolor='gray')

    # Intentar graficar la frontera: w1*x + w2*y + b = 0 -> y = (-b - w1*x)/w2
    w1, w2 = model.weights
    b = model.bias

    if abs(w2) > 1e-6:  # evitar división entre cero
        xs = np.linspace(-0.5, 1.5, 50)
        ys = [(-b - w1*x)/w2 for x in xs]
        plt.plot(xs, ys, label='Frontera (perceptrón)')
    else:
        # frontera vertical x = constante
        if abs(w1) > 1e-6:
            x_const = -b / w1
            plt.axvline(x_const, label='Frontera (perceptrón)')

    plt.title(title)
    plt.xlim(-0.5, 1.5)
    plt.ylim(-0.5, 1.5)
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.grid(True)
    # evitar duplicados en la leyenda
    handles, labels = plt.gca().get_legend_handles_labels()
    uniq = dict(zip(labels, handles))
    plt.legend(uniq.values(), uniq.keys())

    plt.show()

# Graficar AND
plot_dataset_and_boundary(X_and, y_and, per_and, "AND: separable linealmente")

# Graficar XOR
plot_dataset_and_boundary(X_xor, y_xor, per_xor, "XOR: NO separable linealmente")
