# =============================================
# ADALINE: Neurona adaptativa lineal
# =============================================

import numpy as np

class Adaline:
    def __init__(self, num_inputs, lr=0.01):
        self.weights = np.random.uniform(-1, 1, num_inputs)
        self.bias = np.random.uniform(-1, 1)
        self.lr = lr

    def net_input(self, X):
        """Entrada neta (sin función escalón)"""
        return np.dot(X, self.weights) + self.bias

    def activation(self, X):
        """Identidad (lineal)"""
        return X

    def train(self, X, y, epochs=20):
        for epoch in range(epochs):
            net = self.net_input(X)
            output = self.activation(net)
            errors = y - output
            # Regla de Widrow-Hoff (descenso de gradiente)
            self.weights += self.lr * X.T.dot(errors)
            self.bias += self.lr * errors.sum()
            mse = (errors**2).mean()
            print(f"Época {epoch+1} | Error cuadrático medio: {mse:.4f}")

    def predict(self, X):
        return np.where(self.net_input(X) >= 0.0, 1, 0)

# Entrenamiento con AND
X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([0,0,0,1])

a = Adaline(num_inputs=2, lr=0.05)
a.train(X, y)

print("\nPruebas ADALINE:")
for xi in X:
    print(f"{xi} -> {a.predict(xi)}")
