import cv2
import numpy as np
import math

# ---------------------------------------------------------
# 1. Cargar imagen y preprocesar
# ---------------------------------------------------------
# Usa una imagen con líneas claras (bordes definidos).
img = cv2.imread(r"C:\Users\zenso\OneDrive\Escritorio\Escuela\6to semesttre\Inteligencia Artificial\codes\IA-Jonathan-Mercado\AI-Jonathan-Mercado\002_Pobabilidad\007_Percepcion\img\panda.jpg", cv2.IMREAD_GRAYSCALE)

if img is None:
    raise FileNotFoundError("No se encontró la imagen. Colócala en la misma carpeta que el script.")

# Suavizado para reducir ruido
blur = cv2.GaussianBlur(img, (5,5), 0)

# Detectar bordes (Canny)
edges = cv2.Canny(blur, 50, 150, apertureSize=3)

# ---------------------------------------------------------
# 2. Detección de líneas con Transformada de Hough Probabilística
# ---------------------------------------------------------
lineas = cv2.HoughLinesP(
    edges,
    rho=1,
    theta=np.pi / 180,
    threshold=50,
    minLineLength=40,
    maxLineGap=10
)

# Convertimos a color para dibujar líneas
img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

# ---------------------------------------------------------
# 3. Clasificación / Etiquetado de líneas
# ---------------------------------------------------------
def clasificar_linea(x1, y1, x2, y2):
    # Calcular ángulo en grados
    dx = x2 - x1
    dy = y2 - y1
    angulo = math.degrees(math.atan2(dy, dx))
    if angulo < 0:
        angulo += 180  # normalizamos a [0,180)

    # Clasificar por orientación
    if abs(angulo - 0) <= 10 or abs(angulo - 180) <= 10:
        etiqueta = "Horizontal"
        color = (0, 255, 0)  # verde
    elif abs(angulo - 90) <= 10:
        etiqueta = "Vertical"
        color = (255, 0, 0)  # azul
    else:
        etiqueta = "Diagonal"
        color = (0, 0, 255)  # rojo

    return etiqueta, color, angulo

# Dibujar las líneas detectadas y etiquetadas
if lineas is not None:
    print(f"✅ Se detectaron {len(lineas)} líneas.")
    for linea in lineas:
        x1, y1, x2, y2 = linea[0]
        etiqueta, color, angulo = clasificar_linea(x1, y1, x2, y2)

        cv2.line(img_color, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            img_color,
            etiqueta,
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            color,
            1,
            cv2.LINE_AA
        )
        print(f"Línea ({x1},{y1})–({x2},{y2}) → {etiqueta} ({angulo:.1f}°)")
else:
    print("⚠ No se detectaron líneas.")

# ---------------------------------------------------------
# 4. Mostrar resultados
# ---------------------------------------------------------
cv2.imshow("Imagen original (gris)", img)
cv2.imshow("Bordes detectados (Canny)", edges)
cv2.imshow("Líneas etiquetadas", img_color)

cv2.waitKey(0)
cv2.destroyAllWindows()
