# Registro de Trazabilidad y Versionado — Software FJ

## 1. Archivo: `modelos.py` (Capa 1 — Núcleo POO y Reglas de Negocio)

### Módulo General `modelos.py`
```text
AUTOR:  "Agente Antigravity"
COMMIT: "Eliminación de imports abc y datetime; abstracción nativa en Python puro mediante control de instanciación y NotImplementedError"
FECHA:  "2026-11-20 09:57"
VERSION:
        v1: AUTOR:  "Agente Antigravity"
            COMMIT: "Implementación limpia de Capa 1 (modelos.py) con convenciones de nombres en español, jerarquía POO y excepciones propias"
            FECHA:  "2026-11-20 09:53"
```

### Pieza 1.1: Jerarquía de Excepciones Propias (`ExcepcionSistema` y derivadas)
- **Clases incluidas:** `ExcepcionSistema`, `DatosInvalidosError`, `ClienteInvalidoError`, `ServicioInvalidoError`, `ParametroFaltanteError`, `OperacionNoPermitidaError`, `ReservaError`, `ServicioNoDisponibleError`, `CalculoInconsistenteError`.
```text
AUTOR:  "Agente Antigravity"
COMMIT: "Definición de jerarquía de excepciones personalizadas para control de errores de dominio (RNF-02)"
FECHA:  "2026-11-20 09:53"
VERSION:
```

### Pieza 1.2: Clase Abstracta Base `EntidadGeneral` (RF-01)
```text
AUTOR:  "Agente Antigravity"
COMMIT: "Abstracción nativa sin librería abc ni datetime en EntidadGeneral"
FECHA:  "2026-11-20 09:57"
VERSION:
        v1: AUTOR:  "Agente Antigravity"
            COMMIT: "Creación de clase abstracta base EntidadGeneral con id y fecha_creacion"
            FECHA:  "2026-11-20 09:53"
```

### Pieza 1.3: Clase `Cliente` (RF-02)
```text
AUTOR:  "Agente Antigravity"
COMMIT: "Implementación de clase Cliente con atributos privados (__nombre, __documento, __correo, __telefono) y setters validadores"
FECHA:  "2026-11-20 09:53"
VERSION:
```

### Pieza 1.4: Clase Abstracta `Servicio` (RF-03 y RF-04)
```text
AUTOR:  "Agente Antigravity"
COMMIT: "Abstracción nativa en clase Servicio sin depender del módulo abc"
FECHA:  "2026-11-20 09:57"
VERSION:
        v1: AUTOR:  "Agente Antigravity"
            COMMIT: "Creación de clase abstracta Servicio con soporte polimórfico y validación de costos"
            FECHA:  "2026-11-20 09:53"
```

### Pieza 1.5: Subclase `ReservaSala` (RF-03 y RF-04)
```text
AUTOR:  "Agente Antigravity"
COMMIT: "Implementación de subclase ReservaSala con capacidad, equipamiento y cálculo polimórfico sobrecargado"
FECHA:  "2026-11-20 09:53"
VERSION:
```

### Pieza 1.6: Subclase `AlquilerEquipo` (RF-03 y RF-04)
```text
AUTOR:  "Agente Antigravity"
COMMIT: "Implementación de subclase AlquilerEquipo con cantidad de equipos, gama y cálculo polimórfico sobrecargado"
FECHA:  "2026-11-20 09:53"
VERSION:
```

### Pieza 1.7: Subclase `AsesoriaEspecializada` (RF-03 y RF-04)
```text
AUTOR:  "Agente Antigravity"
COMMIT: "Implementación de subclase AsesoriaEspecializada con especialidad, nivel de experto y cálculo polimórfico sobrecargado"
FECHA:  "2026-11-20 09:53"
VERSION:
```

### Pieza 1.8: Clase `Reserva` (RF-05)
```text
AUTOR:  "Agente Antigravity"
COMMIT: "Implementación de clase Reserva con estados (Pendiente, Confirmada, Cancelada) y métodos procesar, confirmar y cancelar"
FECHA:  "2026-11-20 09:53"
VERSION:
```

---

## 2. Archivo: `gestor_sistema.py` (Capa 2 — Cerebro Operativo, Memoria, Logs y Simulador)

### Módulo General `gestor_sistema.py` y Clase `GestorSistema`
- **Componentes incluidos:**
  1. Persistencia en memoria con listas internas (`_clientes`, `_servicios`, `_reservas`) y métodos de consulta/búsqueda (RNF-01).
  2. Sistema de auditoría en `eventos_y_errores.log` en Python puro con lectura y escritura tolerante a fallos (RNF-03).
  3. Operaciones de negocio (`registrar_cliente`, `crear_servicio`, `crear_reserva`, `confirmar_reserva`, `cancelar_reserva`) con bloques `try / except / else / finally` y encadenamiento `raise ... from ...` (RNF-02).
  4. Simulador automático (`ejecutar_simulacion`) con 12 operaciones mixtas válidas, inválidas y fallidas (RNF-04).
```text
AUTOR:  "Agente Antigravity"
COMMIT: "Implementación de Capa 2 (gestor_sistema.py) en Python puro importando únicamente modelos.py: memoria, logs, encadenamiento de excepciones y simulador"
FECHA:  "2026-11-20 10:24"
VERSION:
```

---

## 3. Archivo: `Software_FJ.py` (Capa 3 — Interfaz Gráfica Tkinter y Punto de Entrada)

### Módulo General `Software_FJ.py` y Clase `AplicacionSoftwareFJ`
- **Componentes incluidos:**
  1. Importación exclusiva de `tkinter` (`tk`, `ttk`, `messagebox`) y `GestorSistema` desde `gestor_sistema.py` (respetando la cascada unidireccional sin importar `modelos.py`).
  2. Pestaña 1 (`_construir_pestana_clientes`): Formulario y tabla en vivo para registro de clientes.
  3. Pestaña 2 (`_construir_pestana_servicios`): Formulario dinámico para creación polimórfica de `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada` con tabla en tiempo real.
  4. Pestaña 3 (`_construir_pestana_reservas`): Formulario con selectores de cliente/servicio, campos opcionales sobrecargados (impuesto, descuento, recargo), botones de crear/procesar, confirmar y cancelar, y tabla de reservas.
  5. Pestaña 4 (`_construir_pestana_simulacion`): Ejecución interactiva de las 12 operaciones de prueba del simulador con tabla de resultados.
  6. Visor inferior de auditoría (`_construir_visor_logs`): Lectura automática en tiempo real de `eventos_y_errores.log`.
```text
AUTOR:  "Agente Antigravity"
COMMIT: "Implementación de Capa 3 (Software_FJ.py): interfaz gráfica en Tkinter con 4 pestañas, visor de logs en vivo y conexión unidireccional con GestorSistema"
FECHA:  "2026-11-20 10:32"
VERSION:
        v1: AUTOR:  "Usuario"
            COMMIT: "Archivo inicial de prueba con print de saludo"
            FECHA:  "2026-11-19 23:57"
```
