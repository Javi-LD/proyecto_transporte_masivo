"""
Sistema inteligente de rutas - TransMilenio Bogotá
---------------------------------------------------
Modelo académico simplificado de estaciones, conexiones y troncales.

Importante: los tiempos y algunas conexiones son estimados. No representan
información oficial ni tiempos reales del sistema TransMilenio.

El costo de una ruta se calcula así:

    costo = tiempo de recorrido + penalización por cada transbordo

El grafo se considera bidireccional para simplificar el ejercicio.
"""

from collections import defaultdict
import heapq
import unicodedata


# Cada hecho tiene la forma:
# (estación_origen, estación_destino, troncal, tiempo_en_minutos)
HECHOS_CONEXION = [
    # Troncal Caracas Sur
    ("Portal Usme", "Santa Librada", "Caracas Sur", 4),
    ("Santa Librada", "Molinos", "Caracas Sur", 4),
    ("Molinos", "Consuelo", "Caracas Sur", 3),
    ("Consuelo", "Socorro", "Caracas Sur", 3),
    ("Socorro", "Olaya", "Caracas Sur", 4),

    # Troncal Caracas
    ("Olaya", "Restrepo", "Caracas", 3),
    ("Restrepo", "Nariño", "Caracas", 3),
    ("Nariño", "Hospital", "Caracas", 3),
    ("Hospital", "Avenida Jiménez", "Caracas", 5),
    ("Avenida Jiménez", "Calle 26", "Caracas", 4),
    ("Calle 26", "Marly", "Caracas", 4),

    # Troncal Autopista Norte
    ("Portal Norte", "Toberín", "Autopista Norte", 4),
    ("Toberín", "Pepe Sierra", "Autopista Norte", 4),
    ("Pepe Sierra", "Calle 100", "Autopista Norte", 4),
    ("Calle 100", "Calle 85", "Autopista Norte", 4),
    ("Calle 85", "Héroes", "Autopista Norte", 3),
    ("Héroes", "Calle 76", "Autopista Norte", 3),

    # Troncal NQS (modelo simplificado)
    ("Calle 26", "Avenida El Dorado", "NQS", 4),
    ("Avenida El Dorado", "Universidades", "NQS", 4),
    ("Universidades", "Avenida Chile", "NQS", 5),
    ("Avenida Chile", "La Castellana", "NQS", 5),

    # Conexiones especiales del modelo académico.
    # No se repiten conexiones que ya están representadas arriba.
    ("Avenida Jiménez", "Universidades", "Conexión", 5),
]

PENALIZACION_TRANSBORDO = 5


def normalizar(texto):
    """Permite comparar nombres sin distinguir mayúsculas ni tildes."""
    texto = unicodedata.normalize("NFD", texto.strip().casefold())
    return "".join(
        caracter for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )


def construir_grafo(hechos):
    """Construye un grafo bidireccional a partir de los hechos."""
    grafo = defaultdict(list)

    for origen, destino, troncal, tiempo in hechos:
        if tiempo <= 0:
            raise ValueError(
                f"El tiempo debe ser positivo: {origen} -> {destino}"
            )

        grafo[origen].append((destino, troncal, tiempo))
        # Regla de simetría: si A conecta con B, B conecta con A.
        grafo[destino].append((origen, troncal, tiempo))

    return grafo


def buscar_estacion(grafo, nombre):
    """Devuelve el nombre oficial de una estación escrita por el usuario."""
    buscada = normalizar(nombre)

    for estacion in grafo:
        if normalizar(estacion) == buscada:
            return estacion

    return None


def mejor_ruta(grafo, origen, destino):
    """Encuentra la ruta de menor costo mediante Dijkstra."""
    origen_real = buscar_estacion(grafo, origen)
    destino_real = buscar_estacion(grafo, destino)

    if origen_real is None:
        raise ValueError(f"La estación de origen '{origen}' no existe.")
    if destino_real is None:
        raise ValueError(f"La estación de destino '{destino}' no existe.")

    if origen_real == destino_real:
        return 0, [], 0

    # (costo, estación, troncal_actual, camino, transbordos)
    cola = [(0, origen_real, None, [], 0)]
    mejor_costo = {}

    while cola:
        costo, actual, troncal_actual, camino, transbordos = heapq.heappop(cola)
        estado = (actual, troncal_actual)

        if estado in mejor_costo and mejor_costo[estado] <= costo:
            continue
        mejor_costo[estado] = costo

        if actual == destino_real:
            return costo, camino, transbordos

        for vecino, troncal, tiempo in grafo[actual]:
            es_transbordo = (
                troncal_actual is not None and troncal != troncal_actual
            )
            nuevo_costo = costo + tiempo
            nuevos_transbordos = transbordos

            if es_transbordo:
                nuevo_costo += PENALIZACION_TRANSBORDO
                nuevos_transbordos += 1

            nuevo_camino = camino + [
                (actual, vecino, troncal, tiempo, es_transbordo)
            ]

            heapq.heappush(
                cola,
                (
                    nuevo_costo,
                    vecino,
                    troncal,
                    nuevo_camino,
                    nuevos_transbordos,
                ),
            )

    return None, None, None


def mostrar_estaciones(grafo):
    print("\nESTACIONES DISPONIBLES")
    print("-" * 40)
    for estacion in sorted(grafo):
        print(f"- {estacion}")


def explicar_ruta(origen, destino, costo, pasos, transbordos):
    if pasos is None:
        print(f"\nNo existe una ruta entre '{origen}' y '{destino}'.")
        return

    print("\n" + "=" * 70)
    print("RUTA RECOMENDADA - TRANSMILENIO")
    print("=" * 70)
    print(f"Origen: {origen}")
    print(f"Destino: {destino}")
    print(f"Costo total estimado: {costo} minutos")
    print(f"Transbordos: {transbordos}")

    if not pasos:
        print("\nEl origen y el destino son la misma estación.")
        return

    print("\nRecorrido:")
    for numero, (estacion_a, estacion_b, troncal, tiempo, es_transbordo) in enumerate(pasos, 1):
        if es_transbordo:
            print("  -> TRANSBORDO")
        print(
            f"  {numero}. {estacion_a} "
            f"--[{troncal}, {tiempo} min]--> {estacion_b}"
        )

    print("\n" + "-" * 70)
    print(f"Total de tramos: {len(pasos)}")
    print(f"Troncales utilizadas: {len({paso[2] for paso in pasos})}")
    print("=" * 70)


def main():
    grafo = construir_grafo(HECHOS_CONEXION)

    print("=" * 70)
    print("SISTEMA INTELIGENTE DE RUTAS - TRANSMILENIO BOGOTÁ")
    print("=" * 70)
    print("Modelo académico; no es información oficial ni en tiempo real.")

    mostrar_estaciones(grafo)

    origen = input("\nIngrese la estación de origen: ")
    destino = input("Ingrese la estación de destino: ")

    try:
        origen_real = buscar_estacion(grafo, origen)
        destino_real = buscar_estacion(grafo, destino)
        costo, pasos, transbordos = mejor_ruta(grafo, origen, destino)
        explicar_ruta(
            origen_real,
            destino_real,
            costo,
            pasos,
            transbordos,
        )
    except ValueError as error:
        print(f"\nERROR: {error}")


if __name__ == "__main__":
    main()
