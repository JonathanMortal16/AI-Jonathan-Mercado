import cv2
import numpy as np

frame1 = cv2.imread(r"C:\Users\zenso\OneDrive\Escritorio\Escuela\6to semesttre\Inteligencia Artificial\codes\IA-Jonathan-Mercado\AI-Jonathan-Mercado\002_Pobabilidad\007_Percepcion\img\panda1.png", cv2.IMREAD_GRAYSCALE)
frame2 =  cv2.imread(r"C:\Users\zenso\OneDrive\Escritorio\Escuela\6to semesttre\Inteligencia Artificial\codes\IA-Jonathan-Mercado\AI-Jonathan-Mercado\002_Pobabilidad\007_Percepcion\img\panda2.png", cv2.IMREAD_GRAYSCALE)

if frame1 is None or frame2 is None:
    raise FileNotFoundError("⚠ No se pudieron cargar frame1.jpg y/o frame2.jpg.")

# 🔧 Corregir tamaños
h = min(frame1.shape[0], frame2.shape[0])
w = min(frame1.shape[1], frame2.shape[1])
frame1 = cv2.resize(frame1, (w, h))
frame2 = cv2.resize(frame2, (w, h))

# Suavizar para reducir ruido
blur1 = cv2.GaussianBlur(frame1, (5,5), 0)
blur2 = cv2.GaussianBlur(frame2, (5,5), 0)

# Diferencia
diff = cv2.absdiff(blur2, blur1)

# Umbral: quedarnos solo con diferencias grandes (zonas que cambiaron mucho)
_, diff_bin = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

# Opcional: dilatar para unir manchas y hacerlas más sólidas
kernel = np.ones((5,5), np.uint8)
diff_bin = cv2.dilate(diff_bin, kernel, iterations=2)

# ---------------------------------------------------------
# 3. Encontrar las regiones que se movieron (contornos)
# ---------------------------------------------------------
contours, _ = cv2.findContours(diff_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Convertimos frame2 a color para dibujar encima
frame2_color = cv2.cvtColor(frame2, cv2.COLOR_GRAY2BGR)

movimientos_detectados = 0

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 200:
        # ignorar ruido muy pequeño
        continue

    movimientos_detectados += 1

    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(frame2_color, (x,y), (x+w,y+h), (0,0,255), 2)
    cv2.putText(
        frame2_color,
        "MOVIMIENTO",
        (x, y-5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0,0,255),
        1,
        cv2.LINE_AA
    )

print(f"Objetos en movimiento detectados: {movimientos_detectados}")

# ---------------------------------------------------------
# 4. Mostrar resultados
# ---------------------------------------------------------
cv2.imshow("Frame t", frame1)
cv2.imshow("Frame t+1", frame2)
cv2.imshow("Diferencia Absoluta", diff)
cv2.imshow("Zonas de Movimiento (binario)", diff_bin)
cv2.imshow("Deteccion de Movimiento", frame2_color)

cv2.waitKey(0)
cv2.destroyAllWindows()
