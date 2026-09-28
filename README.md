# Sistema Inteligente de Rutas - TransMilenio Bogotá

## 1. Descripción

Este proyecto implementa un sistema inteligente para encontrar rutas dentro de una representación simplificada del sistema TransMilenio de Bogotá.

El sistema utiliza una **base de conocimiento** formada por estaciones y conexiones entre ellas. A partir de esta información aplica reglas de inferencia y un algoritmo de búsqueda de costo mínimo para determinar una ruta entre una estación de origen y una estación de destino.

El algoritmo utilizado es **Dijkstra**, incorporando una penalización cuando el usuario debe realizar un transbordo entre diferentes troncales.

---

## 2. Objetivo

Encontrar una ruta de menor costo entre dos estaciones de TransMilenio considerando:

- Tiempo estimado de desplazamiento.
- Troncal utilizada.
- Cantidad de transbordos.
- Penalización asociada a cada transbordo.

El sistema permite demostrar cómo una base de conocimiento y reglas de inferencia pueden utilizarse para solucionar un problema de búsqueda de rutas.

---

## 3. Tecnologías utilizadas

- Python 3
- Algoritmo Dijkstra
- Estructuras de datos `heapq`
- `defaultdict`
- Grafo de conocimiento
- Reglas de inferencia

No se requieren librerías externas.

---

## 4. Estructura del sistema

El sistema está dividido en las siguientes partes:

### 4.1. Base de conocimiento

La base de conocimiento se encuentra en:

```python
HECHOS_CONEXION
```

Cada registro tiene la siguiente estructura:

```text
(origen, destino, troncal, tiempo)
```

Ejemplo:

```python
("Calle 26", "Avenida El Dorado", "NQS", 4)
```

Esto representa una conexión entre las estaciones Calle 26 y Avenida El Dorado, asociada a la troncal NQS, con un tiempo estimado de 4 minutos.

---

## 5. Regla de simetría

El sistema aplica una regla de inferencia que permite utilizar las conexiones en ambos sentidos.

Si la base de conocimiento contiene:

```text
A -> B
```

el sistema genera automáticamente:

```text
B -> A
```

Esto se implementa en:

```python
grafo[origen].append(
    (destino, troncal, tiempo)
)

grafo[destino].append(
    (origen, troncal, tiempo)
)
```

De esta forma, el usuario puede consultar rutas tanto de ida como de regreso.

---

## 6. Penalización por transbordo

El sistema considera que realizar un transbordo representa un costo adicional.

La penalización está definida mediante:

```python
PENALIZACION_TRANSBORDO = 5
```

Por ejemplo, si una ruta pasa de:

```text
Caracas -> NQS
```

se agregan 5 minutos al costo total de la ruta.

La fórmula utilizada es:

```text
Costo total =
    tiempo de recorrido
    +
    (número de transbordos × penalización)
```

Esta penalización representa de manera simplificada factores como desplazamiento entre plataformas, espera y complejidad del viaje.

---

## 7. Algoritmo Dijkstra

Para encontrar la ruta de menor costo se utiliza el algoritmo de Dijkstra.

El algoritmo mantiene una cola de prioridad con los posibles recorridos.

Cada estado contiene:

```text
Costo acumulado
Estación actual
Troncal actual
Camino recorrido
```

El algoritmo explora las diferentes alternativas y selecciona progresivamente la ruta con menor costo acumulado.

---

## 8. Ejemplo de funcionamiento

El usuario puede ingresar:

```text
Ingrese la estación de origen: Portal Norte
Ingrese la estación de destino: Avenida Jiménez
```

El sistema analiza las conexiones disponibles y calcula diferentes posibilidades.

Posteriormente muestra una ruta indicando:

```text
Origen: Portal Norte
Destino: Avenida Jiménez

Costo total estimado: XX minutos

Recorrido:

1. Portal Norte --[Autopista Norte, X min]--> Toberín
2. Toberín --[Autopista Norte, X min]--> Pepe Sierra
3. ...
4. ... <-- TRANSBORDO: Autopista Norte -> Caracas
5. ...
```

También muestra:

- Número de tramos.
- Troncales utilizadas.
- Número de transbordos.
- Costo total estimado.

---

## 9. Ejecución en Visual Studio Code

### Paso 1. Instalar Python

Verificar que Python esté instalado:

```bash
python --version
```

También puede utilizarse:

```bash
python3 --version
```

---

### Paso 2. Crear el archivo

Crear un archivo llamado:

```text
sistema_rutas_transmilenio.py
```

Copiar dentro del archivo el código del sistema.

---

### Paso 3. Abrir la terminal

En Visual Studio Code:

```text
Terminal → New Terminal
```

---

### Paso 4. Ejecutar el programa

Ejecutar:

```bash
python sistema_rutas_transmilenio.py
```

---

## 10. Ingreso de datos

El sistema solicitará:

```text
Ingrese la estación de origen:
```

Después:

```text
Ingrese la estación de destino:
```

Los nombres deben escribirse de acuerdo con las estaciones disponibles en la base de conocimiento.

Ejemplo:

```text
Origen: Portal Norte
Destino: Calle 26
```

---

## 11. Modificación de la base de conocimiento

Para agregar una nueva conexión se debe modificar:

```python
HECHOS_CONEXION
```

Por ejemplo:

```python
("Estacion A", "Estacion B", "Troncal X", 4)
```

Los parámetros representan:

```text
Origen
Destino
Troncal
Tiempo
```

Ejemplo:

```python
("Calle 85", "Héroes", "Autopista Norte", 3)
```

---

## 12. Agregar nuevas estaciones

Una estación se incorpora automáticamente al grafo cuando aparece dentro de una conexión.

Por ejemplo:

```python
("Portal Norte", "Toberín", "Autopista Norte", 4)
```

crea las estaciones:

```text
Portal Norte
Toberín
```

y la conexión entre ellas.

---

## 13. Funcionamiento como sistema inteligente

El sistema puede entenderse mediante tres componentes principales:

### Base de conocimiento

Contiene los hechos relacionados con el sistema de transporte:

```text
Estación A conecta con Estación B.
```

### Motor de inferencia

Aplica reglas sobre los hechos conocidos.

Ejemplo:

```text
Si A conecta con B,
entonces B conecta con A.
```

También aplica:

```text
Si la ruta cambia de troncal,
se agrega una penalización.
```

### Motor de búsqueda

Dijkstra analiza las diferentes posibilidades y determina el recorrido con menor costo.

La arquitectura general es:

```text
BASE DE CONOCIMIENTO
        |
        v
MOTOR DE INFERENCIA
        |
        v
CONSTRUCCIÓN DEL GRAFO
        |
        v
ALGORITMO DIJKSTRA
        |
        v
RUTA DE MENOR COSTO
        |
        v
EXPLICACIÓN DEL RECORRIDO
```

---

## 14. Limitaciones

Este proyecto corresponde a un modelo académico simplificado.

Los tiempos utilizados en la base de conocimiento son estimaciones y no representan necesariamente los tiempos reales de operación de TransMilenio.

El sistema tampoco considera actualmente:

- Tráfico en tiempo real.
- Tiempo real de llegada de buses.
- Demoras.
- Estaciones cerradas.
- Incidentes.
- Horarios.
- Cantidad de pasajeros.
- Capacidad de los buses.
- Tiempo real de espera.
- Rutas alimentadoras completas.

Estas funcionalidades podrían incorporarse en una versión futura.

---

## 15. Posibles mejoras

El sistema puede evolucionar incorporando:

1. Datos reales de estaciones y rutas.
2. Información de buses en tiempo real.
3. Tiempo de espera estimado.
4. Cantidad de transbordos.
5. Nivel de congestión.
6. Rutas alimentadoras.
7. Preferencias del usuario.
8. Interfaz gráfica.
9. Mapas.
10. Un modelo de inteligencia artificial para recomendar rutas.

---

## 16. Conclusión

El proyecto demuestra cómo una representación de conocimiento mediante grafos puede utilizarse para solucionar un problema de rutas.

La combinación de una base de conocimiento, reglas de inferencia y el algoritmo Dijkstra permite obtener una ruta considerando no solamente la distancia o el tiempo de desplazamiento, sino también el costo asociado a realizar transbordos.

De esta manera, el sistema constituye una implementación sencilla de un sistema inteligente aplicado al contexto del transporte público de Bogotá.