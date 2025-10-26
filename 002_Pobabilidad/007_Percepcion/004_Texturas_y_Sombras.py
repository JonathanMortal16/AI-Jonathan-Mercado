import cv2
import numpy as np

# ---------------------------------------------------------
# 1. Cargar imagen en escala de grises
# ---------------------------------------------------------
# IMPORTANTE:
# Cambia "panda.jpg" por la imagen que estés usando.
img = cv2.imread(r"C:\Users\zenso\OneDrive\Escritorio\Escuela\6to semesttre\Inteligencia Artificial\codes\IA-Jonathan-Mercado\AI-Jonathan-Mercado\002_Pobabilidad\007_Percepcion\panda_panzon.webp", cv2.IMREAD_GRAYSCALE)

if img is None:
    raise FileNotFoundError("⚠ No se pudo leer la imagen. ¿Está en la misma carpeta?")

# ---------------------------------------------------------
# 2. Estimar TEXTURA local
# ---------------------------------------------------------
win_size = 5  # ventana 5x5
media_local = cv2.blur(img, (win_size, win_size))

# Paso 2.2: calculamos promedio del cuadrado (para varianza)
cuadrado = img.astype(np.float32) ** 2
media_local_cuadrado = cv2.blur(cuadrado, (win_size, win_size))

# varianza = E[x^2] - (E[x])^2
var_local = media_local_cuadrado - (media_local.astype(np.float32) ** 2)

# desviación estándar local = sqrt(varianza), agregando clip por seguridad
std_local = np.sqrt(np.clip(var_local, 0, None))

# Normalizamos para poder verla como imagen 0-255
textura_mapa = cv2.normalize(std_local, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# ---------------------------------------------------------
# 3. Separar SOMBRA / ILUMINACIÓN vs DETALLE
# ---------------------------------------------------------
iluminacion_suave = cv2.GaussianBlur(img, (31, 31), 0)
# Nota: kernel 31x31 es grande a propósito, para quedarnos solo con cambios MUY suaves,
# que normalmente incluyen sombras generales.

detalle_alto = cv2.subtract(img, iluminacion_suave)

# Normalizamos para poder ver el "detalle"
detalle_alto_norm = cv2.normalize(detalle_alto, None, 0, 255, cv2.NORM_MINMAX)

# ---------------------------------------------------------
# 4. Mostrar resultados
# ---------------------------------------------------------
cv2.imshow("Original (gris)", img)
cv2.imshow("Mapa de Textura (desviacion local)", textura_mapa)
cv2.imshow("Iluminacion/Sombras (suave)", iluminacion_suave)
cv2.imshow("Detalle/Texture High-Freq", detalle_alto_norm)

cv2.waitKey(0)
cv2.destroyAllWindows()
