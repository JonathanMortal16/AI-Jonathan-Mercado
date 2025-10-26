import cv2
import numpy as np

# --------------------------------
# 1. Cargar imagen en escala de grises
# --------------------------------
# Puedes reemplazar "imagen.jpg" por la tuya
imagen = cv2.imread(r"C:\Users\zenso\OneDrive\Escritorio\Escuela\6to semesttre\Inteligencia Artificial\codes\IA-Jonathan-Mercado\AI-Jonathan-Mercado\002_Pobabilidad\007_Percepcion\panda.jpg", cv2.IMREAD_GRAYSCALE)

if imagen is None:
    raise FileNotFoundError("⚠️ No se encontró la imagen. Coloca una imagen en la misma carpeta.")

# --------------------------------
# 2. Aplicar distintos filtros
# --------------------------------

# a) Filtro Promedio (suavizado simple)
kernel_media = np.ones((3,3), np.float32) / 9
filtro_media = cv2.filter2D(imagen, -1, kernel_media)

# b) Filtro Gaussiano (suavizado más suave)
filtro_gauss = cv2.GaussianBlur(imagen, (5,5), 0)

# c) Filtro de Mediana (elimina ruido sal y pimienta)
filtro_mediana = cv2.medianBlur(imagen, 3)

# d) Filtro Sobel (resalta bordes horizontales y verticales)
sobel_x = cv2.Sobel(imagen, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(imagen, cv2.CV_64F, 0, 1, ksize=3)
filtro_sobel = cv2.magnitude(sobel_x, sobel_y)  # Magnitud del gradiente

# e) Filtro Laplaciano (detecta cambios abruptos)
filtro_laplaciano = cv2.Laplacian(imagen, cv2.CV_64F)

# --------------------------------
# 3. Mostrar resultados
# --------------------------------
cv2.imshow("Original", imagen)
cv2.imshow("Filtro Promedio", filtro_media)
cv2.imshow("Filtro Gaussiano", filtro_gauss)
cv2.imshow("Filtro Mediana", filtro_mediana)
cv2.imshow("Sobel (bordes)", filtro_sobel)
cv2.imshow("Laplaciano (bordes)", filtro_laplaciano)

cv2.waitKey(0)
cv2.destroyAllWindows()
