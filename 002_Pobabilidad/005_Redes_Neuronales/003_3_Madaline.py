# =============================================
# MADALINE: Dos capas de ADALINE para XOR
# =============================================

import numpy as np

class Madaline:
    def __init__(self, lr=0.1):
        # Capa oculta: 2 neuronas ADALINE
        self.W1 = np.random.uniform(-1, 1, (2, 2))
        self.b1 = np.random.uniform(-1, 1, 2)
        # Capa de salida: 1 neurona ADALINE
        self.W2 = np.random.uniform(-1, 1, (1, 2))
        self.b2 = np.random.uniform(-1, 1)
        self.lr = lr

    def activation(self, x):
        """Función escalón"""
        return np.where(x >= 0, 1, 0)

    def forward(self, X):
        """Propagación hacia adelante"""
        z1 = self.activation(np.dot(X, self.W1.T) + self.b1)
        z2 = self.activation(np.dot(z1, self.W2.T) + self.b2)
        return z1, z2

    def train(self, X, y, epochs=30):
        for epoch in range(epochs):
            total_error = 0
            for xi, target in zip(X, y):
                z1, z2 = self.forward(xi)
                error = target - z2
                total_error += abs(error)
                # Ajuste solo si hay error
                if error != 0:
                    self.W2 += self.lr * error * z1
                    self.b2 += self.lr * error
                    self.W1 += self.lr * error * np.outer(z1, xi)
                    self.b1 += self.lr * error
            print(f"Época {epoch+1} | Error total: {total_error}")

    def predict(self, X):
        _, z2 = self.forward(X)
        return z2

# Dataset XOR
X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([[0],[1],[1],[0]])

m = Madaline(lr=0.1)
m.train(X, y)

print("\nPruebas MADALINE (XOR):")
for xi in X:
    print(f"{xi} -> {m.predict(xi)}")
