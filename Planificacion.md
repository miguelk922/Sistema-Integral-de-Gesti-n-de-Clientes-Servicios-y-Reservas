# Sistema Integral de Gestion de Clientes Servicios y Reservas (Software FJ)

## Planteamiento de la problematica a Resolver

La empresa Software FJ ha diversificado su portafolio comercial ofreciendo tres líneas de negocio principales: reserva de salas, alquiler de equipos y asesorías especializadas.

<u>El Problema</u>
Actualmente, la operación carece de un sistema centralizado y tolerante a fallos. Los errores humanos (datos incompletos, intentos de reservas sobre servicios no disponibles o cálculos inconsistentes) provocan caídas totales en la gestión operativa. Además, por restricciones de infraestructura y latencia, no es viable depender de un motor de bases de datos externo para este módulo, lo que exige una solución autónoma de alta velocidad.

<u>La Solución Requerida</u>
Se requiere desarrollar un Módulo Central de Gestión en Memoria (basado en una arquitectura robusta orientada a objetos) que administre todo el ciclo de vida operativo: clientes, catálogo de servicios y flujo de reservas.


### Tabla de Requerimentos

### Tabla de Requerimientos del Sistema - Software FJ

| ID | Categoría | Requerimiento | Detalle Técnico | Prioridad |
| :--- | :--- | :--- | :--- | :--- |
| **RF-01** | Arquitectura POO | Clase abstracta general | Representar entidades generales del sistema como base jerárquica. | Alta |
| **RF-02** | Gestión de Clientes | Clase Cliente | Encapsular datos personales con validaciones estrictas de entrada. | Alta |
| **RF-03** | Gestión de Servicios | Clase abstracta Servicio y derivadas | Crear clase base y mínimo 3 derivadas (salas, equipos, asesorías) con polimorfismo. | Alta |
| **RF-04** | Cálculos y Costos | Sobrescritura y sobrecarga | Sobrescribir cálculo de costos y sobrecargar métodos con impuestos o descuentos. | Alta |
| **RF-05** | Gestión de Reservas | Clase Reserva | Integrar cliente, servicio, duración y estado; incluir confirmación y cancelación. | Alta |
| **RNF-01** | Almacenamiento | Persistencia en memoria | Gestionar datos mediante listas internas y objetos, sin usar motores de bases de datos. | Alta |
| **RNF-02** | Estabilidad | Manejo avanzado de excepciones | Usar excepciones propias, bloques `try/except/else/finally` y encadenamiento. | Alta |
| **RNF-03** | Auditoría | Registro en archivo de Logs | Guardar errores y eventos relevantes en un archivo de texto manteniendo el sistema activo. | Alta |
| **RNF-04** | Pruebas | Simulación de operaciones | Ejecutar mínimo 10 operaciones combinando casos válidos, inválidos y fallidos. | Alta |

#### Notas adicionales de implementación:
* **Control de errores operativos (RNF-02):** El sistema debe interceptar datos inválidos, parámetros faltantes, operaciones no permitidas, servicios no disponibles y cálculos inconsistentes sin detener la ejecución general.
* **Entregable documental (RNF-05):** Presentar informe en PDF con portada, introducción, enlace al repositorio en GitHub, conclusiones y bibliografía en normas APA.


***

### Diagrama de Flujo

```mermaid
flowchart TD
    Start([Inicio: Ejecución de Software FJ]) --> Init[Inicializar Listas en Memoria: Clientes, Servicios, Reservas y Archivo Log]
    Init --> SimLoop[Ciclo de Simulación: Mínimo 10 Operaciones de Prueba]

    SimLoop --> TryStart[/Inicio Bloque TRY: Seleccionar Operación/]

    %% RAMA 1: CLIENTES (RF-02)
    TryStart -->|Opción 1: Registrar Cliente| ValCli[Instanciar Cliente heredando de EntidadGeneral]
    ValCli --> CheckCli{¿Datos encapsulados válidos y completos?}
    CheckCli -->|No: Dato inválido / Parámetro faltante| ErrCli[Lanzar Excepción: ClienteInvalidoError]
    CheckCli -->|Sí| ElseBlock

    %% RAMA 2: SERVICIOS (RF-03)
    TryStart -->|Opción 2: Crear Servicio| TipoServ[Instanciar Subclase: Sala, Equipo o Asesoría]
    TipoServ --> CheckServ{¿Parámetros específicos y costos base válidos?}
    CheckServ -->|No: Parámetro faltante / Valor negativo| ErrServ[Lanzar Excepción: ServicioInvalidoError]
    CheckServ -->|Sí| ElseBlock

    %% RAMA 3: RESERVAS (RF-04 y RF-05)
    TryStart -->|Opción 3: Gestionar Reserva| AccionRes[Acción: Procesar, Confirmar o Cancelar Reserva]
    AccionRes --> CheckDisp{¿Cliente existe, Servicio disponible y Estado permitido?}
    CheckDisp -->|No: No disponible / Operación no permitida| ErrRes[Lanzar Excepción: ReservaError / OperacionNoPermitidaError]
    CheckDisp -->|Sí| CalcCosto[Calcular Costo Polimórfico y Sobrecargado: Base + Impuestos - Descuentos]
    
    CalcCosto --> CheckCalc{¿Cálculo consistente y Duración válida?}
    CheckCalc -->|No: Cálculo inconsistente / Intento incorrecto| ErrCalc[Lanzar Excepción: CalculoInconsistenteError]
    CheckCalc -->|Sí| ElseBlock

    %% BLOQUE EXCEPT (RNF-02 y RNF-03)
    ErrCli --> ExceptBlock[\Bloque EXCEPT: Interceptar Error sin detener el sistema\]
    ErrServ --> ExceptBlock
    ErrRes --> ExceptBlock
    ErrCalc --> ExceptBlock

    ExceptBlock --> ChainExc[Encadenamiento de Excepciones: raise ExcepcionSistema from CausaOriginal]
    ChainExc --> LogError[(Archivo .log: Registrar Excepción, Traza y Fecha)]

    %% BLOQUE ELSE (RNF-01 y RNF-03)
    ElseBlock[\Bloque ELSE: Ejecución sin Errores\] --> SaveMem[(Guardar/Actualizar Objeto en Listas Internas)]
    SaveMem --> PrintDesc[Ejecutar Polimorfismo: describir_servicio y mostrar resumen]
    PrintDesc --> LogSuccess[(Archivo .log: Registrar Operación Exitosa)]

    %% BLOQUE FINALLY (RNF-02 y RNF-04)
    LogError --> FinallyBlock[\Bloque FINALLY: Garantizar estabilidad y liberar estado de operación\]
    LogSuccess --> FinallyBlock

    FinallyBlock --> CountOps{¿Se completaron las 10+ simulaciones?}
    CountOps -->|No: Siguiente caso de prueba| SimLoop
    CountOps -->|Sí| Resumen[Mostrar Resumen Final de Listas y Estado del Sistema]
    Resumen --> End([Fin de la Aplicación Estable])

    %% Estilos visuales
    classDef initStyle fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000
    classDef tryStyle fill:#fff8e1,stroke:#f57f17,stroke-width:2px,color:#000
    classDef errorStyle fill:#ffebee,stroke:#c62828,stroke-width:2px,color:#000
    classDef okStyle fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
    classDef logStyle fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px,color:#000

    class Init,SimLoop,Resumen initStyle
    class TryStart,ValCli,TipoServ,AccionRes,CalcCosto tryStyle
    class ErrCli,ErrServ,ErrRes,ErrCalc,ExceptBlock,ChainExc errorStyle
    class ElseBlock,SaveMem,PrintDesc okStyle
    class LogError,LogSuccess,FinallyBlock logStyle
```