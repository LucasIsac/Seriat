# Seriat: Simulador de Sistemas de Colas

Seriat es una herramienta de simulación de eventos discretos (DES) basada en Python, diseñada para modelar y analizar diversas configuraciones de sistemas de colas. Esta aplicación fue desarrollada como solución integral para el Trabajo Práctico No. 1 (TP1) de la asignatura Modelización y Simulación de Sistemas.

## Descripción General

La aplicación utiliza un motor de simulación basado en cola de prioridad para procesar eventos cronológicamente. Proporciona una interfaz CLI estructurada para configurar y ejecutar tres escenarios de simulación distintos.

## Características Principales

- **Arquitectura Modular**: Separación del motor de simulación, lógica específica de problemas e interfaz de usuario.
- **Interfaz CLI Interactiva**: Configuración paso a paso usando la biblioteca Rich para salida formateada y tablas.
- **Predefinidos Incluidos**: Incluye secuencias de datos de las tablas del TP1 para facilitar la verificación de simulaciones manuales.
- **Generadores Flexibles**: Soporte para valores constantes y secuencias basadas en listas para intervalos de tiempo.
- **Seguimiento de Estado**: Grabación detallada de cambios de estado del sistema (reloj, tamaño de cola, estado del servidor) para cada evento procesado.
- **Internacionalización**: Soporte para inglés y español.
- **Exportar Resultados**: Los resultados pueden exportarse a tablas Markdown.

## Escenarios Implementados

### 1. Servidor Único Estándar (FCFS)
Modela un sistema básico donde los clientes llegan a intervalos y son atendidos uno a uno en orden de llegada.

### 2. Servidor con Intervalos de Trabajo/Descanso
Simula un sistema donde el servidor alterna entre períodos activos de trabajo y descansos. Incluye lógica para suspender y reanudar servicios cuando el servidor se ausenta.

### 3. Renegación (Abandono)
Introduce umbrales de paciencia del cliente. Los clientes abandonarán la cola si su tiempo de espera excede un límite específico antes de ser atendidos.

## Estructura del Proyecto

```
seriat/
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt       # Dependencias
├── .gitignore          # Reglas de Git ignore
├── sim/
│   ├── __init__.py
│   ├── engine.py        # Motor DES core usando heapq
│   └── problems/
│       ├── __init__.py
│       ├── base.py     # Clase base Problem
│       ├── problem1.py # Ejercicio 1: FCFS
│       ├── problem2.py # Ejercicio 2: Trabajo/Descanso
│       └── problem3.py # Ejercicio 3: Renegación
├── ui/
│   ├── __init__.py
│   └── cli.py      # CLI basada en Rich
└── utils/
    ├── __init__.py
    ├── generators.py  # Generadores de intervalos
    ├── exporter.py  # Exportador de resultados
    └── i18n.py    # Internacionalización
```

## Requisitos

- Python 3.8 o superior
- Biblioteca Rich (`pip install rich`)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/LucasIsac/Seriat.git
cd Seriat
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Ejecutar el simulador:
```bash
python main.py
```

Seguir las instrucciones en pantalla para:
1. **Seleccionar idioma** (Español/Inglés)
2. **Elegir problema** (1, 2 o 3)
3. **Configurar generadores de tiempo**:
   - Valor constante (ej., 45 segundos)
   - Lista de valores (ej., 65, 6, 2, 21, 42, 33, 21)
   - Predefinido de las tablas del TP1
4. **Definir número de eventos** a simular
5. **Ver resultados** en formato de tabla
6. Opcionalmente **ver diagrama de flujo de eventos** en el navegador

## Cómo Funciona

La simulación usa el algoritmo de **Avance al Próximo Evento**:

1. Inicializar reloj en 0
2. Programar eventos iniciales (primera llegada, etc.)
3. Procesar eventos en orden cronológico usando una cola de prioridad (heapq)
4. Para cada evento, actualizar estado del sistema y programar eventos futuros
5. Grabar estado después de cada evento

### Tipos de Eventos

| Evento | Descripción |
|--------|------------|
| `ARRIVAL` | Nuevo cliente llega |
| `END_SERVICE` | Servidor termina de atender un cliente |
| `SERVER_DEPARTURE` | Servidor se ausenta a descansar (Problema 2) |
| `SERVER_ARRIVAL` | Servidor regresa del descanso (Problema 2) |
| `RENEGING` | Cliente abandona la cola (Problema 3) |

### Variables de Estado del Sistema

| Variable | Descripción |
|----------|------------|
| `clock` | Tiempo actual de simulación |
| `server_busy` | 0 = libre, 1 = ocupado |
| `server_present` | 0 = descansando, 1 = en estación |
| `queue` | Número de clientes esperando |
| `abandoned_count` | Total de clientes abandonados (Problema 3) |

## Leyenda Gráfica

En las tablas de resultados, la columna **Gráfica** muestra:

| Símbolo | Significado |
|---------|------------|
| `◠` | Servidor presente pero idle |
| `▣` | Servidor ocupado |
| `□` | Servidor idle (disponible) |
| `●` | Cliente en cola |

**Ejemplo:** `◠[▣] ● ●` = Servidor presente, ocupado, 2 clientes esperando

## Licencia

MIT License