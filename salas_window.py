import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import datetime
import os

class SalasWindow:
    """
    SalasWindow: Interfaz gráfica para gestionar salas de juego utilizando Tkinter.
    
    Esta clase implementa una ventana que permite a los usuarios crear, unirse, editar y
    eliminar salas de juego para facilitar la formación de equipos.
    
    Atributos:
        master (tk.Tk): La ventana principal de Tkinter.
        usuario (str): Nombre del usuario que ha iniciado sesión.
        data_file (str): Ruta del archivo JSON para almacenar las salas.
        is_admin (bool): Indica si el usuario tiene privilegios de administrador.
    """
    def __init__(self, master, usuario, is_admin=False):
        self.master = master
        self.master.title("Teamder - Salas de Juego")
        self.master.geometry("1000x700")
        self.usuario = usuario
        self.is_admin = is_admin
        
        # Archivo para guardar las salas
        self.data_file = "salas_data.json"
        
        # Archivo para cargar juegos disponibles
        self.juegos_file = "juegos_data.json"
        
        # Cargar juegos
        self.cargar_juegos()
        
        # Cargar salas o crear datos iniciales
        self.cargar_salas()
        
        # Crear la interfaz
        self.crear_widgets()
        
    def cargar_juegos(self):
        """
        Carga la lista de juegos disponibles desde el archivo JSON.
        """
        try:
            if os.path.exists(self.juegos_file):
                with open(self.juegos_file, 'r', encoding='utf-8') as f:
                    self.juegos = json.load(f)
            else:
                self.juegos = ["General"]
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los juegos: {str(e)}")
            self.juegos = ["General"]
    
    def cargar_salas(self):
        """
        Carga las salas desde el archivo JSON.
        
        Si el archivo no existe, crea salas de ejemplo.
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.salas = json.load(f)
            else:
                # Crear algunas salas de ejemplo
                self.salas = [
                    {
                        "id": 1,
                        "nombre": "Equipo Rankeds",
                        "juego": "League of Legends",
                        "creador": "fatekiz",
                        "descripcion": "Buscamos jugadores para rankeds en League of Legends",
                        "fecha_creacion": "2025-04-10",
                        "miembros": ["fatekiz", "vice"],
                        "capacidad": 5,
                        "estado": "abierta",
                        "requisitos": "Platino+"
                    },
                    {
                        "id": 2,
                        "nombre": "Torneo Valorant",
                        "juego": "Valorant",
                        "creador": "admin777",
                        "descripcion": "Sala para organizar equipo para el torneo del fin de semana",
                        "fecha_creacion": "2025-04-11",
                        "miembros": ["admin777"],
                        "capacidad": 5,
                        "estado": "abierta",
                        "requisitos": "Cualquier nivel"
                    }
                ]
                self.guardar_salas()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar las salas: {str(e)}")
            self.salas = []
    
    def guardar_salas(self):
        """
        Guarda las salas en el archivo JSON.
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.salas, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar las salas: {str(e)}")
    
    def crear_widgets(self):
        """
        Configura la interfaz gráfica de la ventana de salas.
        """
        # Panel principal con división horizontal
        panel_principal = ttk.PanedWindow(self.master, orient=tk.HORIZONTAL)
        panel_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Lista de salas
        frame_salas = ttk.LabelFrame(panel_principal, text="Salas disponibles")
        panel_principal.add(frame_salas, weight=1)
        
        # Frame para filtros y botones
        frame_filtros = ttk.Frame(frame_salas)
        frame_filtros.pack(pady=5, padx=10, fill=tk.X)
        
        # Label para el selector de juegos
        ttk.Label(frame_filtros, text="Filtrar por juego:").pack(side=tk.LEFT, padx=5)
        
        # Combo para seleccionar juego
        self.combo_juegos = ttk.Combobox(frame_filtros, state="readonly")
        self.combo_juegos["values"] = ["Todos"] + sorted(self.juegos)
        self.combo_juegos.current(0)  # Seleccionar "Todos" por defecto
        self.combo_juegos.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.combo_juegos.bind("<<ComboboxSelected>>", self.filtrar_por_juego)
        
        # Frame para botones de salas
        frame_botones = ttk.Frame(frame_salas)
        frame_botones.pack(pady=5, padx=10, fill=tk.X)
        
        # Botón para crear nueva sala
        btn_nueva_sala = ttk.Button(frame_botones, text="Nueva sala", command=self.crear_nueva_sala)
        btn_nueva_sala.pack(side=tk.LEFT, padx=5)
        
        # Botón para actualizar la lista
        btn_actualizar = ttk.Button(frame_botones, text="Actualizar", command=self.actualizar_lista)
        btn_actualizar.pack(side=tk.LEFT, padx=5)
        
        # Lista de salas
        self.frame_lista = ttk.Frame(frame_salas)
        self.frame_lista.pack(fill=tk.BOTH, expand=True, pady=5, padx=10)
        
        # Cabeceras de lista con scrollbar
        columnas = ("nombre", "juego", "creador", "miembros", "estado")
        self.lista_salas = ttk.Treeview(self.frame_lista, columns=columnas, show="headings", selectmode="browse")
        
        # Configurar columnas
        self.lista_salas.heading("nombre", text="Nombre")
        self.lista_salas.heading("juego", text="Juego")
        self.lista_salas.heading("creador", text="Creador")
        self.lista_salas.heading("miembros", text="Ocupación")
        self.lista_salas.heading("estado", text="Estado")
        
        # Definir anchos de columna
        self.lista_salas.column("nombre", width=150)
        self.lista_salas.column("juego", width=120)
        self.lista_salas.column("creador", width=100)
        self.lista_salas.column("miembros", width=80)
        self.lista_salas.column("estado", width=80)
        
        # Añadir scrollbar
        scrollbar = ttk.Scrollbar(self.frame_lista, orient="vertical", command=self.lista_salas.yview)
        self.lista_salas.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar lista y scrollbar
        self.lista_salas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Evento al seleccionar una sala
        self.lista_salas.bind("<<TreeviewSelect>>", self.mostrar_sala)
        
        # Panel derecho - Detalles de la sala
        self.frame_detalles = ttk.LabelFrame(panel_principal, text="Detalles de la sala")
        panel_principal.add(self.frame_detalles, weight=2)
        
        # Frame para mostrar los detalles
        self.crear_panel_detalles()
        
        # Cargar salas en la lista
        self.actualizar_lista()
    
    def crear_panel_detalles(self):
        """
        Crea el panel de detalles de la sala seleccionada.
        """
        # Frame para información general
        frame_info = ttk.Frame(self.frame_detalles)
        frame_info.pack(fill=tk.X, expand=True, padx=10, pady=10)
        
        # Etiquetas para mostrar información
        self.label_nombre = ttk.Label(frame_info, text="Selecciona una sala", font=("Arial", 14, "bold"))
        self.label_nombre.pack(anchor=tk.W)
        
        self.label_juego = ttk.Label(frame_info, text="")
        self.label_juego.pack(anchor=tk.W)
        
        self.label_creador = ttk.Label(frame_info, text="")
        self.label_creador.pack(anchor=tk.W)
        
        self.label_fecha = ttk.Label(frame_info, text="")
        self.label_fecha.pack(anchor=tk.W)
        
        self.label_estado = ttk.Label(frame_info, text="")
        self.label_estado.pack(anchor=tk.W)
        
        self.label_requisitos = ttk.Label(frame_info, text="")
        self.label_requisitos.pack(anchor=tk.W)
        
        self.label_miembros = ttk.Label(frame_info, text="")
        self.label_miembros.pack(anchor=tk.W, pady=(10, 0))
        
        # Frame para la descripción
        frame_descripcion = ttk.LabelFrame(self.frame_detalles, text="Descripción")
        frame_descripcion.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.texto_descripcion = scrolledtext.ScrolledText(frame_descripcion, wrap=tk.WORD, height=6)
        self.texto_descripcion.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.texto_descripcion.config(state=tk.DISABLED)
        
        # Frame para la lista de miembros
        frame_lista_miembros = ttk.LabelFrame(self.frame_detalles, text="Miembros")
        frame_lista_miembros.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar para lista de miembros
        frame_scroll_miembros = ttk.Frame(frame_lista_miembros)
        frame_scroll_miembros.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Lista de miembros
        self.lista_miembros = tk.Listbox(frame_scroll_miembros, font=("Arial", 10))
        scrollbar_miembros = ttk.Scrollbar(frame_scroll_miembros, orient="vertical", command=self.lista_miembros.yview)
        self.lista_miembros.configure(yscrollcommand=scrollbar_miembros.set)
        
        self.lista_miembros.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_miembros.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para botones de acción
        self.frame_acciones = ttk.Frame(self.frame_detalles)
        self.frame_acciones.pack(fill=tk.X, padx=10, pady=10)
        
        # Botones (inicialmente deshabilitados)
        self.btn_unirse = ttk.Button(self.frame_acciones, text="Unirse a la sala", 
                                     command=self.unirse_sala, state=tk.DISABLED)
        self.btn_unirse.pack(side=tk.LEFT, padx=5)
        
        self.btn_salir = ttk.Button(self.frame_acciones, text="Salir de la sala", 
                                    command=self.salir_sala, state=tk.DISABLED)
        self.btn_salir.pack(side=tk.LEFT, padx=5)
        
        self.btn_editar = ttk.Button(self.frame_acciones, text="Editar sala", 
                                     command=self.editar_sala, state=tk.DISABLED)
        self.btn_editar.pack(side=tk.LEFT, padx=5)
        
        self.btn_eliminar = ttk.Button(self.frame_acciones, text="Eliminar sala", 
                                       command=self.eliminar_sala, state=tk.DISABLED)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        self.btn_chat = ttk.Button(self.frame_acciones, text="Chat de sala", 
                                   command=self.abrir_chat, state=tk.DISABLED)
        self.btn_chat.pack(side=tk.LEFT, padx=5)
    
    def filtrar_por_juego(self, event=None):
        """
        Filtra la lista de salas por el juego seleccionado.
        """
        seleccion = self.combo_juegos.get()
        
        # Limpiar lista actual
        for item in self.lista_salas.get_children():
            self.lista_salas.delete(item)
            
        # Filtrar salas por juego seleccionado
        for sala in self.salas:
            if seleccion == "Todos" or sala.get("juego") == seleccion:
                # Formato para mostrar cantidad de miembros: X/Y
                miembros_str = f"{len(sala['miembros'])}/{sala['capacidad']}"
                self.lista_salas.insert("", tk.END, iid=str(sala["id"]), 
                                        values=(sala.get("nombre", "Sin nombre"), 
                                               sala.get("juego", "General"),
                                               sala["creador"],
                                               miembros_str,
                                               sala["estado"]))
    
    def actualizar_lista(self):
        """
        Actualiza la lista de salas.
        """
        # Cargar salas desde el archivo
        self.cargar_salas()
        
        # Actualizar la lista según el filtro actual
        self.filtrar_por_juego()
        
        # Si hay una sala seleccionada, mantener la selección
        if hasattr(self, 'sala_actual_id') and self.sala_actual_id:
            try:
                self.lista_salas.selection_set(str(self.sala_actual_id))
                self.mostrar_sala(None)
            except:
                pass
    
    def mostrar_sala(self, event):
        """
        Muestra los detalles de la sala seleccionada.
        """
        seleccion = self.lista_salas.selection()
        if not seleccion:
            return
            
        sala_id = int(seleccion[0])
        self.sala_actual_id = sala_id
        
        # Buscar la sala seleccionada
        sala = None
        for s in self.salas:
            if s["id"] == sala_id:
                sala = s
                break
                
        if not sala:
            return
            
        # Mostrar información de la sala
        self.label_nombre.config(text=sala.get("nombre", "Sin nombre"))
        self.label_juego.config(text=f"Juego: {sala.get('juego', 'General')}")
        self.label_creador.config(text=f"Creador: {sala['creador']}")
        self.label_fecha.config(text=f"Creada el: {sala['fecha_creacion']}")
        self.label_estado.config(text=f"Estado: {sala['estado'].capitalize()}")
        self.label_requisitos.config(text=f"Requisitos: {sala.get('requisitos', 'No especificados')}")
        
        miembros_str = f"Ocupación: {len(sala['miembros'])}/{sala['capacidad']}"
        self.label_miembros.config(text=miembros_str)
        
        # Mostrar descripción
        self.texto_descripcion.config(state=tk.NORMAL)
        self.texto_descripcion.delete(1.0, tk.END)
        self.texto_descripcion.insert(tk.END, sala.get("descripcion", "Sin descripción"))
        self.texto_descripcion.config(state=tk.DISABLED)
        
        # Actualizar lista de miembros
        self.lista_miembros.delete(0, tk.END)
        for i, miembro in enumerate(sala['miembros']):
            prefijo = " (Creador)" if miembro == sala['creador'] else ""
            self.lista_miembros.insert(tk.END, f"{i+1}. {miembro}{prefijo}")
        
        # Configurar botones según el estado del usuario
        es_miembro = self.usuario in sala['miembros']
        es_creador = self.usuario == sala['creador']
        sala_llena = len(sala['miembros']) >= sala['capacidad']
        sala_cerrada = sala['estado'].lower() == "cerrada"
        
        # Botón unirse: visible si no es miembro, la sala no está llena y está abierta
        if not es_miembro and not sala_llena and not sala_cerrada:
            self.btn_unirse.config(state=tk.NORMAL)
        else:
            self.btn_unirse.config(state=tk.DISABLED)
        
        # Botón salir: visible si es miembro pero no es el creador
        if es_miembro and not es_creador:
            self.btn_salir.config(state=tk.NORMAL)
        else:
            self.btn_salir.config(state=tk.DISABLED)
        
        # Botón editar: visible si es el creador o es admin
        if es_creador or self.is_admin:
            self.btn_editar.config(state=tk.NORMAL)
        else:
            self.btn_editar.config(state=tk.DISABLED)
        
        # Botón eliminar: visible si es el creador o es admin
        if es_creador or self.is_admin:
            self.btn_eliminar.config(state=tk.NORMAL)
        else:
            self.btn_eliminar.config(state=tk.DISABLED)
        
        # Botón chat: visible si es miembro
        if es_miembro:
            self.btn_chat.config(state=tk.NORMAL)
        else:
            self.btn_chat.config(state=tk.DISABLED)
    
    def crear_nueva_sala(self):
        """
        Abre una ventana para crear una nueva sala.
        """
        ventana_nueva = tk.Toplevel(self.master)
        ventana_nueva.title("Crear nueva sala")
        ventana_nueva.geometry("800x600")
        ventana_nueva.grab_set()  # Modal
        
        # Frame principal con scrollbar
        canvas = tk.Canvas(ventana_nueva)
        scrollbar = ttk.Scrollbar(ventana_nueva, orient="vertical", command=canvas.yview)
        frame_scroll = ttk.Frame(canvas)
        
        frame_scroll.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Añadir padding
        frame_contenido = ttk.Frame(frame_scroll, padding=15)
        frame_contenido.pack(fill=tk.BOTH, expand=True)
        
        # Título del formulario
        ttk.Label(frame_contenido, text="Crear nueva sala de juego", 
                 font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=(0, 15))
        
        # Nombre de la sala
        ttk.Label(frame_contenido, text="Nombre de la sala:").pack(anchor=tk.W, pady=(10, 5))
        entry_nombre = ttk.Entry(frame_contenido, width=50)
        entry_nombre.pack(fill=tk.X, pady=(0, 10))
        
        # Selector de juego
        ttk.Label(frame_contenido, text="Juego:").pack(anchor=tk.W, pady=(10, 5))
        combo_juego = ttk.Combobox(frame_contenido, state="readonly", width=50)
        combo_juego["values"] = ["General"] + sorted(self.juegos)
        combo_juego.current(0)  # Seleccionar "General" por defecto
        combo_juego.pack(fill=tk.X, pady=(0, 10))
        
        # Capacidad
        ttk.Label(frame_contenido, text="Capacidad máxima:").pack(anchor=tk.W, pady=(10, 5))
        frame_capacidad = ttk.Frame(frame_contenido)
        frame_capacidad.pack(fill=tk.X, pady=(0, 10))
        
        capacidad_var = tk.StringVar(value="5")
        
        for i in range(2, 11):
            rb = ttk.Radiobutton(frame_capacidad, text=str(i), variable=capacidad_var, value=str(i))
            rb.pack(side=tk.LEFT, padx=5)
        
        # Requisitos
        ttk.Label(frame_contenido, text="Requisitos para unirse:").pack(anchor=tk.W, pady=(10, 5))
        entry_requisitos = ttk.Entry(frame_contenido, width=50)
        entry_requisitos.pack(fill=tk.X, pady=(0, 10))
        entry_requisitos.insert(0, "Cualquier nivel")
        
        # Descripción
        ttk.Label(frame_contenido, text="Descripción de la sala:").pack(anchor=tk.W, pady=(10, 5))
        texto_descripcion = scrolledtext.ScrolledText(frame_contenido, wrap=tk.WORD, height=6)
        texto_descripcion.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Estado
        frame_estado = ttk.Frame(frame_contenido)
        frame_estado.pack(fill=tk.X, pady=(10, 10))
        
        ttk.Label(frame_estado, text="Estado:").pack(side=tk.LEFT)
        
        estado_var = tk.StringVar(value="abierta")
        
        ttk.Radiobutton(frame_estado, text="Abierta", 
                       variable=estado_var, value="abierta").pack(side=tk.LEFT, padx=(10, 5))
        ttk.Radiobutton(frame_estado, text="Cerrada", 
                       variable=estado_var, value="cerrada").pack(side=tk.LEFT, padx=5)
        
        # Botones
        frame_botones = ttk.Frame(frame_contenido)
        frame_botones.pack(fill=tk.X, pady=15)
        
        def guardar_sala():
            # Validación
            nombre = entry_nombre.get().strip()
            juego = combo_juego.get()
            capacidad = int(capacidad_var.get())
            requisitos = entry_requisitos.get().strip()
            descripcion = texto_descripcion.get(1.0, tk.END).strip()
            estado = estado_var.get()
            
            if not nombre:
                messagebox.showwarning("Campos incompletos", "El nombre de la sala es obligatorio")
                return
            
            if len(nombre) > 30:
                messagebox.showwarning("Nombre demasiado largo", 
                                      "El nombre de la sala debe tener máximo 30 caracteres")
                return
            
            # Crear nueva sala
            nuevo_id = 1
            if self.salas:
                nuevo_id = max(sala["id"] for sala in self.salas) + 1
                
            nueva_sala = {
                "id": nuevo_id,
                "nombre": nombre,
                "juego": juego,
                "creador": self.usuario,
                "descripcion": descripcion,
                "fecha_creacion": datetime.datetime.now().strftime("%Y-%m-%d"),
                "miembros": [self.usuario],
                "capacidad": capacidad,
                "estado": estado,
                "requisitos": requisitos if requisitos else "No especificados"
            }
            
            self.salas.append(nueva_sala)
            self.guardar_salas()
            
            # Actualizar la vista
            self.actualizar_lista()
            self.lista_salas.selection_set(str(nuevo_id))
            self.mostrar_sala(None)
            
            ventana_nueva.destroy()
            messagebox.showinfo("Éxito", "Sala creada correctamente")
        
        ttk.Button(frame_botones, text="Crear sala", command=guardar_sala).pack(side=tk.RIGHT, padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=ventana_nueva.destroy).pack(side=tk.RIGHT, padx=5)
        
    def editar_sala(self):
        """
        Edita la sala seleccionada si el usuario es el creador o administrador.
        """
        seleccion = self.lista_salas.selection()
        if not seleccion:
            return
            
        sala_id = int(seleccion[0])
        
        # Buscar la sala
        sala = None
        for s in self.salas:
            if s["id"] == sala_id:
                sala = s
                break
                
        if not sala:
            return
            
        # Verificar permisos
        if sala["creador"] != self.usuario and not self.is_admin:
            messagebox.showerror("Error", "No tienes permisos para editar esta sala")
            return
        
        # Crear ventana de edición
        ventana_editar = tk.Toplevel(self.master)
        ventana_editar.title(f"Editar sala: {sala['nombre']}")
        ventana_editar.geometry("1000x800")
        ventana_editar.grab_set()  # Modal
        
        # Frame principal con scrollbar
        canvas = tk.Canvas(ventana_editar)
        scrollbar = ttk.Scrollbar(ventana_editar, orient="vertical", command=canvas.yview)
        frame_scroll = ttk.Frame(canvas)
        
        frame_scroll.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Añadir padding
        frame_contenido = ttk.Frame(frame_scroll, padding=15)
        frame_contenido.pack(fill=tk.BOTH, expand=True)
        
        # Título del formulario
        ttk.Label(frame_contenido, text=f"Editar sala: {sala['nombre']}", 
                 font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=(0, 15))
        
        # Nombre de la sala
        ttk.Label(frame_contenido, text="Nombre de la sala:").pack(anchor=tk.W, pady=(10, 5))
        entry_nombre = ttk.Entry(frame_contenido, width=50)
        entry_nombre.pack(fill=tk.X, pady=(0, 10))
        entry_nombre.insert(0, sala.get("nombre", ""))
        
        # Selector de juego
        ttk.Label(frame_contenido, text="Juego:").pack(anchor=tk.W, pady=(10, 5))
        combo_juego = ttk.Combobox(frame_contenido, state="readonly", width=50)
        combo_juego["values"] = ["General"] + sorted(self.juegos)
        
        # Seleccionar el juego actual
        juego_actual = sala.get("juego", "General")
        if juego_actual in combo_juego["values"]:
            combo_juego.set(juego_actual)
        else:
            combo_juego.current(0)
            
        combo_juego.pack(fill=tk.X, pady=(0, 10))
        
        # Capacidad
        ttk.Label(frame_contenido, text="Capacidad máxima:").pack(anchor=tk.W, pady=(10, 5))
        frame_capacidad = ttk.Frame(frame_contenido)
        frame_capacidad.pack(fill=tk.X, pady=(0, 10))
        
        capacidad_var = tk.StringVar(value=str(sala.get("capacidad", 5)))
        
        for i in range(2, 11):
            rb = ttk.Radiobutton(frame_capacidad, text=str(i), variable=capacidad_var, value=str(i))
            rb.pack(side=tk.LEFT, padx=5)
        
        # Requisitos
        ttk.Label(frame_contenido, text="Requisitos para unirse:").pack(anchor=tk.W, pady=(10, 5))
        entry_requisitos = ttk.Entry(frame_contenido, width=50)
        entry_requisitos.pack(fill=tk.X, pady=(0, 10))
        entry_requisitos.insert(0, sala.get("requisitos", "Cualquier nivel"))
        
        # Descripción
        ttk.Label(frame_contenido, text="Descripción de la sala:").pack(anchor=tk.W, pady=(10, 5))
        texto_descripcion = scrolledtext.ScrolledText(frame_contenido, wrap=tk.WORD, height=6)
        texto_descripcion.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        texto_descripcion.insert(tk.END, sala.get("descripcion", ""))
        
        # Estado
        frame_estado = ttk.Frame(frame_contenido)
        frame_estado.pack(fill=tk.X, pady=(10, 10))
        
        ttk.Label(frame_estado, text="Estado:").pack(side=tk.LEFT)
        
        estado_var = tk.StringVar(value=sala.get("estado", "abierta"))
        
        ttk.Radiobutton(frame_estado, text="Abierta", 
                       variable=estado_var, value="abierta").pack(side=tk.LEFT, padx=(10, 5))
        ttk.Radiobutton(frame_estado, text="Cerrada", 
                       variable=estado_var, value="cerrada").pack(side=tk.LEFT, padx=5)
        
        # Gestión de miembros (solo para admin o creador)
        if sala["creador"] == self.usuario or self.is_admin:
            ttk.Label(frame_contenido, text="Gestionar miembros:", 
                     font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(15, 5))
            
            frame_miembros = ttk.Frame(frame_contenido)
            frame_miembros.pack(fill=tk.X, pady=(0, 10))
            
            # Lista de miembros con scrollbar
            lista_miembros = tk.Listbox(frame_miembros, height=5)
            scrollbar_miembros = ttk.Scrollbar(frame_miembros, orient="vertical", command=lista_miembros.yview)
            lista_miembros.configure(yscrollcommand=scrollbar_miembros.set)
            
            lista_miembros.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar_miembros.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Añadir miembros a la lista
            for miembro in sala["miembros"]:
                prefijo = " (Creador)" if miembro == sala["creador"] else ""
                lista_miembros.insert(tk.END, f"{miembro}{prefijo}")
            
            # Botón para expulsar miembro
            def expulsar_miembro():
                indices = lista_miembros.curselection()
                if not indices:
                    messagebox.showwarning("Selección requerida", "Selecciona un miembro para expulsar")
                    return
                    
                indice = indices[0]
                miembro = sala["miembros"][indice]
                
                # No se puede expulsar al creador
                if miembro == sala["creador"]:
                    messagebox.showwarning("Operación no permitida", "No puedes expulsar al creador de la sala")
                    return
                
                if messagebox.askyesno("Confirmar", f"¿Estás seguro de expulsar a '{miembro}' de la sala?"):
                    sala["miembros"].remove(miembro)
                    lista_miembros.delete(indice)
                    messagebox.showinfo("Éxito", f"Usuario '{miembro}' expulsado de la sala")
            
            ttk.Button(frame_contenido, text="Expulsar miembro seleccionado", 
                      command=expulsar_miembro).pack(pady=(0, 15))
        
        # Botones
        frame_botones = ttk.Frame(frame_contenido)
        frame_botones.pack(fill=tk.X, pady=15)
        
        def guardar_cambios():
            # Validación
            nombre = entry_nombre.get().strip()
            juego = combo_juego.get()
            capacidad = int(capacidad_var.get())
            requisitos = entry_requisitos.get().strip()
            descripcion = texto_descripcion.get(1.0, tk.END).strip()
            estado = estado_var.get()
            
            if not nombre:
                messagebox.showwarning("Campos incompletos", "El nombre de la sala es obligatorio")
                return
            
            if len(nombre) > 30:
                messagebox.showwarning("Nombre demasiado largo", 
                                      "El nombre de la sala debe tener máximo 30 caracteres")
                return
            
            # Verificar que la capacidad no sea menor que el número actual de miembros
            if capacidad < len(sala["miembros"]):
                messagebox.showwarning("Error de capacidad", 
                                     f"La capacidad no puede ser menor que el número actual de miembros ({len(sala['miembros'])})")
                return
            
            # Actualizar datos de la sala
            sala["nombre"] = nombre
            sala["juego"] = juego
            sala["capacidad"] = capacidad
            sala["requisitos"] = requisitos if requisitos else "No especificados"
            sala["descripcion"] = descripcion
            sala["estado"] = estado
            
            # Guardar cambios
            self.guardar_salas()
            
            # Actualizar la vista
            self.actualizar_lista()
            
            ventana_editar.destroy()
            messagebox.showinfo("Éxito", "Sala actualizada correctamente")
        
        ttk.Button(frame_botones, text="Guardar cambios", command=guardar_cambios).pack(side=tk.RIGHT, padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=ventana_editar.destroy).pack(side=tk.RIGHT, padx=5)
        
    def unirse_sala(self):
        """
        Une al usuario a la sala seleccionada.
        """
        seleccion = self.lista_salas.selection()
        if not seleccion:
            return
            
        sala_id = int(seleccion[0])
        
        # Buscar la sala
        sala = None
        for s in self.salas:
            if s["id"] == sala_id:
                sala = s
                break
                
        if not sala:
            return
            
        # Verificar estado de la sala
        if sala["estado"] == "cerrada":
            messagebox.showwarning("Sala cerrada", "Esta sala no acepta nuevos miembros actualmente")
            return
            
        # Verificar si hay espacio
        if len(sala["miembros"]) >= sala["capacidad"]:
            messagebox.showwarning("Sala llena", "Esta sala ya está llena")
            return
            
        # Verificar si ya es miembro
        if self.usuario in sala["miembros"]:
            messagebox.showinfo("Ya eres miembro", "Ya formas parte de esta sala")
            return
            
        # Unirse a la sala
        sala["miembros"].append(self.usuario)
        self.guardar_salas()
        
        # Actualizar vista
        self.mostrar_sala(None)
        messagebox.showinfo("Éxito", f"Te has unido a la sala '{sala['nombre']}'")
    
    def salir_sala(self):
        """
        Permite al usuario salir de una sala de la que es miembro.
        """
        seleccion = self.lista_salas.selection()
        if not seleccion:
            return
            
        sala_id = int(seleccion[0])
        
        # Buscar la sala
        sala = None
        for s in self.salas:
            if s["id"] == sala_id:
                sala = s
                break
                
        if not sala:
            return
            
        # Verificar si es miembro
        if self.usuario not in sala["miembros"]:
            messagebox.showinfo("No eres miembro", "No formas parte de esta sala")
            return
            
        # Verificar que no sea el creador (no puede salir, tendría que eliminar la sala)
        if self.usuario == sala["creador"]:
            messagebox.showwarning("Eres el creador", 
                                 "Como creador de la sala, no puedes salir. Debes eliminarla si ya no la necesitas.")
            return
            
        # Confirmar
        if not messagebox.askyesno("Confirmar", f"¿Estás seguro de salir de la sala '{sala['nombre']}'?"):
            return
            
        # Salir de la sala
        sala["miembros"].remove(self.usuario)
        self.guardar_salas()
        
        # Actualizar vista
        self.mostrar_sala(None)
        messagebox.showinfo("Éxito", f"Has salido de la sala '{sala['nombre']}'")
    
    def eliminar_sala(self):
        """
        Elimina la sala si el usuario es el creador o administrador.
        """
        seleccion = self.lista_salas.selection()
        if not seleccion:
            return
            
        sala_id = int(seleccion[0])
        
        # Buscar la sala
        sala = None
        for s in self.salas:
            if s["id"] == sala_id:
                sala = s
                break
                
        if not sala:
            return
            
        # Verificar permisos
        es_creador = self.usuario == sala["creador"]
        if not es_creador and not self.is_admin:
            messagebox.showerror("Error", "No tienes permisos para eliminar esta sala")
            return
            
        # Texto de confirmación
        if es_creador:
            mensaje = f"¿Estás seguro de eliminar tu sala '{sala['nombre']}'?"
        else:
            mensaje = f"¿Estás seguro de eliminar la sala '{sala['nombre']}' como administrador?"
            
        # Confirmar
        if not messagebox.askyesno("Confirmar eliminación", mensaje):
            return
            
        # Eliminar sala
        self.salas = [s for s in self.salas if s["id"] != sala_id]
        self.guardar_salas()
        
        # Actualizar interfaz
        self.actualizar_lista()
        
        # Limpiar panel de detalles
        self.label_nombre.config(text="Selecciona una sala")
        self.label_juego.config(text="")
        self.label_creador.config(text="")
        self.label_fecha.config(text="")
        self.label_estado.config(text="")
        self.label_requisitos.config(text="")
        self.label_miembros.config(text="")
        
        self.texto_descripcion.config(state=tk.NORMAL)
        self.texto_descripcion.delete(1.0, tk.END)
        self.texto_descripcion.config(state=tk.DISABLED)
        
        self.lista_miembros.delete(0, tk.END)
        
        # Deshabilitar botones
        self.btn_unirse.config(state=tk.DISABLED)
        self.btn_salir.config(state=tk.DISABLED)
        self.btn_editar.config(state=tk.DISABLED)
        self.btn_eliminar.config(state=tk.DISABLED)
        self.btn_chat.config(state=tk.DISABLED)
        
        if es_creador:
            messagebox.showinfo("Éxito", f"Tu sala '{sala['nombre']}' ha sido eliminada")
        else:
            messagebox.showinfo("Éxito", f"La sala '{sala['nombre']}' ha sido eliminada (acción de administrador)")
    
    def abrir_chat(self):
        """
        Abre una ventana de chat para la sala seleccionada si el usuario es miembro.
        El chat persistirá entre sesiones usando un archivo JSON para almacenar los mensajes.
        """
        seleccion = self.lista_salas.selection()
        if not seleccion:
            return
            
        sala_id = int(seleccion[0])
        
        # Buscar la sala
        sala = None
        for s in self.salas:
            if s["id"] == sala_id:
                sala = s
                break
                
        if not sala:
            return
            
        # Verificar si es miembro
        if self.usuario not in sala["miembros"]:
            messagebox.showinfo("No eres miembro", "Solo los miembros pueden acceder al chat de la sala")
            return
        
        # Archivo para guardar los mensajes del chat
        chat_file = f"chat_sala_{sala_id}.json"
        
        # Cargar mensajes existentes o crear estructura inicial
        mensajes = self.cargar_mensajes_chat(chat_file)
        
        # Crear ventana de chat
        ventana_chat = tk.Toplevel(self.master)
        ventana_chat.title(f"Chat - {sala['nombre']}")
        ventana_chat.geometry("600x500")
        
        ttk.Label(ventana_chat, text=f"Chat de la sala: {sala['nombre']}", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Área de mensajes
        frame_mensajes = ttk.LabelFrame(ventana_chat, text="Mensajes")
        frame_mensajes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_mensajes = scrolledtext.ScrolledText(frame_mensajes, wrap=tk.WORD, height=15)
        text_mensajes.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        text_mensajes.config(state=tk.NORMAL)
        
        # Mostrar mensajes existentes
        self.mostrar_mensajes_chat(text_mensajes, mensajes)
        
        # Entrada de nuevo mensaje
        frame_nuevo = ttk.Frame(ventana_chat)
        frame_nuevo.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_nuevo, text="Tu mensaje:").pack(side=tk.LEFT, padx=5)
        
        entry_mensaje = ttk.Entry(frame_nuevo, width=50)
        entry_mensaje.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        entry_mensaje.focus()
        
        def enviar_mensaje():
            mensaje = entry_mensaje.get().strip()
            if mensaje:
                # Crear nuevo mensaje con timestamp
                nuevo_mensaje = {
                    "usuario": self.usuario,
                    "contenido": mensaje,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Añadir mensaje a la lista
                mensajes.append(nuevo_mensaje)
                
                # Guardar mensajes en archivo
                self.guardar_mensajes_chat(chat_file, mensajes)
                
                # Mostrar mensaje en la interfaz
                text_mensajes.config(state=tk.NORMAL)
                text_mensajes.insert(tk.END, f"[{nuevo_mensaje['timestamp']}] {self.usuario}: {mensaje}\n")
                text_mensajes.see(tk.END)
                text_mensajes.config(state=tk.DISABLED)
                entry_mensaje.delete(0, tk.END)
        
        # Bind Enter key
        entry_mensaje.bind("<Return>", lambda e: enviar_mensaje())
        
        ttk.Button(frame_nuevo, text="Enviar", command=enviar_mensaje).pack(side=tk.LEFT, padx=5)
        
        # Config para actualizar el chat automáticamente
        def actualizar_chat():
            # Cargar mensajes más recientes
            mensajes_actuales = self.cargar_mensajes_chat(chat_file)
            
            # Verificar si hay nuevos mensajes comparando la longitud
            if len(mensajes_actuales) > len(mensajes):
                # Identificar solo los nuevos mensajes
                nuevos_mensajes = mensajes_actuales[len(mensajes):]
                
                # Actualizar nuestra lista local de mensajes
                mensajes.extend(nuevos_mensajes)
                
                # Mostrar solo los nuevos mensajes
                text_mensajes.config(state=tk.NORMAL)
                for msg in nuevos_mensajes:
                    if msg["usuario"] != self.usuario:  # No mostrar nuestros propios mensajes (ya se muestran al enviarlos)
                        text_mensajes.insert(tk.END, f"[{msg['timestamp']}] {msg['usuario']}: {msg['contenido']}\n")
                text_mensajes.see(tk.END)
                text_mensajes.config(state=tk.DISABLED)
            
            # Programar la siguiente actualización en 2 segundos
            if ventana_chat.winfo_exists():  # Verificar que la ventana aún existe
                ventana_chat.after(2000, actualizar_chat)
        
        # Iniciar actualización automática
        ventana_chat.after(2000, actualizar_chat)
        
        # Lista de miembros en línea
        frame_online = ttk.LabelFrame(ventana_chat, text="Miembros en línea")
        frame_online.pack(fill=tk.X, padx=10, pady=10)
        
        lista_online = tk.Listbox(frame_online, height=5)
        scrollbar_online = ttk.Scrollbar(frame_online, orient="vertical", command=lista_online.yview)
        lista_online.configure(yscrollcommand=scrollbar_online.set)
        
        lista_online.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar_online.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Añadir todos los miembros como "en línea"
        for miembro in sala["miembros"]:
            estado = " (tú)" if miembro == self.usuario else ""
            lista_online.insert(tk.END, f"{miembro}{estado} - En línea")
        
        # Botón para cerrar
        ttk.Button(ventana_chat, text="Cerrar chat", 
                  command=ventana_chat.destroy).pack(pady=10)

    def cargar_mensajes_chat(self, archivo):
        """
        Carga los mensajes de chat desde un archivo JSON.
        
        Args:
            archivo (str): Ruta del archivo JSON.
            
        Returns:
            list: Lista de mensajes.
        """
        try:
            if os.path.exists(archivo):
                with open(archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Si no existe el archivo, crear estructura inicial con mensaje de sistema
                mensajes_iniciales = [
                    {
                        "usuario": "Sistema",
                        "contenido": "¡Bienvenido al chat de sala!",
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                ]
                # Guardar estructura inicial
                with open(archivo, 'w', encoding='utf-8') as f:
                    json.dump(mensajes_iniciales, f, ensure_ascii=False, indent=4)
                return mensajes_iniciales
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar mensajes del chat: {str(e)}")
            return []

    def guardar_mensajes_chat(self, archivo, mensajes):
        """
        Guarda los mensajes de chat en un archivo JSON.
        
        Args:
            archivo (str): Ruta del archivo JSON.
            mensajes (list): Lista de mensajes a guardar.
        """
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(mensajes, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar mensajes del chat: {str(e)}")

    def mostrar_mensajes_chat(self, text_widget, mensajes):
        """
        Muestra los mensajes de chat en el widget de texto.
        
        Args:
            text_widget (tk.Text): Widget donde mostrar los mensajes.
            mensajes (list): Lista de mensajes a mostrar.
        """
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        
        for msg in mensajes:
            text_widget.insert(tk.END, f"[{msg['timestamp']}] {msg['usuario']}: {msg['contenido']}\n")
        
        text_widget.see(tk.END)
        text_widget.config(state=tk.DISABLED)