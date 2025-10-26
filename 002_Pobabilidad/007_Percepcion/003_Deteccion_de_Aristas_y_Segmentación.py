import cv2
import numpy as np

# ---------------------------------------------------------
# 1. Cargar imagen en escala de grises
# ---------------------------------------------------------
imagen = cv2.imread(r"C:\Users\zenso\OneDrive\Escritorio\Escuela\6to semesttre\Inteligencia Artificial\codes\IA-Jonathan-Mercado\AI-Jonathan-Mercado\002_Pobabilidad\007_Percepcion\img\panda.jpg", cv2.IMREAD_GRAYSCALE)

if imagen is None:
    raise FileNotFoundError("No se pudo leer la imagen. ¿Está en la misma carpeta?")

# ---------------------------------------------------------
# 2. Detección de bordes con Sobel
# ---------------------------------------------------------
# Sobel calcula el cambio (gradiente) en X y en Y.
sobel_x = cv2.Sobel(imagen, cv2.CV_64F, 1, 0, ksize=3)  # derivada en X
sobel_y = cv2.Sobel(imagen, cv2.CV_64F, 0, 1, ksize=3)  # derivada en Y

# Magnitud del gradiente = fuerza del borde
magnitud_sobel = cv2.magnitude(sobel_x, sobel_y)

# Convertimos la magnitud a rango visible (0-255, tipo uint8)
sobel_norm = cv2.normalize(magnitud_sobel, None, 0, 255, cv2.NORM_MINMAX)
sobel_norm = sobel_norm.astype(np.uint8)

# ---------------------------------------------------------
# 3. Detección de bordes con Canny (clásico en visión)
# ---------------------------------------------------------
# Canny hace:
#  - suavizado gaussiano
#  - gradiente
#  - suprime bordes débiles que no son reales
#  - conexión por histéresis
bordes_canny = cv2.Canny(imagen, 100, 200)

# ---------------------------------------------------------
# 4. Segmentación por umbral (threshold)
# ---------------------------------------------------------
# Idea: separar "objeto" (brilloso) del "fondo" (oscuro).
# threshold fija un corte en intensidad.
ret, segmentada = cv2.threshold(
    imagen,        # imagen original en gris
    127,           # umbral (0-255). 127 ~ gris medio
    255,           # valor que se asigna a "objeto"
    cv2.THRESH_BINARY
)

# También podemos hacer Otsu, que calcula el mejor umbral automáticamente:
ret_otsu, segmentada_otsu = cv2.threshold(
    imagen,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)
# segmentada_otsu intenta separar fondo/objeto sin que tú elijas 127 a mano.

# ---------------------------------------------------------
# 5. Mostrar resultados (solo funciona si tu OpenCV tiene GUI)
# ---------------------------------------------------------
cv2.imshow("Original (Gris)", imagen)
cv2.imshow("Bordes Sobel", sobel_norm)
cv2.imshow("Bordes Canny", bordes_canny)
cv2.imshow("Segmentacion (umbral fijo=127)", segmentada)
cv2.imshow("Segmentacion (Otsu auto)", segmentada_otsu)

print("Umbral Otsu elegido automáticamente:", ret_otsu)

cv2.waitKey(0)
cv2.destroyAllWindows()
