import numpy as np
import matplotlib.pyplot as plt

# ---------- Definición de funciones ----------
def escalon(x):
    """Función escalón: salida 1 si x >= 0, sino 0"""
    return np.where(x >= 0, 1, 0)

def sigmoide(x):
    """Función sigmoide (logística)"""
    return 1 / (1 + np.exp(-x))

def tanh(x):
    """Tangente hiperbólica"""
    return np.tanh(x)

def relu(x):
    """Rectified Linear Unit"""
    return np.maximum(0, x)

def leaky_relu(x, alpha=0.01):
    """Variante de ReLU con pendiente pequeña para x<0"""
    return np.where(x > 0, x, alpha * x)

# ---------- Generamos valores para graficar ----------
x = np.linspace(-6, 6, 200)

# Diccionario para recorrer fácilmente todas las funciones
funciones = {
    "Escalón": escalon(x),
    "Sigmoide": sigmoide(x),
    "Tanh": tanh(x),
    "ReLU": relu(x),
    "Leaky ReLU": leaky_relu(x)
}

# ---------- Graficamos ----------
plt.figure(figsize=(10, 8))
for i, (nombre, y) in enumerate(funciones.items(), 1):
    plt.subplot(3, 2, i)
    plt.plot(x, y)
    plt.title(nombre)
    plt.grid(True)
    plt.ylim(-1.5, 1.5)

plt.tight_layout()
plt.show()
