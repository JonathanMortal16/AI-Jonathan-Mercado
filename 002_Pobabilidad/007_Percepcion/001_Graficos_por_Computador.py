import math

# ============================
# 1. Definimos un cubo en 3D
# ============================
# Un cubo centrado en el origen, de lado 2
# Cada punto es (X,Y,Z)
cube_vertices = [
    (-1, -1, -1),
    (-1, -1,  1),
    (-1,  1, -1),
    (-1,  1,  1),
    ( 1, -1, -1),
    ( 1, -1,  1),
    ( 1,  1, -1),
    ( 1,  1,  1)
]

# Conexiones entre vértices para dibujar las aristas del cubo
cube_edges = [
    (0,1), (0,2), (0,4),
    (7,6), (7,5), (7,3),
    (1,3), (1,5),
    (2,3), (2,6),
    (4,5), (4,6)
]

# ============================
# 2. Rotamos el cubo en 3D
# ============================
# Rotación simple para que no se vea plano.
# Rotación alrededor de los ejes X y Y.
def rotate_point(px, py, pz, angle_x, angle_y):
    # Rotar alrededor de X
    cosx = math.cos(angle_x)
    sinx = math.sin(angle_x)
    y1 = py * cosx - pz * sinx
    z1 = py * sinx + pz * cosx
    x1 = px

    # Rotar alrededor de Y
    cosy = math.cos(angle_y)
    siny = math.sin(angle_y)
    z2 = z1 * cosy - x1 * siny
    x2 = z1 * siny + x1 * cosy
    y2 = y1

    return x2, y2, z2

# ============================
# 3. Proyección en perspectiva 3D -> 2D
# ============================
# Cámara mirando hacia -Z
# f = distancia focal (qué tan "zoom" tiene la cámara)
f = 100  # escoger un valor grande para que se vea grandecito

def project_point(px, py, pz):
    # IMPORTANTE:
    # mientras más grande es pz, más lejos está.
    # pero si pz está cerca de 0 o positivo, puede quedar atrás de la cámara.
    #
    # Movemos el cubo un poco "al fondo" sumando un offset en z
    pz_camera = pz + 5  # alejamos el cubo 5 unidades hacia la cámara

    # Evitar división entre cero o negativo
    if pz_camera <= 0:
        return None  # punto detrás de la cámara, no se dibuja

    x2d = f * (px / pz_camera)
    y2d = f * (py / pz_camera)
    return (x2d, y2d)

# ============================
# 4. Convertir coords 2D a una "pantalla" ASCII
# ============================
WIDTH = 80
HEIGHT = 40

def draw_wireframe(angle_x, angle_y):
    # Creamos un lienzo en blanco
    canvas = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # Rotar y proyectar todos los vértices
    projected = []
    for (x, y, z) in cube_vertices:
        xr, yr, zr = rotate_point(x, y, z, angle_x, angle_y)
        p = project_point(xr, yr, zr)
        projected.append(p)

    # Función auxiliar: trazar una línea entre dos puntos proyectados en el canvas ASCII
    def draw_line(p1, p2):
        if p1 is None or p2 is None:
            return

        (x1, y1) = p1
        (x2, y2) = p2

        # Trasladar coords para que el centro quede en medio del canvas
        x1 = int(x1 + WIDTH/2)
        y1 = int(-y1 + HEIGHT/2)  # invertimos y porque en pantalla crece hacia abajo
        x2 = int(x2 + WIDTH/2)
        y2 = int(-y2 + HEIGHT/2)

        # Algoritmo de línea simple (Bresenham-ish pero flotante sencillo)
        steps = max(abs(x2 - x1), abs(y2 - y1), 1)
        for step in range(steps + 1):
            t = step / steps
            xi = int(x1 + t * (x2 - x1))
            yi = int(y1 + t * (y2 - y1))

            if 0 <= xi < WIDTH and 0 <= yi < HEIGHT:
                canvas[yi][xi] = "#"

    # Dibujar cada arista del cubo
    for (a, b) in cube_edges:
        draw_line(projected[a], projected[b])

    # Imprimir el canvas
    for row in canvas:
        print("".join(row))

# ============================
# 5. Ejecutar una vista del cubo
# ============================
# Escoge ángulos de rotación en radianes
angle_x = math.radians(25)  # rotar 25 grados sobre X
angle_y = math.radians(35)  # rotar 35 grados sobre Y

draw_wireframe(angle_x, angle_y)
