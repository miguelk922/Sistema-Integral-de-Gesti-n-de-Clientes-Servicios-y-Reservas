from modelos import (
    ExcepcionSistema,
    DatosInvalidosError,
    ClienteInvalidoError,
    ServicioInvalidoError,
    ParametroFaltanteError,
    OperacionNoPermitidaError,
    ReservaError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
    EntidadGeneral,
    Cliente,
    Servicio,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
    Reserva,
)

"""
AUTOR:  "Agente Antigravity"
COMMIT: "Implementación de Capa 2 (gestor_sistema.py) en Python puro importando únicamente modelos.py: memoria, logs, encadenamiento de excepciones y simulador"
FECHA:  "2026-11-20 10:24"
VERSION:
"""

class GestorSistema:
    """
    AUTOR:  "Miguel Parra"
    COMMIT: "Creación de clase GestorSistema con listas en memoria, auditoría en archivo .log, bloques try/except/else/finally y simulador de operaciones"
    FECHA:  "2026-11-20 16:14"
    VERSION:
    """

    def __init__(self, nombre_archivo_log="eventos_y_errores.log"):
        self._clientes = []
        self._servicios = []
        self._reservas = []
        self._contador_eventos = 0
        self._total_operaciones = 0
        self._operacion_activa = False

        # Resolución de ruta en Python puro sin usar la librería os
        ruta_modulo = __file__.replace("\\", "/")
        if "/" in ruta_modulo:
            directorio_base = ruta_modulo.rsplit("/", 1)[0]
            self._ruta_archivo_log = f"{directorio_base}/{nombre_archivo_log}"
        else:
            self._ruta_archivo_log = nombre_archivo_log

        self._inicializar_archivo_log()

    # =====================================================================
    # 1. PROPIEDADES Y CONSULTA DE LISTAS EN MEMORIA (RNF-01)
    # =====================================================================

    @property
    def clientes(self):
        return list(self._clientes)

    @property
    def servicios(self):
        return list(self._servicios)

    @property
    def reservas(self):
        return list(self._reservas)

    @property
    def total_operaciones(self):
        return self._total_operaciones

    def obtener_clientes(self):
        """Retorna la lista actual de clientes en memoria."""
        return list(self._clientes)

    def obtener_servicios(self):
        """Retorna la lista actual de servicios en memoria."""
        return list(self._servicios)

    def obtener_reservas(self):
        """Retorna la lista actual de reservas en memoria."""
        return list(self._reservas)

    def buscar_cliente(self, id_cliente):
        """Busca un cliente por su ID en la lista en memoria."""
        if id_cliente is None:
            return None
        id_buscado = str(id_cliente).strip()
        for cliente in self._clientes:
            if cliente.id == id_buscado:
                return cliente
        return None

    def buscar_servicio(self, id_servicio):
        """Busca un servicio por su ID en la lista en memoria."""
        if id_servicio is None:
            return None
        id_buscado = str(id_servicio).strip()
        for servicio in self._servicios:
            if servicio.id == id_buscado:
                return servicio
        return None

    def buscar_reserva(self, id_reserva):
        """Busca una reserva por su ID en la lista en memoria."""
        if id_reserva is None:
            return None
        id_buscado = str(id_reserva).strip()
        for reserva in self._reservas:
            if reserva.id == id_buscado:
                return reserva
        return None

    # =====================================================================
    # 2. SISTEMA DE AUDITORÍA Y ARCHIVO DE LOGS (RNF-03)
    # =====================================================================

    def _inicializar_archivo_log(self):
        """Verifica o crea el archivo de log sin detener el sistema ante fallos de disco."""
        try:
            archivo = open(self._ruta_archivo_log, "a", encoding="utf-8")
            archivo.close()
        except Exception:
            pass

    def _obtener_marca_evento(self):
        """Genera un identificador secuencial de evento sin depender de datetime."""
        self._contador_eventos += 1
        return f"Evento #{self._contador_eventos:04d}"

    def registrar_evento_log(self, operacion, detalle):
        """Escribe un evento exitoso en eventos_y_errores.log con protección try/except."""
        marca = self._obtener_marca_evento()
        linea_log = f"[{marca}] [EXITO] [{operacion}] {detalle}\n"
        try:
            with open(self._ruta_archivo_log, "a", encoding="utf-8") as archivo_log:
                archivo_log.write(linea_log)
        except Exception:
            pass

    def registrar_error_log(self, operacion, error_encadenado):
        """
        Escribe un error y su traza de encadenamiento (__cause__) en
        eventos_y_errores.log sin usar librerías externas.
        """
        marca = self._obtener_marca_evento()
        tipo_error = type(error_encadenado).__name__
        mensaje_error = str(error_encadenado)

        causa = error_encadenado.__cause__
        if causa is not None:
            tipo_causa = type(causa).__name__
            mensaje_causa = str(causa)
            linea_traza = None
            if causa.__traceback__ is not None:
                linea_traza = causa.__traceback__.tb_lineno
            detalle_causa = f"Causa raíz ({tipo_causa}"
            if linea_traza is not None:
                detalle_causa += f", línea {linea_traza}"
            detalle_causa += f"): {mensaje_causa}"
        else:
            detalle_causa = "Sin causa encadenada adicional"

        linea_log = (
            f"[{marca}] [ERROR] [{operacion}] {tipo_error}: {mensaje_error} "
            f"| Traza -> {detalle_causa}\n"
        )
        try:
            with open(self._ruta_archivo_log, "a", encoding="utf-8") as archivo_log:
                archivo_log.write(linea_log)
        except Exception:
            pass

    def leer_archivo_log(self):
        """Lee y retorna el contenido completo del archivo de logs para la interfaz."""
        try:
            with open(self._ruta_archivo_log, "r", encoding="utf-8") as archivo_log:
                contenido = archivo_log.read()
                if contenido.strip() == "":
                    return "El archivo de registro (eventos_y_errores.log) está vacío actualmente."
                return contenido
        except Exception as error_lectura:
            return f"No fue posible leer el archivo de logs: {error_lectura}"

    # =====================================================================
    # 3. OPERACIONES DE NEGOCIO CON TRY / EXCEPT / ELSE / FINALLY (RNF-02)
    # =====================================================================

    def _encadenar_y_registrar_error(self, nombre_operacion, causa_original):
        """
        Aplica encadenamiento explícito de excepciones (raise ... from ...)
        y registra el error resultante en el archivo de auditoría.
        """
        try:
            raise ExcepcionSistema(
                f"Error en '{nombre_operacion}': {causa_original}"
            ) from causa_original
        except ExcepcionSistema as error_encadenado:
            self.registrar_error_log(nombre_operacion, error_encadenado)
            return str(error_encadenado)

    def registrar_cliente(self, id_cliente, nombre, documento, correo, telefono):
        """
        Registra un nuevo cliente validando duplicados y reglas de dominio
        mediante estructura completa try/except/else/finally.
        """
        nombre_operacion = "REGISTRAR_CLIENTE"
        self._operacion_activa = True
        exito = False
        mensaje = ""
        nuevo_cliente = None

        try:
            if id_cliente is not None and self.buscar_cliente(id_cliente) is not None:
                raise OperacionNoPermitidaError(
                    f"Ya existe un cliente registrado con el ID '{str(id_cliente).strip()}'."
                )
            for cliente_existente in self._clientes:
                if documento is not None and cliente_existente.documento == str(documento).strip():
                    raise OperacionNoPermitidaError(
                        f"Ya existe un cliente con el número de documento '{str(documento).strip()}'."
                    )

            nuevo_cliente = Cliente(
                id_cliente=id_cliente,
                nombre=nombre,
                documento=documento,
                correo=correo,
                telefono=telefono,
            )
        except (ExcepcionSistema, Exception) as causa_original:
            mensaje = self._encadenar_y_registrar_error(nombre_operacion, causa_original)
        else:
            self._clientes.append(nuevo_cliente)
            resumen = nuevo_cliente.obtener_resumen()
            self.registrar_evento_log(nombre_operacion, f"Registro exitoso -> {resumen}")
            exito = True
            mensaje = f"Cliente '{nuevo_cliente.nombre}' registrado correctamente."
        finally:
            self._operacion_activa = False
            self._total_operaciones += 1

        return {"exito": exito, "mensaje": mensaje, "datos": nuevo_cliente}

    def crear_servicio(
        self,
        tipo_servicio,
        id_servicio,
        nombre,
        tarifa_hora,
        parametro_principal=None,
        parametro_secundario=None,
        disponible=True,
    ):
        """
        Crea e instancia polimórficamente una subclase de Servicio
        ('Sala', 'Equipo' o 'Asesoria') con bloque try/except/else/finally.
        """
        nombre_operacion = "CREAR_SERVICIO"
        self._operacion_activa = True
        exito = False
        mensaje = ""
        nuevo_servicio = None

        try:
            if tipo_servicio is None or str(tipo_servicio).strip() == "":
                raise ParametroFaltanteError("El tipo de servicio es obligatorio (Sala, Equipo o Asesoria).")
            if id_servicio is not None and self.buscar_servicio(id_servicio) is not None:
                raise OperacionNoPermitidaError(
                    f"Ya existe un servicio registrado con el ID '{str(id_servicio).strip()}'."
                )

            tipo_normalizado = str(tipo_servicio).strip().lower()

            if tipo_normalizado in ("sala", "reservasala", "reserva de sala"):
                incluye_equipo = False
                if isinstance(parametro_secundario, bool):
                    incluye_equipo = parametro_secundario
                elif parametro_secundario is not None:
                    incluye_equipo = str(parametro_secundario).strip().lower() in (
                        "true", "1", "si", "sí", "con equipamiento"
                    )
                nuevo_servicio = ReservaSala(
                    id_servicio=id_servicio,
                    nombre=nombre,
                    tarifa_hora=tarifa_hora,
                    capacidad=parametro_principal,
                    incluye_equipamiento=incluye_equipo,
                    disponible=disponible,
                )
            elif tipo_normalizado in ("equipo", "alquilerequipo", "alquiler de equipo"):
                gama_equipo = "Estandar" if parametro_secundario is None or str(parametro_secundario).strip() == "" else parametro_secundario
                cantidad = 1 if parametro_principal is None or str(parametro_principal).strip() == "" else parametro_principal
                nuevo_servicio = AlquilerEquipo(
                    id_servicio=id_servicio,
                    nombre=nombre,
                    tarifa_hora=tarifa_hora,
                    cantidad_equipos=cantidad,
                    gama=gama_equipo,
                    disponible=disponible,
                )
            elif tipo_normalizado in ("asesoria", "asesoría", "asesoriaespecializada", "asesoría especializada"):
                nivel = "Senior" if parametro_secundario is None or str(parametro_secundario).strip() == "" else parametro_secundario
                nuevo_servicio = AsesoriaEspecializada(
                    id_servicio=id_servicio,
                    nombre=nombre,
                    tarifa_hora=tarifa_hora,
                    especialidad=parametro_principal,
                    nivel_experto=nivel,
                    disponible=disponible,
                )
            else:
                raise ServicioInvalidoError(
                    f"El tipo de servicio '{tipo_servicio}' no es reconocido. Use 'Sala', 'Equipo' o 'Asesoria'."
                )
        except (ExcepcionSistema, Exception) as causa_original:
            mensaje = self._encadenar_y_registrar_error(nombre_operacion, causa_original)
        else:
            self._servicios.append(nuevo_servicio)
            descripcion = nuevo_servicio.describir_servicio()
            self.registrar_evento_log(nombre_operacion, f"Servicio creado -> {descripcion}")
            exito = True
            mensaje = f"Servicio '{nuevo_servicio.nombre}' creado correctamente."
        finally:
            self._operacion_activa = False
            self._total_operaciones += 1

        return {"exito": exito, "mensaje": mensaje, "datos": nuevo_servicio}

    def crear_reserva(
        self,
        id_reserva,
        id_cliente,
        id_servicio,
        duracion,
        impuesto=0.0,
        descuento=0.0,
        recargo=0.0,
    ):
        """
        Localiza cliente y servicio en memoria, instancia la Reserva y ejecuta
        su procesamiento polimórfico sobrecargado con try/except/else/finally.
        """
        nombre_operacion = "CREAR_PROCESAR_RESERVA"
        self._operacion_activa = True
        exito = False
        mensaje = ""
        nueva_reserva = None

        try:
            if id_reserva is not None and self.buscar_reserva(id_reserva) is not None:
                raise OperacionNoPermitidaError(
                    f"Ya existe una reserva registrada con el ID '{str(id_reserva).strip()}'."
                )
            if id_cliente is None or str(id_cliente).strip() == "":
                raise ParametroFaltanteError("Debe seleccionar o indicar el ID del cliente.")
            if id_servicio is None or str(id_servicio).strip() == "":
                raise ParametroFaltanteError("Debe seleccionar o indicar el ID del servicio.")

            cliente_encontrado = self.buscar_cliente(id_cliente)
            if cliente_encontrado is None:
                raise ReservaError(f"No existe ningún cliente registrado con el ID '{id_cliente}'.")

            servicio_encontrado = self.buscar_servicio(id_servicio)
            if servicio_encontrado is None:
                raise ReservaError(f"No existe ningún servicio registrado con el ID '{id_servicio}'.")

            nueva_reserva = Reserva(
                id_reserva=id_reserva,
                cliente=cliente_encontrado,
                servicio=servicio_encontrado,
                duracion=duracion,
            )
            nueva_reserva.procesar(
                impuesto=impuesto,
                descuento=descuento,
                recargo=recargo,
            )
        except (ExcepcionSistema, Exception) as causa_original:
            mensaje = self._encadenar_y_registrar_error(nombre_operacion, causa_original)
        else:
            self._reservas.append(nueva_reserva)
            resumen = nueva_reserva.obtener_resumen()
            self.registrar_evento_log(nombre_operacion, f"Reserva procesada -> {resumen}")
            exito = True
            mensaje = (
                f"Reserva '{nueva_reserva.id}' creada y procesada. "
                f"Costo calculado: ${nueva_reserva.costo_total:,.2f}"
            )
        finally:
            self._operacion_activa = False
            self._total_operaciones += 1

        return {"exito": exito, "mensaje": mensaje, "datos": nueva_reserva}

    def confirmar_reserva(self, id_reserva):
        """
        Confirma una reserva existente en memoria y bloquea la disponibilidad
        del servicio asociado usando try/except/else/finally.
        """
        nombre_operacion = "CONFIRMAR_RESERVA"
        self._operacion_activa = True
        exito = False
        mensaje = ""
        reserva_encontrada = None

        try:
            if id_reserva is None or str(id_reserva).strip() == "":
                raise ParametroFaltanteError("El ID de la reserva a confirmar es obligatorio.")
            reserva_encontrada = self.buscar_reserva(id_reserva)
            if reserva_encontrada is None:
                raise ReservaError(f"No se encontró ninguna reserva con el ID '{id_reserva}'.")

            reserva_encontrada.confirmar()
        except (ExcepcionSistema, Exception) as causa_original:
            mensaje = self._encadenar_y_registrar_error(nombre_operacion, causa_original)
        else:
            resumen = reserva_encontrada.obtener_resumen()
            self.registrar_evento_log(nombre_operacion, f"Reserva confirmada -> {resumen}")
            exito = True
            mensaje = f"Reserva '{reserva_encontrada.id}' confirmada exitosamente."
        finally:
            self._operacion_activa = False
            self._total_operaciones += 1

        return {"exito": exito, "mensaje": mensaje, "datos": reserva_encontrada}

    def cancelar_reserva(self, id_reserva):
        """
        Cancela una reserva existente en memoria y libera la disponibilidad
        del servicio asociado usando try/except/else/finally.
        """
        nombre_operacion = "CANCELAR_RESERVA"
        self._operacion_activa = True
        exito = False
        mensaje = ""
        reserva_encontrada = None

        try:
            if id_reserva is None or str(id_reserva).strip() == "":
                raise ParametroFaltanteError("El ID de la reserva a cancelar es obligatorio.")
            reserva_encontrada = self.buscar_reserva(id_reserva)
            if reserva_encontrada is None:
                raise ReservaError(f"No se encontró ninguna reserva con el ID '{id_reserva}'.")

            reserva_encontrada.cancelar()
        except (ExcepcionSistema, Exception) as causa_original:
            mensaje = self._encadenar_y_registrar_error(nombre_operacion, causa_original)
        else:
            resumen = reserva_encontrada.obtener_resumen()
            self.registrar_evento_log(nombre_operacion, f"Reserva cancelada -> {resumen}")
            exito = True
            mensaje = f"Reserva '{reserva_encontrada.id}' cancelada y servicio liberado."
        finally:
            self._operacion_activa = False
            self._total_operaciones += 1

        return {"exito": exito, "mensaje": mensaje, "datos": reserva_encontrada}

    # =====================================================================
    # 4. SIMULADOR AUTOMÁTICO DE OPERACIONES (RNF-04: >= 10 OPERACIONES)
    # =====================================================================

    def ejecutar_simulacion(self):
        """
        Ejecuta una batería automática de 12 operaciones mixtas (casos válidos,
        datos inválidos, parámetros faltantes, servicios no disponibles,
        cálculos inconsistentes y operaciones no permitidas), demostrando
        que el sistema registra cada evento/error y continúa funcionando.
        """
        resultados_simulacion = []
        sufijo = self._total_operaciones + 1

        id_cli_1 = f"SIM-C{sufijo}01"
        id_cli_2 = f"SIM-C{sufijo}02"
        doc_cli_1 = f"1000{sufijo}01"
        doc_cli_2 = f"1000{sufijo}02"

        id_srv_sala = f"SIM-S{sufijo}01"
        id_srv_equipo = f"SIM-S{sufijo}02"
        id_srv_asesoria = f"SIM-S{sufijo}03"

        id_res_1 = f"SIM-R{sufijo}01"
        id_res_2 = f"SIM-R{sufijo}02"

        self.registrar_evento_log(
            "SIMULADOR",
            "=== INICIO DE BATERÍA DE SIMULACIÓN (12 OPERACIONES MIXTAS) ===",
        )

        # Operación 1 (VÁLIDA): Registro de Cliente 1
        res_1 = self.registrar_cliente(
            id_cliente=id_cli_1,
            nombre="Laura Gómez",
            documento=doc_cli_1,
            correo="laura.gomez@softwarefj.com",
            telefono="3104567890",
        )
        resultados_simulacion.append(("1. Registro Cliente Válido (Laura Gómez)", res_1))

        # Operación 2 (VÁLIDA): Registro de Cliente 2
        res_2 = self.registrar_cliente(
            id_cliente=id_cli_2,
            nombre="Carlos Mendoza",
            documento=doc_cli_2,
            correo="carlos.mendoza@empresa.co",
            telefono="3159876543",
        )
        resultados_simulacion.append(("2. Registro Cliente Válido (Carlos Mendoza)", res_2))

        # Operación 3 (INVÁLIDA - ClienteInvalidoError): Correo sin formato válido
        res_3 = self.registrar_cliente(
            id_cliente=f"SIM-C{sufijo}99",
            nombre="Pedro Error",
            documento=f"9999{sufijo}99",
            correo="correo_invalido_sin_arroba",
            telefono="3001112233",
        )
        resultados_simulacion.append(("3. Registro Cliente Inválido (Correo mal formado)", res_3))

        # Operación 4 (INVÁLIDA - ParametroFaltanteError): Nombre vacío
        res_4 = self.registrar_cliente(
            id_cliente=f"SIM-C{sufijo}98",
            nombre="   ",
            documento=f"8888{sufijo}88",
            correo="vacio@test.com",
            telefono="3004445566",
        )
        resultados_simulacion.append(("4. Registro Cliente Inválido (Nombre faltante)", res_4))

        # Operación 5 (VÁLIDA): Creación de Servicio ReservaSala
        res_5 = self.crear_servicio(
            tipo_servicio="Sala",
            id_servicio=id_srv_sala,
            nombre="Sala Ejecutiva Orion",
            tarifa_hora=80000,
            parametro_principal=25,
            parametro_secundario=True,
        )
        resultados_simulacion.append(("5. Creación Servicio Sala Válido", res_5))

        # Operación 6 (VÁLIDA): Creación de Servicio AlquilerEquipo
        res_6 = self.crear_servicio(
            tipo_servicio="Equipo",
            id_servicio=id_srv_equipo,
            nombre="Estación Workstation Pro",
            tarifa_hora=45000,
            parametro_principal=3,
            parametro_secundario="Alta",
        )
        resultados_simulacion.append(("6. Creación Servicio Equipo Válido", res_6))

        # Operación 7 (VÁLIDA): Creación de Servicio AsesoriaEspecializada
        res_7 = self.crear_servicio(
            tipo_servicio="Asesoria",
            id_servicio=id_srv_asesoria,
            nombre="Arquitectura Cloud y Seguridad",
            tarifa_hora=120000,
            parametro_principal="Ciberseguridad",
            parametro_secundario="Master",
        )
        resultados_simulacion.append(("7. Creación Servicio Asesoría Válido", res_7))

        # Operación 8 (INVÁLIDA - ServicioInvalidoError): Tarifa negativa
        res_8 = self.crear_servicio(
            tipo_servicio="Sala",
            id_servicio=f"SIM-S{sufijo}99",
            nombre="Sala con Tarifa Negativa",
            tarifa_hora=-50000,
            parametro_principal=10,
            parametro_secundario=False,
        )
        resultados_simulacion.append(("8. Creación Servicio Inválido (Tarifa negativa)", res_8))

        # Operación 9 (VÁLIDA): Crear y procesar Reserva con sobrecarga (impuesto 19%, descuento 10%)
        res_9 = self.crear_reserva(
            id_reserva=id_res_1,
            id_cliente=id_cli_1,
            id_servicio=id_srv_sala,
            duracion=4,
            impuesto=19.0,
            descuento=10.0,
            recargo=0.0,
        )
        resultados_simulacion.append(("9. Creación Reserva Válida (Con Impuesto y Descuento)", res_9))

        # Operación 10 (VÁLIDA): Confirmar Reserva 1 (bloquea disponibilidad de la sala)
        res_10 = self.confirmar_reserva(id_res_1)
        resultados_simulacion.append(("10. Confirmación de Reserva Válida", res_10))

        # Operación 11 (FALLIDA - ServicioNoDisponibleError): Intentar reservar sala ya ocupada
        res_11 = self.crear_reserva(
            id_reserva=id_res_2,
            id_cliente=id_cli_2,
            id_servicio=id_srv_sala,
            duracion=2,
            impuesto=19.0,
            descuento=0.0,
        )
        resultados_simulacion.append(("11. Reserva Fallida (Servicio no disponible)", res_11))

        # Operación 12 (FALLIDA - CalculoInconsistenteError): Descuento mayor al 100%
        res_12 = self.crear_reserva(
            id_reserva=f"SIM-R{sufijo}99",
            id_cliente=id_cli_2,
            id_servicio=id_srv_equipo,
            duracion=3,
            impuesto=19.0,
            descuento=150.0,
        )
        resultados_simulacion.append(("12. Reserva Fallida (Descuento inconsistente > 100%)", res_12))

        total_exitosas = sum(1 for _, resultado in resultados_simulacion if resultado["exito"])
        total_controladas = len(resultados_simulacion) - total_exitosas

        self.registrar_evento_log(
            "SIMULADOR",
            f"=== FIN DE SIMULACIÓN: {len(resultados_simulacion)} operaciones ejecutadas "
            f"({total_exitosas} exitosas, {total_controladas} errores controlados) ===",
        )

        return {
            "total_ejecutadas": len(resultados_simulacion),
            "exitosas": total_exitosas,
            "errores_controlados": total_controladas,
            "detalle_operaciones": resultados_simulacion,
        }
