import random

# --- 1. Definir el entorno ----------------------------------

estados = ["A", "B", "C", "META"]
acciones = ["izq", "der"]

def transicion(estado, accion):
    """Simula el cambio de estado y devuelve (nuevo_estado, recompensa)."""
    if estado == "META":
        return "META", 0
    if accion == "der":
        if estado == "A": return "B", 0
        if estado == "B": return "C", 0
        if estado == "C": return "META", 10
    if accion == "izq":
        if estado == "C": return "B", 0
        if estado == "B": return "A", 0
        if estado == "A": return "A", 0
    return estado, 0


# --- 2. Parámetros del agente -------------------------------
gamma = 0.9  # factor de descuento
theta = 0.001  # umbral de convergencia

# Política inicial aleatoria
politica = {s: random.choice(acciones) for s in ["A", "B", "C"]}
# Valor inicial de cada estado
V = {s: 0.0 for s in estados}

def evaluar_politica():
    """Evalúa la política actual calculando V(s) hasta converger."""
    while True:
        delta = 0
        for s in ["A", "B", "C"]:
            a = politica[s]
            s_next, r = transicion(s, a)
            nuevo_valor = r + gamma * V[s_next]
            delta = max(delta, abs(nuevo_valor - V[s]))
            V[s] = nuevo_valor
        if delta < theta:
            break

def mejorar_politica():
    """Mejora la política actual según los valores V(s)."""
    estable = True
    for s in ["A", "B", "C"]:
        # Acción actual
        vieja_accion = politica[s]

        # Evaluar ambas acciones posibles
        valores_accion = {}
        for a in acciones:
            s_next, r = transicion(s, a)
            valores_accion[a] = r + gamma * V[s_next]

        # Elegir la mejor acción
        mejor_accion = max(valores_accion, key=valores_accion.get)
        politica[s] = mejor_accion

        if mejor_accion != vieja_accion:
            estable = False
    return estable


# --- 3. Iteración de Políticas -------------------------------
iteracion = 0
while True:
    iteracion += 1
    print(f"\n--- Iteración {iteracion} ---")
    evaluar_politica()
    estable = mejorar_politica()

    for s in ["A", "B", "C"]:
        print(f"V({s}) = {V[s]:.2f}, acción óptima: {politica[s]}")
    if estable:
        print("\n✅ Política estable: alcanzada la óptima.")
        break

# --- 4. Política final aprendida ------------------------------
print("\n====================================")
print("POLÍTICA FINAL:")
for s in ["A", "B", "C"]:
    print(f"  En estado {s} -> {politica[s]}")
print("====================================")
