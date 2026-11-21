"""
AUTOR:  "Miguel Parra"
COMMIT: "Eliminación de imports abc y datetime; abstracción nativa en Python puro mediante control de instanciación y NotImplementedError, Modificaciones pequeñas de descripciones exepciones....."
FECHA:  "2026-11-19 10:00"
VERSION:
        v1: AUTOR:  "Agente Antigravity"
            COMMIT: "Implementación de Capa con convenciones de nombres, jerarquía POO y excepciones propias"
            FECHA:  "2026-11-19 09:40"
"""


# =====================================================================
# 1. JERARQUÍA DE EXCEPCIONES PROPIAS DEL SISTEMA (RNF-02)
# =====================================================================

class ExcepcionSistema(Exception):
    """Clase base para todas las excepciones de negocio de Software FJ."""
    pass


class DatosInvalidosError(ExcepcionSistema):
    """Se lanza cuando un dato de entrada no cumple el formato o rango esperado."""
    pass


class ClienteInvalidoError(DatosInvalidosError):
    """Se lanza cuando los datos personales de un cliente son inválidos."""
    pass


class ServicioInvalidoError(DatosInvalidosError):
    """Se lanza cuando los parámetros de configuración de un servicio son inválidos."""
    pass


class ParametroFaltanteError(ExcepcionSistema):
    """Se lanza cuando un campo o parámetro obligatorio está vacío o ausente."""
    pass


class OperacionNoPermitidaError(ExcepcionSistema):
    """Se lanza cuando se intenta una transición de estado u operación inválida."""
    pass


class ReservaError(ExcepcionSistema):
    """Se lanza cuando ocurre un error en la creación o gestión de una reserva."""
    pass


class ServicioNoDisponibleError(ReservaError):
    """Se lanza cuando se intenta reservar o confirmar un servicio que no está disponible."""
    pass


class CalculoInconsistenteError(ExcepcionSistema):
    """Se lanza cuando los valores de tarifas, duraciones, impuestos o descuentos producen un cálculo inválido."""
    pass


# =====================================================================
# 2. CLASE ABSTRACTA BASE: ENTIDAD GENERAL (RF-01)
# =====================================================================

class EntidadGeneral:
    """
    AUTOR:  "Miguel Parra"
    COMMIT: "Abstracción nativa sin librería abc ni datetime en EntidadGeneral"
    FECHA:  "2026-11-19 09:57"
    VERSION:
            v1: AUTOR:  "Agente Antigravity"
                COMMIT: "Creación de clase abstracta base EntidadGeneral con id y fecha_creacion"
                FECHA:  "2026-11-18 19:00"
    """

    _contador_registros = 0

    def __init__(self, id_entidad, fecha_creacion=None):
        if type(self) is EntidadGeneral:
            raise OperacionNoPermitidaError(
                "No se puede instanciar directamente la clase abstracta EntidadGeneral."
            )
        if id_entidad is None or str(id_entidad).strip() == "":
            raise ParametroFaltanteError("El identificador (ID) de la entidad es obligatorio.")

        EntidadGeneral._contador_registros += 1
        self._id = str(id_entidad).strip()
        if fecha_creacion is None or str(fecha_creacion).strip() == "":
            self._fecha_creacion = f"Registro #{EntidadGeneral._contador_registros}"
        else:
            self._fecha_creacion = str(fecha_creacion).strip()

    @property
    def id(self):
        return self._id

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    def validar_datos(self):
        """Método abstracto: valida los datos internos obligatorios de la entidad."""
        raise NotImplementedError(
            "El método abstracto 'validar_datos' debe ser implementado por la subclase."
        )

    def obtener_resumen(self):
        """Método abstracto: retorna una representación resumida y legible de la entidad."""
        raise NotImplementedError(
            "El método abstracto 'obtener_resumen' debe ser implementado por la subclase."
        )


# =====================================================================
# 3. CLASE CLIENTE CON ENCAPSULAMIENTO ESTRICTO (RF-02)
# =====================================================================

class Cliente(EntidadGeneral):
    """
    AUTOR:  "Agente Antigravity"
    COMMIT: "Implementación de clase Cliente con atributos privados y setters validadores"
    FECHA:  "2026-11-20 09:53"
    VERSION:
    """

    def __init__(self, id_cliente, nombre, documento, correo, telefono):
        super().__init__(id_cliente)
        self.__nombre = ""
        self.__documento = ""
        self.__correo = ""
        self.__telefono = ""

        # Asignación mediante setters para validar desde la creación del objeto
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        self.validar_datos()

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        if nuevo_nombre is None or str(nuevo_nombre).strip() == "":
            raise ParametroFaltanteError("El nombre del cliente no puede estar vacío.")
        texto_nombre = str(nuevo_nombre).strip()
        if len(texto_nombre) < 3:
            raise ClienteInvalidoError(f"El nombre '{texto_nombre}' es demasiado corto (mínimo 3 caracteres).")
        self.__nombre = texto_nombre

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, nuevo_documento):
        if nuevo_documento is None or str(nuevo_documento).strip() == "":
            raise ParametroFaltanteError("El documento del cliente es obligatorio.")
        texto_documento = str(nuevo_documento).strip()
        if not texto_documento.isdigit() or len(texto_documento) < 5:
            raise ClienteInvalidoError(
                f"El documento '{texto_documento}' es inválido (debe contener solo números y al menos 5 dígitos)."
            )
        self.__documento = texto_documento

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, nuevo_correo):
        if nuevo_correo is None or str(nuevo_correo).strip() == "":
            raise ParametroFaltanteError("El correo electrónico del cliente es obligatorio.")
        texto_correo = str(nuevo_correo).strip()
        partes_correo = texto_correo.split("@")
        if "@" not in texto_correo or len(partes_correo) != 2 or not partes_correo[0] or "." not in partes_correo[1]:
            raise ClienteInvalidoError(f"El correo electrónico '{texto_correo}' no tiene un formato válido.")
        self.__correo = texto_correo

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, nuevo_telefono):
        if nuevo_telefono is None or str(nuevo_telefono).strip() == "":
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        texto_telefono = str(nuevo_telefono).strip()
        if not texto_telefono.isdigit() or len(texto_telefono) < 7:
            raise ClienteInvalidoError(
                f"El teléfono '{texto_telefono}' es inválido (debe ser numérico y tener mínimo 7 dígitos)."
            )
        self.__telefono = texto_telefono

    def validar_datos(self):
        if not all([self.__nombre, self.__documento, self.__correo, self.__telefono]):
            raise ParametroFaltanteError("Faltan datos obligatorios en el registro del cliente.")
        return True

    def obtener_resumen(self):
        return (
            f"Cliente [{self.id}] {self.nombre} | Doc: {self.documento} | "
            f"Correo: {self.correo} | Tel: {self.telefono}"
        )


# =====================================================================
# 4. CLASE ABSTRACTA SERVICIO Y DERIVADAS POLIMÓRFICAS (RF-03 y RF-04)
# =====================================================================

class Servicio(EntidadGeneral):
    """
    AUTOR:  "Agente Antigravity"
    COMMIT: "Abstracción nativa en clase Servicio sin depender del módulo abc"
    FECHA:  "2026-11-20 09:57"
    VERSION:
            v1: AUTOR:  "Agente Antigravity"
                COMMIT: "Creación de clase abstracta Servicio con soporte polimórfico y validación de costos"
                FECHA:  "2026-11-20 09:53"
    """

    def __init__(self, id_servicio, nombre, tarifa_hora, disponible=True):
        if type(self) is Servicio:
            raise OperacionNoPermitidaError(
                "No se puede instanciar directamente la clase abstracta Servicio."
            )
        super().__init__(id_servicio)
        self._nombre = ""
        self._tarifa_hora = 0.0
        self._disponible = True

        self.nombre = nombre
        self.tarifa_hora = tarifa_hora
        self.disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        if nuevo_nombre is None or str(nuevo_nombre).strip() == "":
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        self._nombre = str(nuevo_nombre).strip()

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @tarifa_hora.setter
    def tarifa_hora(self, nueva_tarifa):
        if nueva_tarifa is None or str(nueva_tarifa).strip() == "":
            raise ParametroFaltanteError("La tarifa por hora es obligatoria.")
        try:
            valor_tarifa = float(nueva_tarifa)
        except (ValueError, TypeError) as error_original:
            raise ServicioInvalidoError(
                f"La tarifa por hora '{nueva_tarifa}' debe ser un número válido."
            ) from error_original
        if valor_tarifa <= 0:
            raise ServicioInvalidoError(
                f"La tarifa por hora debe ser mayor a 0 (recibido: {valor_tarifa})."
            )
        self._tarifa_hora = valor_tarifa

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, estado_disponible):
        self._disponible = bool(estado_disponible)

    def aplicar_ajustes_sobrecargados(self, costo_base, impuesto=0.0, descuento=0.0, recargo=0.0):
        """
        Aplica los porcentajes opcionales de impuesto, descuento y recargo
        sobre el costo base, verificando que los valores sean consistentes.
        """
        try:
            valor_impuesto = float(impuesto)
            valor_descuento = float(descuento)
            valor_recargo = float(recargo)
        except (ValueError, TypeError) as error_original:
            raise CalculoInconsistenteError(
                "Los valores de impuesto, descuento o recargo deben ser numéricos."
            ) from error_original

        if valor_impuesto < 0 or valor_recargo < 0:
            raise CalculoInconsistenteError("El impuesto y el recargo no pueden ser negativos.")
        if valor_descuento < 0 or valor_descuento > 100:
            raise CalculoInconsistenteError(
                f"El porcentaje de descuento es inconsistente ({valor_descuento}%). Debe estar entre 0% y 100%."
            )

        monto_descuento = costo_base * (valor_descuento / 100.0)
        subtotal = costo_base - monto_descuento
        monto_impuesto = subtotal * (valor_impuesto / 100.0)
        monto_recargo = subtotal * (valor_recargo / 100.0)
        costo_final = round(subtotal + monto_impuesto + monto_recargo, 2)

        if costo_final < 0:
            raise CalculoInconsistenteError(f"El costo total calculado resultó negativo ({costo_final}).")
        return costo_final

    def validar_duracion(self, duracion):
        """Valida que la duración en horas sea un número positivo."""
        if duracion is None or str(duracion).strip() == "":
            raise ParametroFaltanteError("La duración del servicio es obligatoria.")
        try:
            horas_validas = float(duracion)
        except (ValueError, TypeError) as error_original:
            raise CalculoInconsistenteError(
                f"La duración '{duracion}' debe ser numérica."
            ) from error_original
        if horas_validas <= 0:
            raise CalculoInconsistenteError(
                f"La duración debe ser mayor a 0 horas (recibido: {horas_validas})."
            )
        return horas_validas

    def validar_datos(self):
        return self.validar_parametros()

    def validar_parametros(self):
        """Método abstracto: valida los parámetros específicos del tipo de servicio."""
        raise NotImplementedError(
            "El método abstracto 'validar_parametros' debe ser implementado por la subclase."
        )

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0, recargo=0.0):
        """
        Método abstracto: calcula el costo del servicio aplicando polimorfismo
        y sobrecarga mediante parámetros opcionales (impuesto, descuento y recargo).
        """
        raise NotImplementedError(
            "El método abstracto 'calcular_costo' debe ser implementado por la subclase."
        )

    def describir_servicio(self):
        """Método abstracto: retorna la descripción polimórfica detallada del servicio."""
        raise NotImplementedError(
            "El método abstracto 'describir_servicio' debe ser implementado por la subclase."
        )

    def obtener_resumen(self):
        return self.describir_servicio()


class ReservaSala(Servicio):
    """
    AUTOR:  "Agente Antigravity"
    COMMIT: "Implementación de subclase ReservaSala con capacidad, equipamiento y cálculo polimórfico"
    FECHA:  "2026-11-20 09:53"
    VERSION:
    """

    def __init__(self, id_servicio, nombre, tarifa_hora, capacidad, incluye_equipamiento=False, disponible=True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        self._capacidad = 0
        self._incluye_equipamiento = bool(incluye_equipamiento)
        self.capacidad = capacidad
        self.validar_parametros()

    @property
    def capacidad(self):
        return self._capacidad

    @capacidad.setter
    def capacidad(self, nueva_capacidad):
        if nueva_capacidad is None or str(nueva_capacidad).strip() == "":
            raise ParametroFaltanteError("La capacidad de la sala es obligatoria.")
        try:
            valor_capacidad = int(nueva_capacidad)
        except (ValueError, TypeError) as error_original:
            raise ServicioInvalidoError(
                f"La capacidad '{nueva_capacidad}' debe ser un número entero."
            ) from error_original
        if valor_capacidad <= 0:
            raise ServicioInvalidoError(
                f"La capacidad de la sala debe ser mayor a 0 (recibido: {valor_capacidad})."
            )
        self._capacidad = valor_capacidad

    @property
    def incluye_equipamiento(self):
        return self._incluye_equipamiento

    @incluye_equipamiento.setter
    def incluye_equipamiento(self, estado_equipamiento):
        self._incluye_equipamiento = bool(estado_equipamiento)

    def validar_parametros(self):
        if self._capacidad <= 0 or self._tarifa_hora <= 0:
            raise ServicioInvalidoError("Parámetros inválidos en ReservaSala.")
        return True

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0, recargo=0.0):
        horas = self.validar_duracion(duracion)
        costo_base = self.tarifa_hora * horas
        # Si incluye equipamiento audiovisual o supera 20 personas, incrementa un 10% el costo base
        if self._incluye_equipamiento or self._capacidad > 20:
            costo_base *= 1.10
        return self.aplicar_ajustes_sobrecargados(costo_base, impuesto, descuento, recargo)

    def describir_servicio(self):
        texto_estado = "Disponible" if self.disponible else "No Disponible"
        texto_equipamiento = "Con Equipamiento" if self._incluye_equipamiento else "Estándar"
        return (
            f"[Sala {self.id}] {self.nombre} | Capacidad: {self.capacidad} personas ({texto_equipamiento}) | "
            f"Tarifa/hora: ${self.tarifa_hora:,.2f} | {texto_estado}"
        )


class AlquilerEquipo(Servicio):
    """
    AUTOR:  "Agente Antigravity"
    COMMIT: "Implementación de subclase AlquilerEquipo con cantidad de equipos y gama"
    FECHA:  "2026-11-20 09:53"
    VERSION:
    """

    def __init__(self, id_servicio, nombre, tarifa_hora, cantidad_equipos=1, gama="Estandar", disponible=True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        self._cantidad_equipos = 1
        self._gama = "Estandar"
        self.cantidad_equipos = cantidad_equipos
        self.gama = gama
        self.validar_parametros()

    @property
    def cantidad_equipos(self):
        return self._cantidad_equipos

    @cantidad_equipos.setter
    def cantidad_equipos(self, nueva_cantidad):
        if nueva_cantidad is None or str(nueva_cantidad).strip() == "":
            raise ParametroFaltanteError("La cantidad de equipos es obligatoria.")
        try:
            valor_cantidad = int(nueva_cantidad)
        except (ValueError, TypeError) as error_original:
            raise ServicioInvalidoError(
                f"La cantidad de equipos '{nueva_cantidad}' debe ser un número entero."
            ) from error_original
        if valor_cantidad <= 0:
            raise ServicioInvalidoError(
                f"La cantidad de equipos debe ser mayor a 0 (recibido: {valor_cantidad})."
            )
        self._cantidad_equipos = valor_cantidad

    @property
    def gama(self):
        return self._gama

    @gama.setter
    def gama(self, nueva_gama):
        if nueva_gama is None or str(nueva_gama).strip() == "":
            raise ParametroFaltanteError("La gama del equipo es obligatoria.")
        gama_limpia = str(nueva_gama).strip().capitalize()
        if gama_limpia not in ("Estandar", "Estándar", "Alta"):
            raise ServicioInvalidoError(f"La gama '{nueva_gama}' no es válida. Use 'Estandar' o 'Alta'.")
        self._gama = "Alta" if gama_limpia == "Alta" else "Estandar"

    def validar_parametros(self):
        if self._cantidad_equipos <= 0 or self._tarifa_hora <= 0:
            raise ServicioInvalidoError("Parámetros inválidos en AlquilerEquipo.")
        return True

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0, recargo=0.0):
        horas = self.validar_duracion(duracion)
        factor_gama = 1.25 if self._gama == "Alta" else 1.0
        costo_base = (self.tarifa_hora * horas * self._cantidad_equipos) * factor_gama
        return self.aplicar_ajustes_sobrecargados(costo_base, impuesto, descuento, recargo)

    def describir_servicio(self):
        texto_estado = "Disponible" if self.disponible else "No Disponible"
        return (
            f"[Equipo {self.id}] {self.nombre} | Cantidad: {self.cantidad_equipos} | Gama: {self.gama} | "
            f"Tarifa/hora: ${self.tarifa_hora:,.2f} | {texto_estado}"
        )


class AsesoriaEspecializada(Servicio):
    """
    AUTOR:  "Agente Antigravity"
    COMMIT: "Implementación de subclase AsesoriaEspecializada con especialidad y nivel de experto"
    FECHA:  "2026-11-20 09:53"
    VERSION:
    """

    FACTORES_NIVEL = {
        "Junior": 1.0,
        "Senior": 1.30,
        "Master": 1.60,
    }

    def __init__(self, id_servicio, nombre, tarifa_hora, especialidad, nivel_experto="Senior", disponible=True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        self._especialidad = ""
        self._nivel_experto = "Senior"
        self.especialidad = especialidad
        self.nivel_experto = nivel_experto
        self.validar_parametros()

    @property
    def especialidad(self):
        return self._especialidad

    @especialidad.setter
    def especialidad(self, nueva_especialidad):
        if nueva_especialidad is None or str(nueva_especialidad).strip() == "":
            raise ParametroFaltanteError("La especialidad de la asesoría es obligatoria.")
        self._especialidad = str(nueva_especialidad).strip()

    @property
    def nivel_experto(self):
        return self._nivel_experto

    @nivel_experto.setter
    def nivel_experto(self, nuevo_nivel):
        if nuevo_nivel is None or str(nuevo_nivel).strip() == "":
            raise ParametroFaltanteError("El nivel del experto es obligatorio.")
        texto_nivel = str(nuevo_nivel).strip().capitalize()
        if texto_nivel not in self.FACTORES_NIVEL:
            raise ServicioInvalidoError(
                f"Nivel de experto '{nuevo_nivel}' inválido. Opciones válidas: Junior, Senior, Master."
            )
        self._nivel_experto = texto_nivel

    def validar_parametros(self):
        if not self._especialidad or self._nivel_experto not in self.FACTORES_NIVEL:
            raise ServicioInvalidoError("Parámetros inválidos en AsesoriaEspecializada.")
        return True

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0, recargo=0.0):
        horas = self.validar_duracion(duracion)
        factor_experto = self.FACTORES_NIVEL[self._nivel_experto]
        costo_base = (self.tarifa_hora * horas) * factor_experto
        return self.aplicar_ajustes_sobrecargados(costo_base, impuesto, descuento, recargo)

    def describir_servicio(self):
        texto_estado = "Disponible" if self.disponible else "No Disponible"
        return (
            f"[Asesoría {self.id}] {self.nombre} | Especialidad: {self.especialidad} ({self.nivel_experto}) | "
            f"Tarifa/hora: ${self.tarifa_hora:,.2f} | {texto_estado}"
        )


# =====================================================================
# 5. CLASE RESERVA: INTEGRACIÓN Y CICLO DE VIDA (RF-05)
# =====================================================================

class Reserva(EntidadGeneral):
    """
    AUTOR:  "Miguel Parra"
    COMMIT: "Implementación de clase Reserva con estados (Pendiente, Confirmada, Cancelada) y métodos operativos"
    FECHA:  "2026-11-20 09:53"
    VERSION:
    """

    ESTADOS_VALIDOS = ("Pendiente", "Confirmada", "Cancelada")

    def __init__(self, id_reserva, cliente, servicio, duracion):
        super().__init__(id_reserva)
        if not isinstance(cliente, Cliente):
            raise ReservaError("La reserva requiere un objeto válido de tipo Cliente.")
        if not isinstance(servicio, Servicio):
            raise ReservaError("La reserva requiere un objeto válido de tipo Servicio.")

        if duracion is None or str(duracion).strip() == "":
            raise ParametroFaltanteError("La duración de la reserva es obligatoria.")
        try:
            horas_reserva = float(duracion)
        except (ValueError, TypeError) as error_original:
            raise CalculoInconsistenteError(
                f"La duración '{duracion}' debe ser un número válido."
            ) from error_original
        if horas_reserva <= 0:
            raise CalculoInconsistenteError(
                f"La duración de la reserva debe ser mayor a 0 horas (recibido: {horas_reserva})."
            )

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = horas_reserva
        self._estado = "Pendiente"
        self._costo_total = 0.0
        self.validar_datos()

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    def validar_datos(self):
        if self._duracion <= 0:
            raise CalculoInconsistenteError("La duración de la reserva es inconsistente.")
        if self._estado not in self.ESTADOS_VALIDOS:
            raise ReservaError(f"Estado de reserva desconocido: {self._estado}.")
        return True

    def procesar(self, impuesto=0.0, descuento=0.0, recargo=0.0):
        """
        Verifica disponibilidad del servicio y calcula el costo total polimórfico
        sobrecargado con impuestos, descuentos o recargos.
        """
        if self._estado == "Cancelada":
            raise OperacionNoPermitidaError(
                f"No se puede procesar la reserva '{self.id}' porque está Cancelada."
            )
        if not self._servicio.disponible and self._estado == "Pendiente":
            raise ServicioNoDisponibleError(
                f"El servicio '{self._servicio.nombre}' ({self._servicio.id}) no está disponible actualmente."
            )

        self._costo_total = self._servicio.calcular_costo(
            self._duracion,
            impuesto=impuesto,
            descuento=descuento,
            recargo=recargo,
        )
        return self._costo_total

    def confirmar(self):
        """Confirma una reserva pendiente y marca el servicio como no disponible."""
        if self._estado == "Cancelada":
            raise OperacionNoPermitidaError(
                f"No es posible confirmar la reserva '{self.id}' porque ya fue Cancelada."
            )
        if self._estado == "Confirmada":
            raise OperacionNoPermitidaError(
                f"La reserva '{self.id}' ya se encuentra Confirmada."
            )
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"No se puede confirmar la reserva '{self.id}': el servicio '{self._servicio.nombre}' no está disponible."
            )

        if self._costo_total <= 0:
            self.procesar()

        self._estado = "Confirmada"
        self._servicio.disponible = False
        return self._estado

    def cancelar(self):
        """Cancela una reserva activa o pendiente y libera la disponibilidad del servicio."""
        if self._estado == "Cancelada":
            raise OperacionNoPermitidaError(
                f"La reserva '{self.id}' ya se encuentra Cancelada."
            )

        self._estado = "Cancelada"
        self._servicio.disponible = True
        return self._estado

    def obtener_resumen(self):
        return (
            f"Reserva [{self.id}] | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} ({self.duracion}h) | "
            f"Costo: ${self.costo_total:,.2f} | Estado: {self.estado}"
        )
