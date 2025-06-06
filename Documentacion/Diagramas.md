# Diagramas del Proyecto - Modelado de Trayectorias Elípticas

## Tabla de Contenidos
1. [Diagrama de Arquitectura General](#diagrama-de-arquitectura-general)
2. [Diagrama de Clases](#diagrama-de-clases)
3. [Diagrama de Flujo del Sistema](#diagrama-de-flujo-del-sistema)
4. [Diagrama de Secuencia - Detección de Colisiones](#diagrama-de-secuencia---detección-de-colisiones)
5. [Diagrama de Componentes](#diagrama-de-componentes)
6. [Diagrama de Estados de Trayectoria](#diagrama-de-estados-de-trayectoria)
7. [Diagrama de Casos de Uso](#diagrama-de-casos-de-uso)

## Diagrama de Arquitectura General

```mermaid
graph TB
    subgraph "Capa de Presentación"
        GUI[Interfaz Gráfica PyQt6]
        CLI[Interfaz de Línea de Comandos]
    end
    
    subgraph "Capa de Servicios"
        COL[ColisionadorTrayectorias]
        VIS[Servicios de Visualización]
    end
    
    subgraph "Capa de Modelos"
        TRAJ[TrayectoriaEliptica]
        RUT[Procesador RUT]
    end
    
    subgraph "Capa de Utilidades"
        GUTIL[graficos_utils]
        CUTIL[colision_utils]
        TUTIL[trayectoria_utils]
    end
    
    subgraph "Capa de Datos"
        COORD[Coordenadas]
        PARAM[Parámetros Elípticos]
    end
    
    GUI --> COL
    CLI --> COL
    GUI --> VIS
    CLI --> VIS
    COL --> TRAJ
    VIS --> GUTIL
    COL --> CUTIL
    TRAJ --> RUT
    TRAJ --> TUTIL
    GUTIL --> COORD
    TRAJ --> PARAM
```

## Diagrama de Clases

```mermaid
classDiagram
    class TrayectoriaEliptica {
        -float h
        -float k
        -float a
        -float b
        -float theta
        -string rut
        +__init__(h, k, a, b, theta, rut)
        +desde_rut(rut) TrayectoriaEliptica
        +calcular_posicion(t) array
        +calcular_velocidad(t, dt) array
        +trayectoria_completa(n_puntos) array
        +puntos(n) tuple
        +contiene_punto(x, y) bool
        +__repr__() string
    }
    
    class ColisionadorTrayectorias {
        +hay_colision_trayectorias(e1, e2, n) bool
        +ruta_cruce(e1, e2, n, tol) list
        +puntos_interseccion_aproximados(e1, e2, n) list
        +buscar_colisiones_trayectorias(lista) list
        +buscar_colisiones_global(trayectorias, detectar_ruta, detectar_puntos) list
    }
    
    class MainWindow {
        -list trayectorias
        -QLineEdit rut_input
        -QListWidget list_widget
        -Figure fig
        -FigureCanvas canvas
        +agregar_trayectoria()
        +graficar_trayectorias()
        +buscar_colisiones()
        +abrir_ventana_colision()
        +mostrar_ventana_canonica()
    }
    
    class VentanaInterseccion {
        -Figure fig
        -FigureCanvas canvas
        +plot_interseccion(e1, e2, ruta, puntos, idx1, idx2)
    }
    
    class VentanaEcuacionCanonica {
        +__init__(rut, label, parent)
    }
    
    TrayectoriaEliptica --> ColisionadorTrayectorias : utilizada por
    MainWindow --> TrayectoriaEliptica : gestiona
    MainWindow --> ColisionadorTrayectorias : utiliza
    MainWindow --> VentanaInterseccion : crea
    MainWindow --> VentanaEcuacionCanonica : crea
```

## Diagrama de Flujo del Sistema

```mermaid
flowchart TD
    A[Inicio del Sistema] --> B[Cargar Interfaz]
    B --> C{Tipo de Interfaz}
    C -->|GUI| D[Cargar PyQt6]
    C -->|CLI| E[Cargar Consola]
    
    D --> F[Esperar Entrada RUT]
    E --> F
    
    F --> G[Validar Formato RUT]
    G -->|Válido| H[Extraer Dígitos]
    G -->|Inválido| I[Mostrar Error]
    I --> F
    
    H --> J[Calcular Parámetros Elípticos]
    J --> K[Crear Trayectoria Elíptica]
    K --> L[Agregar a Lista]
    
    L --> M{¿Más Trayectorias?}
    M -->|Sí| F
    M -->|No| N[¿Operación Solicitada?]
    
    N -->|Visualizar| O[Generar Gráfico 2D]
    N -->|Detectar Colisiones| P[Ejecutar Algoritmo de Colisión]
    N -->|Análisis Específico| Q[Seleccionar Dos Trayectorias]
    
    O --> R[Mostrar Resultado]
    P --> S{¿Colisiones Detectadas?}
    Q --> T[Calcular Intersección]
    
    S -->|Sí| U[Mostrar Alerta de Colisión]
    S -->|No| V[Confirmar Seguridad]
    
    T --> W[Visualizar Análisis Detallado]
    
    U --> R
    V --> R
    W --> R
    
    R --> X{¿Continuar?}
    X -->|Sí| N
    X -->|No| Y[Fin del Sistema]
```

## Diagrama de Secuencia - Detección de Colisiones

```mermaid
sequenceDiagram
    participant U as Usuario
    participant GUI as MainWindow
    participant COL as ColisionadorTrayectorias
    participant T1 as TrayectoriaEliptica1
    participant T2 as TrayectoriaEliptica2
    participant UTIL as colision_utils
    
    U->>GUI: Solicita detección de colisiones
    GUI->>COL: buscar_colisiones_global(trayectorias)
    
    loop Para cada par de trayectorias
        COL->>T1: puntos(n=500)
        T1-->>COL: coordenadas_x1, coordenadas_y1
        COL->>T2: puntos(n=500)
        T2-->>COL: coordenadas_x2, coordenadas_y2
        
        COL->>UTIL: hay_colision_trayectorias(T1, T2)
        
        loop Para cada punto de T1
            UTIL->>T2: contiene_punto(x, y)
            T2-->>UTIL: boolean
        end
        
        loop Para cada punto de T2
            UTIL->>T1: contiene_punto(x, y)
            T1-->>UTIL: boolean
        end
        
        UTIL-->>COL: resultado_colision
        
        alt Si hay colisión
            COL->>UTIL: ruta_cruce(T1, T2)
            UTIL-->>COL: puntos_ruta
            COL->>UTIL: puntos_interseccion_aproximados(T1, T2)
            UTIL-->>COL: puntos_interseccion
        end
    end
    
    COL-->>GUI: lista_colisiones
    GUI->>GUI: graficar_rutas_puntos_colision()
    GUI-->>U: Visualización de colisiones
```

## Diagrama de Componentes

```mermaid
graph TB
    subgraph "Sistema de Modelado de Trayectorias"
        subgraph "Módulo de Interfaz"
            GUI[app.py - GUI PyQt6]
            CLI[main.py - Interfaz CLI]
        end
        
        subgraph "Módulo de Modelos"
            TRAJ[modelos/trayectoria_eliptica.py]
        end
        
        subgraph "Módulo de Servicios"
            COL[servicios/colisionador_trayectorias.py]
        end
        
        subgraph "Módulo de Utilidades"
            GUTIL[utils/graficos_utils.py]
            CUTIL[utils/colision_utils.py]
            TUTIL[utils/trayectoria_utils.py]
        end
        
        subgraph "Bibliotecas Externas"
            PYQT[PyQt6]
            MPL[Matplotlib]
            NUMPY[NumPy]
            SYMPY[SymPy]
        end
    end
    
    GUI --> TRAJ
    GUI --> COL
    GUI --> GUTIL
    CLI --> TRAJ
    CLI --> COL
    CLI --> GUTIL
    
    COL --> CUTIL
    TRAJ --> TUTIL
    GUTIL --> MPL
    
    GUI --> PYQT
    TRAJ --> NUMPY
    CUTIL --> NUMPY
    TUTIL --> SYMPY
```

## Diagrama de Estados de Trayectoria

```mermaid
stateDiagram-v2
    [*] --> Inicializado
    
    Inicializado --> Validando : desde_rut(rut)
    Validando --> Válido : RUT correcto
    Validando --> Error : RUT inválido
    Error --> [*]
    
    Válido --> Calculando : calcular_parámetros()
    Calculando --> Activo : parámetros_listos
    
    Activo --> Graficando : solicitar_visualización()
    Activo --> Analizando : detectar_colisiones()
    Activo --> Movimiento : calcular_posición(t)
    
    Graficando --> Activo : gráfico_completado
    Analizando --> Colisión : colisión_detectada
    Analizando --> Seguro : sin_colisiones
    Movimiento --> Activo : cálculo_completado
    
    Colisión --> Activo : análisis_completado
    Seguro --> Activo : verificación_completada
    
    Activo --> Finalizado : eliminar_trayectoria()
    Finalizado --> [*]
```

## Diagrama de Casos de Uso

```mermaid
graph LR
    subgraph "Sistema de Modelado de Trayectorias"
        UC1[Crear Trayectoria desde RUT]
        UC2[Visualizar Trayectorias 2D]
        UC3[Detectar Colisiones Globales]
        UC4[Analizar Colisión Específica]
        UC5[Mostrar Ecuación Canónica]
        UC6[Calcular Rutas de Cruce]
        UC7[Identificar Puntos de Intersección]
        UC8[Gestionar Lista de Trayectorias]
    end
    
    Actor1[Operador de Drones] --> UC1
    Actor1 --> UC2
    Actor1 --> UC3
    Actor1 --> UC4
    
    Actor2[Ingeniero de Seguridad] --> UC3
    Actor2 --> UC6
    Actor2 --> UC7
    
    Actor3[Analista Matemático] --> UC5
    Actor3 --> UC1
    
    Actor4[Administrador del Sistema] --> UC8
    Actor4 --> UC2
      UC1 -.->|incluye| UC8
    UC3 -.->|incluye| UC6
    UC3 -.->|incluye| UC7
    UC4 -.->|incluye| UC6
    UC4 -.->|incluye| UC7
    UC2 -.->|requiere| UC8
```

---

## Notas sobre los Diagramas

### Arquitectura del Sistema
- **Capa de Presentación**: Maneja las interfaces de usuario (GUI y CLI)
- **Capa de Servicios**: Contiene la lógica de negocio para detección de colisiones
- **Capa de Modelos**: Define las estructuras de datos para trayectorias elípticas
- **Capa de Utilidades**: Proporciona funciones auxiliares para cálculos y visualización

### Flujo de Datos
1. El usuario ingresa un RUT
2. El sistema extrae los dígitos y calcula parámetros elípticos
3. Se crea una instancia de TrayectoriaEliptica
4. El sistema puede realizar análisis de colisiones o visualizaciones
5. Los resultados se presentan al usuario

### Algoritmos de Colisión
- **Detección básica**: Verifica si puntos de una elipse están dentro de otra
- **Ruta de cruce**: Identifica todos los puntos donde las trayectorias se solapan
- **Puntos de intersección**: Encuentra ubicaciones específicas donde las trayectorias se cruzan

### Consideraciones de Seguridad
- Validación rigurosa de entrada de datos
- Manejo de errores en cálculos matemáticos
- Alertas visuales para situaciones de riesgo de colisión