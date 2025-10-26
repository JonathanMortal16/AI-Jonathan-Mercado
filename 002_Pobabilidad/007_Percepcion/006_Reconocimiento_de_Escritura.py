import cv2
import numpy as np

# ---------------------------------------------------------
# 1. Cargar imagen y preprocesar
# ---------------------------------------------------------
imagen = cv2.imread(r"C:\Users\zenso\OneDrive\Escritorio\Escuela\6to semesttre\Inteligencia Artificial\codes\IA-Jonathan-Mercado\AI-Jonathan-Mercado\002_Pobabilidad\007_Percepcion\texto_pandar.jpg", cv2.IMREAD_GRAYSCALE)

if imagen is None:
    raise FileNotFoundError("⚠ No se encontró la imagen. Colócala en la misma carpeta que el script.")

# Reducir ruido y binarizar
blur = cv2.GaussianBlur(imagen, (3, 3), 0)
_, binaria = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# ---------------------------------------------------------
# 2. Encontrar contornos (cada símbolo o carácter)
# ---------------------------------------------------------
contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Ordenar los contornos de izquierda a derecha
contornos = sorted(contornos, key=lambda c: cv2.boundingRect(c)[0])

# Copia a color para mostrar resultados
color = cv2.cvtColor(imagen, cv2.COLOR_GRAY2BGR)

# ---------------------------------------------------------
# 3. Recortar y mostrar cada carácter detectado
# ---------------------------------------------------------
for i, contorno in enumerate(contornos):
    x, y, w, h = cv2.boundingRect(contorno)

    # Filtrar posibles ruidos
    if w < 10 or h < 10:
        continue

    # Dibujar cuadro alrededor del carácter
    cv2.rectangle(color, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Extraer el carácter como ROI (región de interés)
    caracter = binaria[y:y + h, x:x + w]

    # Redimensionar a 28x28 (como el dataset MNIST)
    caracter_redim = cv2.resize(caracter, (28, 28), interpolation=cv2.INTER_AREA)

    # Mostrar el carácter (para revisión visual)
    cv2.imshow(f"Caracter {i+1}", caracter_redim)

# ---------------------------------------------------------
# 4. Mostrar imagen con todos los cuadros detectados
# ---------------------------------------------------------
cv2.imshow("Original", imagen)
cv2.imshow("Binaria", binaria)
cv2.imshow("Deteccion de caracteres", color)

print(f"Se detectaron {len(contornos)} posibles caracteres.")

cv2.waitKey(0)
cv2.destroyAllWindows()
