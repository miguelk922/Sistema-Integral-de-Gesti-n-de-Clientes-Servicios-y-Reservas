"""
AUTOR:  "Agente Antigravity"
COMMIT: "Implementación de Capa 3 (Software_FJ.py): interfaz gráfica en Tkinter con 4 pestañas, visor de logs en vivo y conexión unidireccional con GestorSistema"
FECHA:  "2026-11-20 10:32"
VERSION:
"""

# NECESITO MEJORAR CON TKINTER ME CUESTA MUCHO TRABAJAR CON TKINTER, (Antigravity hizo todo el codigo de tkiter y lo mantendre tal cual.)

import tkinter as tk
from tkinter import ttk, messagebox
from gestor_sistema import GestorSistema


class AplicacionSoftwareFJ:
    """
    AUTOR:  "Agente Antigravity"
    COMMIT: "Construcción de ventana principal AplicacionSoftwareFJ con pestañas de Clientes, Servicios, Reservas, Simulación y visor de auditoría"
    FECHA:  "2026-11-20 10:32"
    VERSION:
    """

    def __init__(self, ventana_raiz):
        self.ventana = ventana_raiz
        self.ventana.title("Software FJ — Sistema Integral de Gestión de Clientes, Servicios y Reservas")
        self.ventana.geometry("1120x780")
        self.ventana.minsize(980, 680)

        # Instancia única del cerebro operativo (Capa 2)
        self.gestor = GestorSistema()

        self._configurar_estilos()
        self._construir_encabezado()
        self._construir_contenedor_principal()
        self._construir_visor_logs()

        # Carga inicial de tablas y visor de logs
        self.actualizar_todo()

    def _configurar_estilos(self):
        """Configura estilos visuales limpios usando únicamente ttk base."""
        estilo = ttk.Style()
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure("TFrame", background="#f4f6f9")
        estilo.configure("TLabelframe", background="#f4f6f9")
        estilo.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"), foreground="#1a365d")
        estilo.configure("TLabel", background="#f4f6f9", font=("Segoe UI", 9))
        estilo.configure("Titulo.TLabel", background="#1a365d", foreground="#ffffff", font=("Segoe UI", 14, "bold"))
        estilo.configure("Subtitulo.TLabel", background="#1a365d", foreground="#dbeafe", font=("Segoe UI", 9))
        estilo.configure("TButton", font=("Segoe UI", 9, "bold"), padding=5)
        estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        estilo.configure("Treeview", rowheight=24, font=("Segoe UI", 9))

    def _construir_encabezado(self):
        """Construye la barra superior informativa de la aplicación."""
        marco_encabezado = tk.Frame(self.ventana, bg="#1a365d", padx=15, pady=10)
        marco_encabezado.pack(fill="x")

        etiqueta_titulo = ttk.Label(
            marco_encabezado,
            text="SOFTWARE FJ — Módulo Central de Gestión en Memoria (POO)",
            style="Titulo.TLabel",
        )
        etiqueta_titulo.pack(anchor="w")

        etiqueta_subtitulo = ttk.Label(
            marco_encabezado,
            text="Gestión tolerante a fallos de Clientes, Servicios (Salas, Equipos, Asesorías) y Reservas con Auditoría en Tiempo Real",
            style="Subtitulo.TLabel",
        )
        etiqueta_subtitulo.pack(anchor="w")

    def _construir_contenedor_principal(self):
        """Crea el cuaderno de 4 pestañas principales."""
        marco_central = ttk.Frame(self.ventana, padding=8)
        marco_central.pack(fill="both", expand=True)

        self.cuaderno = ttk.Notebook(marco_central)
        self.cuaderno.pack(fill="both", expand=True)

        self.pestana_clientes = ttk.Frame(self.cuaderno, padding=10)
        self.pestana_servicios = ttk.Frame(self.cuaderno, padding=10)
        self.pestana_reservas = ttk.Frame(self.cuaderno, padding=10)
        self.pestana_simulacion = ttk.Frame(self.cuaderno, padding=10)

        self.cuaderno.add(self.pestana_clientes, text="  1. Gestión de Clientes  ")
        self.cuaderno.add(self.pestana_servicios, text="  2. Gestión de Servicios  ")
        self.cuaderno.add(self.pestana_reservas, text="  3. Gestión de Reservas  ")
        self.cuaderno.add(self.pestana_simulacion, text="  4. Panel de Simulación  ")

        self._construir_pestana_clientes()
        self._construir_pestana_servicios()
        self._construir_pestana_reservas()
        self._construir_pestana_simulacion()

    # =====================================================================
    # PESTAÑA 1: GESTIÓN DE CLIENTES (RF-02)
    # =====================================================================

    def _construir_pestana_clientes(self):
        marco_formulario = ttk.LabelFrame(
            self.pestana_clientes,
            text="Registrar Nuevo Cliente",
            padding=10,
        )
        marco_formulario.pack(fill="x", pady=(0, 8))

        self.var_cliente_id = tk.StringVar(value="CLI-01")
        self.var_cliente_nombre = tk.StringVar()
        self.var_cliente_documento = tk.StringVar()
        self.var_cliente_correo = tk.StringVar()
        self.var_cliente_telefono = tk.StringVar()

        ttk.Label(marco_formulario, text="ID Cliente:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.var_cliente_id, width=16).grid(row=0, column=1, sticky="w", padx=5, pady=4)

        ttk.Label(marco_formulario, text="Nombre Completo:").grid(row=0, column=2, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.var_cliente_nombre, width=28).grid(row=0, column=3, sticky="w", padx=5, pady=4)

        ttk.Label(marco_formulario, text="Documento (solo números):").grid(row=0, column=4, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.var_cliente_documento, width=18).grid(row=0, column=5, sticky="w", padx=5, pady=4)

        ttk.Label(marco_formulario, text="Correo Electrónico:").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.var_cliente_correo, width=28).grid(row=1, column=1, columnspan=2, sticky="we", padx=5, pady=4)

        ttk.Label(marco_formulario, text="Teléfono (mín. 7 dígitos):").grid(row=1, column=3, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.var_cliente_telefono, width=20).grid(row=1, column=4, sticky="w", padx=5, pady=4)

        marco_botones = ttk.Frame(marco_formulario)
        marco_botones.grid(row=1, column=5, sticky="e", padx=5, pady=4)

        ttk.Button(marco_botones, text="Registrar Cliente", command=self.registrar_cliente_ui).pack(side="left", padx=3)
        ttk.Button(marco_botones, text="Limpiar", command=self.limpiar_formulario_cliente).pack(side="left", padx=3)

        # Tabla de clientes en memoria
        marco_tabla = ttk.LabelFrame(self.pestana_clientes, text="Clientes Registrados en Memoria", padding=8)
        marco_tabla.pack(fill="both", expand=True)

        columnas = ("id", "nombre", "documento", "correo", "telefono", "registro")
        self.tabla_clientes = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=10)

        self.tabla_clientes.heading("id", text="ID")
        self.tabla_clientes.heading("nombre", text="Nombre Completo")
        self.tabla_clientes.heading("documento", text="Documento")
        self.tabla_clientes.heading("correo", text="Correo Electrónico")
        self.tabla_clientes.heading("telefono", text="Teléfono")
        self.tabla_clientes.heading("registro", text="Orden Registro")

        self.tabla_clientes.column("id", width=90, anchor="center")
        self.tabla_clientes.column("nombre", width=220)
        self.tabla_clientes.column("documento", width=130, anchor="center")
        self.tabla_clientes.column("correo", width=240)
        self.tabla_clientes.column("telefono", width=130, anchor="center")
        self.tabla_clientes.column("registro", width=110, anchor="center")

        barra_vertical = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla_clientes.yview)
        self.tabla_clientes.configure(yscrollcommand=barra_vertical.set)

        self.tabla_clientes.pack(side="left", fill="both", expand=True)
        barra_vertical.pack(side="right", fill="y")

    def registrar_cliente_ui(self):
        """Captura los datos del formulario de cliente e invoca al gestor."""
        try:
            id_cli = self.var_cliente_id.get()
            nombre = self.var_cliente_nombre.get()
            documento = self.var_cliente_documento.get()
            correo = self.var_cliente_correo.get()
            telefono = self.var_cliente_telefono.get()

            resultado = self.gestor.registrar_cliente(
                id_cliente=id_cli,
                nombre=nombre,
                documento=documento,
                correo=correo,
                telefono=telefono,
            )
        except Exception as error_ui:
            messagebox.showerror("Error en Interfaz", f"Error inesperado al procesar entrada: {error_ui}")
            return

        self.actualizar_todo()
        if resultado["exito"]:
            self.limpiar_formulario_cliente()
            messagebox.showinfo("Registro Exitoso", resultado["mensaje"])
        else:
            messagebox.showwarning("Operación Controlada", resultado["mensaje"])

    def limpiar_formulario_cliente(self):
        siguiente_num = len(self.gestor.obtener_clientes()) + 1
        self.var_cliente_id.set(f"CLI-{siguiente_num:02d}")
        self.var_cliente_nombre.set("")
        self.var_cliente_documento.set("")
        self.var_cliente_correo.set("")
        self.var_cliente_telefono.set("")

    # =====================================================================
    # PESTAÑA 2: GESTIÓN DE SERVICIOS (RF-03 y RF-04)
    # =====================================================================

    def _construir_pestana_servicios(self):
        marco_formulario = ttk.LabelFrame(
            self.pestana_servicios,
            text="Crear Nuevo Servicio en Catálogo (Polimorfismo)",
            padding=10,
        )
        marco_formulario.pack(fill="x", pady=(0, 8))

        self.var_servicio_tipo = tk.StringVar(value="Sala")
        self.var_servicio_id = tk.StringVar(value="SRV-01")
        self.var_servicio_nombre = tk.StringVar()
        self.var_servicio_tarifa = tk.StringVar(value="50000")
        self.var_servicio_param1 = tk.StringVar(value="15")
        self.var_servicio_param2 = tk.StringVar(value="Si")

        ttk.Label(marco_formulario, text="Tipo de Servicio:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.combo_tipo_servicio = ttk.Combobox(
            marco_formulario,
            textvariable=self.var_servicio_tipo,
            values=("Sala", "Equipo", "Asesoria"),
            state="readonly",
            width=16,
        )
        self.combo_tipo_servicio.grid(row=0, column=1, sticky="w", padx=5, pady=4)
        self.combo_tipo_servicio.bind("<<ComboboxSelected>>", self._actualizar_etiquetas_servicio)

        ttk.Label(marco_formulario, text="ID Servicio:").grid(row=0, column=2, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.var_servicio_id, width=16).grid(row=0, column=3, sticky="w", padx=5, pady=4)

        ttk.Label(marco_formulario, text="Nombre del Servicio:").grid(row=0, column=4, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.var_servicio_nombre, width=28).grid(row=0, column=5, sticky="w", padx=5, pady=4)

        ttk.Label(marco_formulario, text="Tarifa por Hora ($):").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.var_servicio_tarifa, width=18).grid(row=1, column=1, sticky="w", padx=5, pady=4)

        self.etiqueta_param1 = ttk.Label(marco_formulario, text="Capacidad (Personas):")
        self.etiqueta_param1.grid(row=1, column=2, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.var_servicio_param1, width=18).grid(row=1, column=3, sticky="w", padx=5, pady=4)

        self.etiqueta_param2 = ttk.Label(marco_formulario, text="¿Incluye Equipamiento?:")
        self.etiqueta_param2.grid(row=1, column=4, sticky="w", padx=5, pady=4)
        self.combo_param2 = ttk.Combobox(
            marco_formulario,
            textvariable=self.var_servicio_param2,
            values=("Si", "No"),
            width=18,
        )
        self.combo_param2.grid(row=1, column=5, sticky="w", padx=5, pady=4)

        marco_botones = ttk.Frame(marco_formulario)
        marco_botones.grid(row=2, column=0, columnspan=6, sticky="e", padx=5, pady=6)

        ttk.Button(marco_botones, text="Crear Servicio", command=self.crear_servicio_ui).pack(side="left", padx=3)
        ttk.Button(marco_botones, text="Limpiar", command=self.limpiar_formulario_servicio).pack(side="left", padx=3)

        # Tabla de servicios
        marco_tabla = ttk.LabelFrame(self.pestana_servicios, text="Catálogo de Servicios en Memoria", padding=8)
        marco_tabla.pack(fill="both", expand=True)

        columnas = ("id", "tipo", "nombre", "tarifa", "disponible", "descripcion")
        self.tabla_servicios = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=10)

        self.tabla_servicios.heading("id", text="ID")
        self.tabla_servicios.heading("tipo", text="Categoría")
        self.tabla_servicios.heading("nombre", text="Nombre del Servicio")
        self.tabla_servicios.heading("tarifa", text="Tarifa / Hora")
        self.tabla_servicios.heading("disponible", text="Disponibilidad")
        self.tabla_servicios.heading("descripcion", text="Descripción Polimórfica (describir_servicio)")

        self.tabla_servicios.column("id", width=85, anchor="center")
        self.tabla_servicios.column("tipo", width=130, anchor="center")
        self.tabla_servicios.column("nombre", width=180)
        self.tabla_servicios.column("tarifa", width=110, anchor="e")
        self.tabla_servicios.column("disponible", width=110, anchor="center")
        self.tabla_servicios.column("descripcion", width=360)

        barra_vertical = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla_servicios.yview)
        self.tabla_servicios.configure(yscrollcommand=barra_vertical.set)

        self.tabla_servicios.pack(side="left", fill="both", expand=True)
        barra_vertical.pack(side="right", fill="y")

    def _actualizar_etiquetas_servicio(self, evento=None):
        """Ajusta dinámicamente las etiquetas según la subclase de Servicio seleccionada."""
        tipo = self.var_servicio_tipo.get()
        if tipo == "Sala":
            self.etiqueta_param1.configure(text="Capacidad (Personas):")
            self.etiqueta_param2.configure(text="¿Incluye Equipamiento?:")
            self.combo_param2.configure(values=("Si", "No"))
            self.var_servicio_param1.set("15")
            self.var_servicio_param2.set("Si")
        elif tipo == "Equipo":
            self.etiqueta_param1.configure(text="Cantidad de Equipos:")
            self.etiqueta_param2.configure(text="Gama del Equipo:")
            self.combo_param2.configure(values=("Estandar", "Alta"))
            self.var_servicio_param1.set("2")
            self.var_servicio_param2.set("Alta")
        else:
            self.etiqueta_param1.configure(text="Especialidad:")
            self.etiqueta_param2.configure(text="Nivel del Experto:")
            self.combo_param2.configure(values=("Junior", "Senior", "Master"))
            self.var_servicio_param1.set("Arquitectura de Software")
            self.var_servicio_param2.set("Senior")

    def crear_servicio_ui(self):
        """Valida localmente la entrada y solicita al gestor la creación polimórfica del servicio."""
        texto_tarifa = self.var_servicio_tarifa.get().strip()
        try:
            if texto_tarifa == "":
                raise ValueError("Debe ingresar un valor para la tarifa por hora.")
            valor_tarifa = float(texto_tarifa)
        except ValueError:
            # Si el usuario ingresó texto no numérico, lo enviamos igualmente al gestor
            # para que también quede auditado en eventos_y_errores.log sin congelar Tkinter
            valor_tarifa = texto_tarifa

        resultado = self.gestor.crear_servicio(
            tipo_servicio=self.var_servicio_tipo.get(),
            id_servicio=self.var_servicio_id.get(),
            nombre=self.var_servicio_nombre.get(),
            tarifa_hora=valor_tarifa,
            parametro_principal=self.var_servicio_param1.get(),
            parametro_secundario=self.var_servicio_param2.get(),
        )

        self.actualizar_todo()
        if resultado["exito"]:
            self.limpiar_formulario_servicio()
            messagebox.showinfo("Servicio Creado", resultado["mensaje"])
        else:
            messagebox.showwarning("Operación Controlada", resultado["mensaje"])

    def limpiar_formulario_servicio(self):
        siguiente_num = len(self.gestor.obtener_servicios()) + 1
        self.var_servicio_id.set(f"SRV-{siguiente_num:02d}")
        self.var_servicio_nombre.set("")
        self.var_servicio_tarifa.set("50000")
        self._actualizar_etiquetas_servicio()

    # =====================================================================
    # PESTAÑA 3: GESTIÓN DE RESERVAS (RF-04 y RF-05)
    # =====================================================================

    def _construir_pestana_reservas(self):
        marco_formulario = ttk.LabelFrame(
            self.pestana_reservas,
            text="Crear, Procesar, Confirmar o Cancelar Reservas (Cálculo Sobrecargado)",
            padding=10,
        )
        marco_formulario.pack(fill="x", pady=(0, 8))

        self.var_reserva_id = tk.StringVar(value="RES-01")
        self.var_reserva_cliente = tk.StringVar()
        self.var_reserva_servicio = tk.StringVar()
        self.var_reserva_duracion = tk.StringVar(value="2")
        self.var_reserva_impuesto = tk.StringVar(value="19")
        self.var_reserva_descuento = tk.StringVar(value="0")
        self.var_reserva_recargo = tk.StringVar(value="0")

        ttk.Label(marco_formulario, text="ID Reserva:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.var_reserva_id, width=14).grid(row=0, column=1, sticky="w", padx=5, pady=4)

        ttk.Label(marco_formulario, text="Cliente (ID):").grid(row=0, column=2, sticky="w", padx=5, pady=4)
        self.combo_reserva_cliente = ttk.Combobox(marco_formulario, textvariable=self.var_reserva_cliente, width=26)
        self.combo_reserva_cliente.grid(row=0, column=3, sticky="w", padx=5, pady=4)

        ttk.Label(marco_formulario, text="Servicio (ID):").grid(row=0, column=4, sticky="w", padx=5, pady=4)
        self.combo_reserva_servicio = ttk.Combobox(marco_formulario, textvariable=self.var_reserva_servicio, width=28)
        self.combo_reserva_servicio.grid(row=0, column=5, sticky="w", padx=5, pady=4)

        ttk.Label(marco_formulario, text="Duración (Horas):").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.var_reserva_duracion, width=14).grid(row=1, column=1, sticky="w", padx=5, pady=4)

        ttk.Label(marco_formulario, text="Impuesto (% opc.):").grid(row=1, column=2, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.var_reserva_impuesto, width=14).grid(row=1, column=3, sticky="w", padx=5, pady=4)

        ttk.Label(marco_formulario, text="Descuento (% opc.):").grid(row=1, column=4, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.var_reserva_descuento, width=14).grid(row=1, column=5, sticky="w", padx=5, pady=4)

        ttk.Label(marco_formulario, text="Recargo (% opc.):").grid(row=2, column=0, sticky="w", padx=5, pady=4)
        ttk.Entry(marco_formulario, textvariable=self.var_reserva_recargo, width=14).grid(row=2, column=1, sticky="w", padx=5, pady=4)

        marco_botones = ttk.Frame(marco_formulario)
        marco_botones.grid(row=2, column=2, columnspan=4, sticky="e", padx=5, pady=6)

        ttk.Button(marco_botones, text="1. Crear y Procesar Reserva", command=self.crear_reserva_ui).pack(side="left", padx=3)
        ttk.Button(marco_botones, text="2. Confirmar Reserva", command=self.confirmar_reserva_ui).pack(side="left", padx=3)
        ttk.Button(marco_botones, text="3. Cancelar Reserva", command=self.cancelar_reserva_ui).pack(side="left", padx=3)
        ttk.Button(marco_botones, text="Limpiar", command=self.limpiar_formulario_reserva).pack(side="left", padx=3)

        # Tabla de reservas
        marco_tabla = ttk.LabelFrame(
            self.pestana_reservas,
            text="Reservas en Memoria (Seleccione una fila para Confirmar o Cancelar)",
            padding=8,
        )
        marco_tabla.pack(fill="both", expand=True)

        columnas = ("id", "cliente", "servicio", "duracion", "costo", "estado")
        self.tabla_reservas = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=10)

        self.tabla_reservas.heading("id", text="ID Reserva")
        self.tabla_reservas.heading("cliente", text="Cliente")
        self.tabla_reservas.heading("servicio", text="Servicio Reservado")
        self.tabla_reservas.heading("duracion", text="Duración (Horas)")
        self.tabla_reservas.heading("costo", text="Costo Total Calculado")
        self.tabla_reservas.heading("estado", text="Estado Actual")

        self.tabla_reservas.column("id", width=100, anchor="center")
        self.tabla_reservas.column("cliente", width=210)
        self.tabla_reservas.column("servicio", width=240)
        self.tabla_reservas.column("duracion", width=120, anchor="center")
        self.tabla_reservas.column("costo", width=150, anchor="e")
        self.tabla_reservas.column("estado", width=120, anchor="center")

        self.tabla_reservas.bind("<<TreeviewSelect>>", self._al_seleccionar_reserva)

        barra_vertical = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla_reservas.yview)
        self.tabla_reservas.configure(yscrollcommand=barra_vertical.set)

        self.tabla_reservas.pack(side="left", fill="both", expand=True)
        barra_vertical.pack(side="right", fill="y")

    def _extraer_id_selector(self, texto_selector):
        """Extrae el ID limpio cuando el usuario elige 'ID | Nombre' del desplegable."""
        if texto_selector is None:
            return ""
        texto = str(texto_selector).strip()
        if "|" in texto:
            return texto.split("|")[0].strip()
        return texto

    def _al_seleccionar_reserva(self, evento=None):
        """Copia el ID de la reserva seleccionada en la tabla hacia el campo ID Reserva."""
        seleccion = self.tabla_reservas.selection()
        if seleccion:
            valores = self.tabla_reservas.item(seleccion[0], "values")
            if valores:
                self.var_reserva_id.set(valores[0])

    def crear_reserva_ui(self):
        """Valida las entradas numéricas locales y solicita al gestor crear y procesar la reserva."""
        id_reserva = self.var_reserva_id.get()
        id_cliente = self._extraer_id_selector(self.var_reserva_cliente.get())
        id_servicio = self._extraer_id_selector(self.var_reserva_servicio.get())

        texto_duracion = self.var_reserva_duracion.get().strip()
        texto_impuesto = self.var_reserva_impuesto.get().strip() or "0"
        texto_descuento = self.var_reserva_descuento.get().strip() or "0"
        texto_recargo = self.var_reserva_recargo.get().strip() or "0"

        try:
            duracion = float(texto_duracion) if texto_duracion != "" else texto_duracion
        except ValueError:
            duracion = texto_duracion

        try:
            impuesto = float(texto_impuesto)
        except ValueError:
            impuesto = texto_impuesto

        try:
            descuento = float(texto_descuento)
        except ValueError:
            descuento = texto_descuento

        try:
            recargo = float(texto_recargo)
        except ValueError:
            recargo = texto_recargo

        resultado = self.gestor.crear_reserva(
            id_reserva=id_reserva,
            id_cliente=id_cliente,
            id_servicio=id_servicio,
            duracion=duracion,
            impuesto=impuesto,
            descuento=descuento,
            recargo=recargo,
        )

        self.actualizar_todo()
        if resultado["exito"]:
            messagebox.showinfo("Reserva Procesada", resultado["mensaje"])
        else:
            messagebox.showwarning("Operación Controlada", resultado["mensaje"])

    def confirmar_reserva_ui(self):
        """Confirma la reserva cuyo ID esté seleccionado o escrito en el formulario."""
        id_reserva = self.var_reserva_id.get()
        resultado = self.gestor.confirmar_reserva(id_reserva)
        self.actualizar_todo()
        if resultado["exito"]:
            messagebox.showinfo("Reserva Confirmada", resultado["mensaje"])
        else:
            messagebox.showwarning("Operación Controlada", resultado["mensaje"])

    def cancelar_reserva_ui(self):
        """Cancela la reserva cuyo ID esté seleccionado o escrito en el formulario."""
        id_reserva = self.var_reserva_id.get()
        resultado = self.gestor.cancelar_reserva(id_reserva)
        self.actualizar_todo()
        if resultado["exito"]:
            messagebox.showinfo("Reserva Cancelada", resultado["mensaje"])
        else:
            messagebox.showwarning("Operación Controlada", resultado["mensaje"])

    def limpiar_formulario_reserva(self):
        siguiente_num = len(self.gestor.obtener_reservas()) + 1
        self.var_reserva_id.set(f"RES-{siguiente_num:02d}")
        self.var_reserva_duracion.set("2")
        self.var_reserva_impuesto.set("19")
        self.var_reserva_descuento.set("0")
        self.var_reserva_recargo.set("0")

    # =====================================================================
    # PESTAÑA 4: PANEL DE SIMULACIÓN AUTOMÁTICA (RNF-04)
    # =====================================================================

    def _construir_pestana_simulacion(self):
        marco_control = ttk.LabelFrame(
            self.pestana_simulacion,
            text="Simulador de Resiliencia y Manejo Avanzado de Excepciones (RNF-04)",
            padding=10,
        )
        marco_control.pack(fill="x", pady=(0, 8))

        descripcion = (
            "Este panel ejecuta automáticamente una batería de 12 operaciones completas en memoria:\n"
            "• Casos válidos: registro de clientes, creación de las 3 subclases de servicio, procesamiento sobrecargado y confirmación de reserva.\n"
            "• Casos inválidos y fallidos: correo inválido, parámetro faltante, tarifa negativa, servicio no disponible y descuento inconsistente (>100%).\n"
            "El sistema intercepta cada error con bloques try/except/else/finally, encadena la causa raíz y continúa operando sin interrupciones."
        )
        ttk.Label(marco_control, text=descripcion, justify="left").pack(anchor="w", pady=(0, 8))

        marco_acciones = ttk.Frame(marco_control)
        marco_acciones.pack(fill="x")

        ttk.Button(
            marco_acciones,
            text="Ejecutar Simulación Completa (12 Operaciones)",
            command=self.ejecutar_simulacion_ui,
        ).pack(side="left", padx=(0, 15))

        self.var_resumen_simulacion = tk.StringVar(
            value="Estado: Pendiente de ejecución | Operaciones totales en sesión: 0"
        )
        ttk.Label(
            marco_acciones,
            textvariable=self.var_resumen_simulacion,
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left")

        # Tabla de resultados de simulación
        marco_tabla = ttk.LabelFrame(
            self.pestana_simulacion,
            text="Resultado Detallado de las Operaciones Simuladas",
            padding=8,
        )
        marco_tabla.pack(fill="both", expand=True)

        columnas = ("operacion", "estado", "mensaje")
        self.tabla_simulacion = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=10)

        self.tabla_simulacion.heading("operacion", text="Caso de Prueba Ejecutado")
        self.tabla_simulacion.heading("estado", text="Resultado")
        self.tabla_simulacion.heading("mensaje", text="Respuesta Controlada del Sistema / Excepción Encadenada")

        self.tabla_simulacion.column("operacion", width=300)
        self.tabla_simulacion.column("estado", width=140, anchor="center")
        self.tabla_simulacion.column("mensaje", width=520)

        barra_vertical = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla_simulacion.yview)
        self.tabla_simulacion.configure(yscrollcommand=barra_vertical.set)

        self.tabla_simulacion.pack(side="left", fill="both", expand=True)
        barra_vertical.pack(side="right", fill="y")

    def ejecutar_simulacion_ui(self):
        """Ejecuta las 12 operaciones del simulador y refresca todas las tablas y el log."""
        reporte = self.gestor.ejecutar_simulacion()

        for item in self.tabla_simulacion.get_children():
            self.tabla_simulacion.delete(item)

        for nombre_caso, resultado in reporte["detalle_operaciones"]:
            texto_estado = "EXITOSA" if resultado["exito"] else "ERROR CONTROLADO"
            self.tabla_simulacion.insert(
                "",
                "end",
                values=(nombre_caso, texto_estado, resultado["mensaje"]),
            )

        self.var_resumen_simulacion.set(
            f"Simulación completada: {reporte['total_ejecutadas']} operaciones | "
            f"Exitosas: {reporte['exitosas']} | "
            f"Errores interceptados: {reporte['errores_controlados']} | "
            f"Total sesión: {self.gestor.total_operaciones}"
        )

        self.actualizar_todo()
        messagebox.showinfo(
            "Simulación Finalizada",
            f"Se ejecutaron {reporte['total_ejecutadas']} operaciones sin detener el sistema.\n\n"
            f"• Operaciones exitosas: {reporte['exitosas']}\n"
            f"• Errores controlados y auditados: {reporte['errores_controlados']}\n\n"
            "Revise las pestañas de Clientes, Servicios, Reservas y el visor inferior de logs.",
        )

    # =====================================================================
    # VISOR INFERIOR DE AUDITORÍA (eventos_y_errores.log) (RNF-03)
    # =====================================================================

    def _construir_visor_logs(self):
        marco_logs = ttk.LabelFrame(
            self.ventana,
            text="Visor de Auditoría en Tiempo Real — Archivo: eventos_y_errores.log",
            padding=8,
        )
        marco_logs.pack(fill="both", expand=False, padx=8, pady=(0, 8))

        marco_texto = ttk.Frame(marco_logs)
        marco_texto.pack(fill="both", expand=True)

        self.caja_texto_log = tk.Text(
            marco_texto,
            height=8,
            bg="#0f172a",
            fg="#e2e8f0",
            font=("Consolas", 9),
            wrap="none",
            state="disabled",
        )
        barra_vertical = ttk.Scrollbar(marco_texto, orient="vertical", command=self.caja_texto_log.yview)
        barra_horizontal = ttk.Scrollbar(marco_logs, orient="horizontal", command=self.caja_texto_log.xview)

        self.caja_texto_log.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set,
        )

        self.caja_texto_log.pack(side="left", fill="both", expand=True)
        barra_vertical.pack(side="right", fill="y")
        barra_horizontal.pack(fill="x")

    # =====================================================================
    # SINCRONIZACIÓN DE TABLAS Y VISOR DE LOGS EN TIEMPO REAL
    # =====================================================================

    def actualizar_todo(self):
        """Sincroniza todas las tablas, selectores desplegables y el visor del archivo .log."""
        self.actualizar_tabla_clientes()
        self.actualizar_tabla_servicios()
        self.actualizar_tabla_reservas()
        self.actualizar_selectores_reserva()
        self.actualizar_visor_log()

    def actualizar_tabla_clientes(self):
        for fila in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(fila)

        for cliente in self.gestor.obtener_clientes():
            self.tabla_clientes.insert(
                "",
                "end",
                values=(
                    cliente.id,
                    cliente.nombre,
                    cliente.documento,
                    cliente.correo,
                    cliente.telefono,
                    cliente.fecha_creacion,
                ),
            )

    def actualizar_tabla_servicios(self):
        for fila in self.tabla_servicios.get_children():
            self.tabla_servicios.delete(fila)

        for servicio in self.gestor.obtener_servicios():
            nombre_clase = type(servicio).__name__
            estado_texto = "Disponible" if servicio.disponible else "Ocupado / No Disp."
            self.tabla_servicios.insert(
                "",
                "end",
                values=(
                    servicio.id,
                    nombre_clase,
                    servicio.nombre,
                    f"${servicio.tarifa_hora:,.2f}",
                    estado_texto,
                    servicio.describir_servicio(),
                ),
            )

    def actualizar_tabla_reservas(self):
        for fila in self.tabla_reservas.get_children():
            self.tabla_reservas.delete(fila)

        for reserva in self.gestor.obtener_reservas():
            self.tabla_reservas.insert(
                "",
                "end",
                values=(
                    reserva.id,
                    f"{reserva.cliente.id} - {reserva.cliente.nombre}",
                    f"{reserva.servicio.id} - {reserva.servicio.nombre}",
                    f"{reserva.duracion} h",
                    f"${reserva.costo_total:,.2f}",
                    reserva.estado,
                ),
            )

    def actualizar_selectores_reserva(self):
        opciones_clientes = [
            f"{cliente.id} | {cliente.nombre}"
            for cliente in self.gestor.obtener_clientes()
        ]
        self.combo_reserva_cliente.configure(values=opciones_clientes)
        if opciones_clientes and not self.var_reserva_cliente.get():
            self.var_reserva_cliente.set(opciones_clientes[0])

        opciones_servicios = [
            f"{servicio.id} | {servicio.nombre} ({'Disp.' if servicio.disponible else 'Ocupado'})"
            for servicio in self.gestor.obtener_servicios()
        ]
        self.combo_reserva_servicio.configure(values=opciones_servicios)
        if opciones_servicios and not self.var_reserva_servicio.get():
            self.var_reserva_servicio.set(opciones_servicios[0])

    def actualizar_visor_log(self):
        contenido_log = self.gestor.leer_archivo_log()
        self.caja_texto_log.configure(state="normal")
        self.caja_texto_log.delete("1.0", "end")
        self.caja_texto_log.insert("end", contenido_log)
        self.caja_texto_log.see("end")
        self.caja_texto_log.configure(state="disabled")


def iniciar_aplicacion():
    """Punto de entrada principal de Software FJ."""
    ventana_principal = tk.Tk()
    AplicacionSoftwareFJ(ventana_principal)
    ventana_principal.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()
