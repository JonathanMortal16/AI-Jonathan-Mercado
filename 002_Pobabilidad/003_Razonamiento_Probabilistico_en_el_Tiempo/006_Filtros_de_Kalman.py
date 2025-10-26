# Matrices del modelo (A, H, etc.)
dt = 1.0  # intervalo de tiempo

# Matriz de transición A
A = [
    [1, dt],
    [0, 1]
]

# Matriz de control B (no hay control externo en este ejemplo)
B = [
    [0],
    [0]
]

# Matriz de observación H (solo medimos posición)
H = [[1, 0]]

# Ruido del proceso (modelo)
Q = [
    [0.001, 0],
    [0, 0.001]
]

# Ruido de medición (sensor)
R = [[0.1]]

# Matriz identidad (2x2)
I = [
    [1, 0],
    [0, 1]
]

# Estado inicial
x = [[0],   # posición
     [1]]   # velocidad

# Covarianza inicial (incertidumbre)
P = [
    [1, 0],
    [0, 1]
]

# Mediciones simuladas (posiciones observadas con ruido)
mediciones = [1.2, 2.8, 4.5, 6.1, 8.2, 10.0, 11.7]

# ------------------------------------------------------------
# Funciones auxiliares para multiplicación de matrices pequeñas
# ------------------------------------------------------------
def matmul(A, B):
    """Multiplicación de matrices 2D"""
    res = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                res[i][j] += A[i][k] * B[k][j]
    return res

def transpose(A):
    """Transpuesta"""
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def add(A, B):
    """Suma de matrices"""
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def sub(A, B):
    """Resta de matrices"""
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def inv1x1(a):
    """Inversa para matriz 1x1"""
    return [[1 / a[0][0]]]

def scalar_mul(A, s):
    """Multiplicar matriz por escalar"""
    return [[A[i][j] * s for j in range(len(A[0]))] for i in range(len(A))]

# ------------------------------------------------------------
# Filtro de Kalman
# ------------------------------------------------------------
print("=== FILTRO DE KALMAN ===\n")
for k, z in enumerate(mediciones):
    # ---- PREDICCIÓN ----
    x_pred = matmul(A, x)
    P_pred = add(matmul(A, matmul(P, transpose(A))), Q)

    # ---- ACTUALIZACIÓN ----
    z_mat = [[z]]  # convertir medición a matriz

    # Residuo (innovación)
    y = sub(z_mat, matmul(H, x_pred))

    # Ganancia de Kalman
    S = add(matmul(H, matmul(P_pred, transpose(H))), R)
    K = matmul(P_pred, matmul(transpose(H), inv1x1(S)))

    # Nueva estimación
    x = add(x_pred, matmul(K, y))

    # Nueva covarianza
    KH = matmul(K, H)
    IKH = sub(I, KH)
    P = matmul(IKH, P_pred)

    # ---- RESULTADOS ----
    print(f"Medición {k+1}: {z:.2f}")
    print(f"  Posición estimada: {x[0][0]:.3f}")
    print(f"  Velocidad estimada: {x[1][0]:.3f}")
    print("--------------------------------------------------")
