import cv2
import numpy as np

# ---------------------------------------------------------
# 1. Cargar imagen en escala de grises
# ---------------------------------------------------------
# Cambia "panda.jpg" por la imagen que quieras analizar.
img_gray = cv2.imread(r"C:\Users\zenso\OneDrive\Escritorio\Escuela\6to semesttre\Inteligencia Artificial\codes\IA-Jonathan-Mercado\AI-Jonathan-Mercado\002_Pobabilidad\007_Percepcion\panda_panzon.webp", cv2.IMREAD_GRAYSCALE)
if img_gray is None:
    raise FileNotFoundError("⚠ No se pudo leer la imagen. Asegúrate que está en la misma carpeta.")

# ---------------------------------------------------------
# 2. Suavizar un poco para reducir ruido
# ---------------------------------------------------------
img_blur = cv2.GaussianBlur(img_gray, (5,5), 0)

# ---------------------------------------------------------
# 3. Segmentar: objeto vs fondo (umbral)
# ---------------------------------------------------------

_, img_bin = cv2.threshold(
    img_blur,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)


white_ratio = np.mean(img_bin)  # cuánta parte está blanca
if white_ratio < 0.5:
    # si hay muy poco blanco, probablemente el objeto está negro
    img_bin = 255 - img_bin

# ---------------------------------------------------------
# 4. Encontrar contornos (posibles objetos)
# ---------------------------------------------------------
# cv2.findContours encuentra las "manchas blancas"
contours, hierarchy = cv2.findContours(
    img_bin,
    cv2.RETR_EXTERNAL,      # solo contornos externos
    cv2.CHAIN_APPROX_SIMPLE # compresión de puntos
)

# Vamos a hacer una copia en color para dibujar resultados
img_color = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

objetos_detectados = []

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 100:  
        # Muy pequeño -> probablemente ruido, lo ignoramos
        continue

    # bounding box del contorno
    x, y, w, h = cv2.boundingRect(cnt)

    # Relación de aspecto
    aspecto = w / float(h)

    # Clasificación súper básica por forma
    # (Esto es una heurística: tú la puedes cambiar según tu práctica)
    if 0.8 <= aspecto <= 1.2:
        clase = "bloque/cuadrado"
    elif aspecto > 1.2:
        clase = "barra horizontal"
    else:
        clase = "barra vertical"

    # Guardar info del objeto
    objetos_detectados.append({
        "area": area,
        "bbox": (x, y, w, h),
        "aspecto": aspecto,
        "clase": clase
    })

    # Dibujar el recuadro y el texto en la imagen de salida
    cv2.rectangle(img_color, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(
        img_color,
        clase,
        (x, y-5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 0),
        1,
        cv2.LINE_AA
    )

# ---------------------------------------------------------
# 5. Mostrar resultados
# ---------------------------------------------------------
print("Objetos detectados:")
for obj in objetos_detectados:
    print(f"- Clase: {obj['clase']}")
    print(f"  Área: {obj['area']:.1f} px")
    print(f"  BBox: {obj['bbox']}")
    print(f"  Aspecto (w/h): {obj['aspecto']:.2f}")
    print("")

cv2.imshow("Imagen original (gris)", img_gray)
cv2.imshow("Binaria / Segmentada", img_bin)
cv2.imshow("Reconocimiento (etiquetado)", img_color)

cv2.waitKey(0)
cv2.destroyAllWindows()
