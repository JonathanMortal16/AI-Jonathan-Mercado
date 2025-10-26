import itertools

# Jugadores
jugadores = ["A", "B"]

# Estrategias posibles
estrategias = ["Cooperar", "Traicionar"]

# Matrices de utilidad (U1 y U2)
# Cada tupla representa (utilidad_A, utilidad_B)
utilidad = {
    ("Cooperar", "Cooperar"): (-1, -1),
    ("Cooperar", "Traicionar"): (-10, 0),
    ("Traicionar", "Cooperar"): (0, -10),
    ("Traicionar", "Traicionar"): (-5, -5)
}

def es_equilibrio_nash(a_A, a_B):
    """Verifica si (a_A, a_B) es un equilibrio de Nash."""
    # Utilidades actuales
    uA_actual, uB_actual = utilidad[(a_A, a_B)]
    
    # Verificamos si A o B mejorarían al cambiar su acción
    for aA_alt in estrategias:
        if utilidad[(aA_alt, a_B)][0] > uA_actual:
            return False
    for aB_alt in estrategias:
        if utilidad[(a_A, aB_alt)][1] > uB_actual:
            return False
    return True

# Buscamos equilibrios de Nash
equilibrios = []
for (aA, aB) in itertools.product(estrategias, estrategias):
    if es_equilibrio_nash(aA, aB):
        equilibrios.append((aA, aB))

print("=== Equilibrios de Nash encontrados ===")
for e in equilibrios:
    print(e)
