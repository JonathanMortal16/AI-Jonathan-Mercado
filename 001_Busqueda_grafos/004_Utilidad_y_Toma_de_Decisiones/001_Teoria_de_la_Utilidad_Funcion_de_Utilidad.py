# 1) Definimos las utilidades de los posibles resultados
#    Nota: estos valores son inventados para el ejemplo.
utilidad_resultado = {
    "llego_rapido_sano": 100,   # wow, cliente feliz, bono
    "robot_danado":    -200,    # carísimo reparar
    "llego_lento_ok":   40      # llegaste bien, normal
}

# 2) Definimos las acciones y sus posibles resultados con probabilidades
#    Formato:
#    acciones["NombreAccion"] = [
#        ("nombre_resultado", probabilidad_de_ese_resultado),
#        ...
#    ]
acciones = {
    "ruta_rapida_peligrosa": [
        ("llego_rapido_sano", 0.70),
        ("robot_danado",      0.30)
    ],
    "ruta_lenta_segura": [
        ("llego_lento_ok",    1.00)
    ]
}

def utilidad_esperada(accion, modelo_acciones, tabla_utilidad):
    """
    Calcula la utilidad esperada de una acción.
    EU(A) = sumatoria[ P(resultado|A) * U(resultado) ]
    """
    suma = 0.0
    for resultado, prob in modelo_acciones[accion]:
        u = tabla_utilidad[resultado]  # utilidad numérica de ese resultado
        suma += prob * u
    return suma

# 3) Calculamos la utilidad esperada para cada acción
for nombre_accion in acciones:
    ue = utilidad_esperada(nombre_accion, acciones, utilidad_resultado)
    print(f"Acción: {nombre_accion}")
    print(f"  Utilidad esperada = {ue}")
    print()

# 4) Elegimos la mejor acción automáticamente
mejor_accion = None
mejor_utilidad = None

for nombre_accion in acciones:
    ue = utilidad_esperada(nombre_accion, acciones, utilidad_resultado)
    if (mejor_utilidad is None) or (ue > mejor_utilidad):
        mejor_utilidad = ue
        mejor_accion = nombre_accion

print("=====================================")
print(f"La mejor decisión es: {mejor_accion}")
print(f"Con utilidad esperada: {mejor_utilidad}")
print("=====================================")
