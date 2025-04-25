import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import datetime
import json
import os

class ForoWindow:
    """
    ForoWindow: Interfaz gráfica para un foro de discusión utilizando Tkinter.
    
    Esta clase implementa una ventana de foro que permite a los usuarios crear, visualizar,
    editar y eliminar temas y respuestas. Los datos del foro se almacenan en un archivo JSON.
    
    Atributos:
        master (tk.Tk): La ventana principal de Tkinter.
        usuario (str): Nombre del usuario que ha iniciado sesión.
        data_file (str): Ruta del archivo JSON para almacenar los mensajes.
        botones_respuestas (list): Almacena referencias a los botones de las respuestas.
        mensajes (list): Lista de diccionarios que contienen los mensajes del foro.
        is_admin (bool): Indica si el usuario actual tiene privilegios de administrador.
        juegos (list): Lista de juegos disponibles como temas.
        juego_actual (str): Juego seleccionado para filtrar.
    """
    def __init__(self, master, usuario, is_admin=False):
        """
        Inicializa la ventana del foro.
        
        Args:
            master (tk.Tk): La ventana principal de Tkinter.
            usuario (str): Nombre del usuario que ha iniciado sesión.
            is_admin (bool): Indica si el usuario tiene privilegios de administrador.
        """
        self.master = master
        self.master.title("Tkinder - Foro")
        self.master.geometry("1000x800")
        self.usuario = usuario
        self.is_admin = is_admin
        
        # Archivo para guardar los mensajes y juegos
        self.data_file = "foro_data.json"
        self.juegos_file = "juegos_data.json"
        
        # Para mantener referencia a los botones de las respuestas
        self.botones_respuestas = []
        
        # Juego seleccionado actualmente para filtrar (None = mostrar todos)
        self.juego_actual = None
        
        # Cargar juegos o crear datos iniciales
        self.cargar_juegos()
        
        # Cargar mensajes o crear datos iniciales
        self.cargar_mensajes()
        
        self.crear_widgets()
        
    def cargar_juegos(self):
        """
        Carga la lista de juegos desde el archivo JSON o crea una lista predeterminada.
        """
        try:
            if os.path.exists(self.juegos_file):
                with open(self.juegos_file, 'r', encoding='utf-8') as f:
                    self.juegos = json.load(f)
            else:
                # Lista de juegos predeterminados
                self.juegos = [
                    "League of Legends",
                    "Valorant",
                    "Counter-Strike",
                    "Fortnite",
                    "Minecraft",
                    "Dota 2",
                    "Apex Legends",
                    "Overwatch",
                    "Rocket League",
                    "Call of Duty"
                ]
                self.guardar_juegos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los juegos: {str(e)}")
            self.juegos = []
    
    def guardar_juegos(self):
        """
        Guarda la lista de juegos en el archivo JSON.
        """
        try:
            with open(self.juegos_file, 'w', encoding='utf-8') as f:
                json.dump(self.juegos, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar los juegos: {str(e)}")
        
    def cargar_mensajes(self):
        """
        Carga los mensajes desde el archivo JSON.
        
        Si el archivo no existe, crea mensajes de prueba predeterminados.
        En caso de error, inicializa mensajes como una lista vacía.
        """
        # Intentar cargar mensajes desde el archivo, o crear mensajes de prueba si no existe
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.mensajes = json.load(f)
                    
                    # Asegurar compatibilidad con datos antiguos
                    for mensaje in self.mensajes:
                        if "juego" not in mensaje:
                            mensaje["juego"] = "General"
            else:
                # Mensajes de prueba para mostrar en el foro
                self.mensajes = [
                    {"id": 1, "usuario": "Admin", "fecha": "2025-04-10", "titulo": "Bienvenida", 
                     "contenido": "¡Bienvenidos al foro de Tkinder!", "respuestas": [], "juego": "General"},
                    {"id": 2, "usuario": "JugadorPro", "fecha": "2025-04-10", "titulo": "Busco equipo", 
                     "contenido": "Busco equipo para torneo de fin de semana", "juego": "League of Legends",
                     "respuestas": [
                         {"id": 1, "usuario": "GameMaster", "fecha": "2025-04-10", "contenido": "Yo tengo un grupo, contáctame"},
                         {"id": 2, "usuario": "Novatillo", "fecha": "2025-04-11", "contenido": "¿De qué nivel es el torneo?"}
                     ]},
                ]
                self.guardar_mensajes()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los mensajes: {str(e)}")
            self.mensajes = []
            
    def guardar_mensajes(self):
        """
        Guarda los mensajes en el archivo JSON.
        
        Utiliza encoding utf-8 para preservar caracteres especiales y
        muestra un mensaje de error si ocurre algún problema.
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.mensajes, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar los mensajes: {str(e)}")
        
    def crear_widgets(self):
        """
        Configura todos los widgets de la interfaz gráfica del foro.
        
        Crea la estructura de paneles, botones, listas y áreas de texto
        necesarias para la visualización y gestión de los temas y respuestas.
        """
        # Panel principal
        panel_principal = ttk.PanedWindow(self.master, orient=tk.HORIZONTAL)
        panel_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Lista de temas
        frame_temas = ttk.LabelFrame(panel_principal, text="Temas")
        panel_principal.add(frame_temas, weight=1)
        
        # Frame para filtros y botones
        frame_filtros = ttk.Frame(frame_temas)
        frame_filtros.pack(pady=5, padx=10, fill=tk.X)
        
        # Label para el selector de juegos
        ttk.Label(frame_filtros, text="Filtrar por juego:").pack(side=tk.LEFT, padx=5)
        
        # Combo para seleccionar juego
        self.combo_juegos = ttk.Combobox(frame_filtros, state="readonly")
        self.combo_juegos["values"] = ["Todos"] + sorted(self.juegos)
        self.combo_juegos.current(0)  # Seleccionar "Todos" por defecto
        self.combo_juegos.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.combo_juegos.bind("<<ComboboxSelected>>", self.filtrar_por_juego)
        
        # Botón para administrar juegos (solo para admins)
        if self.is_admin:
            btn_admin_juegos = ttk.Button(frame_filtros, text="Administrar Juegos", command=self.administrar_juegos)
            btn_admin_juegos.pack(side=tk.LEFT, padx=5)
        
        # Frame para botones de temas
        frame_botones = ttk.Frame(frame_temas)
        frame_botones.pack(pady=5, padx=10, fill=tk.X)
        
        # Botón para crear nuevo tema
        btn_nuevo_tema = ttk.Button(frame_botones, text="Nuevo tema", command=self.crear_nuevo_tema)
        btn_nuevo_tema.pack(side=tk.LEFT, padx=5)
        
        # Botón para actualizar la lista
        btn_actualizar = ttk.Button(frame_botones, text="Actualizar", command=self.actualizar_lista)
        btn_actualizar.pack(side=tk.LEFT, padx=5)
        
        # Lista de temas
        self.lista_temas = ttk.Treeview(frame_temas, columns=("titulo", "autor", "fecha", "juego"), show="headings")
        self.lista_temas.heading("titulo", text="Título")
        self.lista_temas.heading("autor", text="Autor")
        self.lista_temas.heading("fecha", text="Fecha")
        self.lista_temas.heading("juego", text="Juego")
        self.lista_temas.column("titulo", width=150)
        self.lista_temas.column("autor", width=80)
        self.lista_temas.column("fecha", width=80)
        self.lista_temas.column("juego", width=100)
        self.lista_temas.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # Cargar temas en la lista
        self.actualizar_lista()
        
        self.lista_temas.bind("<<TreeviewSelect>>", self.mostrar_tema)
        
        # Panel derecho - Contenido del tema
        frame_contenido = ttk.LabelFrame(panel_principal, text="Contenido")
        panel_principal.add(frame_contenido, weight=2)
        
        # Botones para editar/eliminar tema
        self.frame_acciones = ttk.Frame(frame_contenido)
        self.frame_acciones.pack(pady=5, padx=10, fill=tk.X)
        
        self.btn_editar = ttk.Button(self.frame_acciones, text="Editar tema", 
                                     command=self.editar_tema, state=tk.DISABLED)
        self.btn_editar.pack(side=tk.LEFT, padx=5)
        
        self.btn_eliminar = ttk.Button(self.frame_acciones, text="Eliminar tema", 
                                       command=self.eliminar_tema, state=tk.DISABLED)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        # Contenedor para el tema y las respuestas
        self.frame_contenido_tema = ttk.Frame(frame_contenido)
        self.frame_contenido_tema.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Área de visualización del tema principal
        self.texto_tema = scrolledtext.ScrolledText(self.frame_contenido_tema, wrap=tk.WORD, height=10)
        self.texto_tema.pack(fill=tk.BOTH, expand=True, pady=5)
        self.texto_tema.config(state=tk.DISABLED)
        
        # Frame para las respuestas con scroll
        self.frame_respuestas = ttk.LabelFrame(self.frame_contenido_tema, text="Respuestas")
        self.frame_respuestas.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Canvas y scrollbar para las respuestas
        self.canvas_respuestas = tk.Canvas(self.frame_respuestas)
        scrollbar = ttk.Scrollbar(self.frame_respuestas, orient="vertical", command=self.canvas_respuestas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas_respuestas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas_respuestas.configure(scrollregion=self.canvas_respuestas.bbox("all"))
        )
        
        self.canvas_respuestas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_respuestas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas_respuestas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Área para escribir respuesta
        frame_nueva_respuesta = ttk.LabelFrame(frame_contenido, text="Tu respuesta")
        frame_nueva_respuesta.pack(pady=5, padx=10, fill=tk.X)
        
        self.texto_respuesta = scrolledtext.ScrolledText(frame_nueva_respuesta, wrap=tk.WORD, height=5)
        self.texto_respuesta.pack(pady=5, padx=5, fill=tk.X)
        
        ttk.Button(frame_nueva_respuesta, text="Enviar respuesta", 
                  command=self.enviar_respuesta).pack(pady=5, padx=5, anchor=tk.E)
    
    def administrar_juegos(self):
        """
        Permite al administrador gestionar la lista de juegos disponibles.
        
        Muestra una ventana con la lista de juegos actuales, permitiendo añadir y eliminar juegos.
        """
        if not self.is_admin:
            return
            
        ventana_juegos = tk.Toplevel(self.master)
        ventana_juegos.title("Administrar Juegos")
        ventana_juegos.geometry("400x500")
        
        ttk.Label(ventana_juegos, text="Lista de Juegos Disponibles", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Frame para agregar juego
        frame_agregar = ttk.Frame(ventana_juegos)
        frame_agregar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_agregar, text="Nuevo juego:").pack(side=tk.LEFT, padx=5)
        nuevo_juego_entry = ttk.Entry(frame_agregar, width=20)
        nuevo_juego_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        def agregar_juego():
            juego = nuevo_juego_entry.get().strip()
            if not juego:
                messagebox.showwarning("Aviso", "Ingresa un nombre de juego")
                return
                
            if juego in self.juegos:
                messagebox.showwarning("Aviso", "Este juego ya existe en la lista")
                return
                
            self.juegos.append(juego)
            self.juegos.sort()
            self.guardar_juegos()
            
            # Actualizar lista en la ventana de administración
            listbox_juegos.delete(0, tk.END)
            for juego in self.juegos:
                listbox_juegos.insert(tk.END, juego)
                
            # Actualizar combo en ventana principal
            self.combo_juegos["values"] = ["Todos"] + sorted(self.juegos)
                
            nuevo_juego_entry.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Juego añadido correctamente")
        
        ttk.Button(frame_agregar, text="Agregar", command=agregar_juego).pack(side=tk.LEFT, padx=5)
        
        # Listbox para mostrar juegos
        frame_lista = ttk.Frame(ventana_juegos)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox_juegos = tk.Listbox(frame_lista)
        listbox_juegos.pack(fill=tk.BOTH, expand=True)
        
        listbox_juegos.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox_juegos.yview)
        
        # Llenar lista de juegos
        for juego in self.juegos:
            listbox_juegos.insert(tk.END, juego)
        
        def eliminar_juego():
            seleccion = listbox_juegos.curselection()
            if not seleccion:
                messagebox.showwarning("Aviso", "Selecciona un juego para eliminar")
                return
                
            juego = listbox_juegos.get(seleccion[0])
            
            if messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar '{juego}'?\n\nNota: Los temas existentes con este juego se mantendrán, pero no se podrán crear nuevos."):
                self.juegos.remove(juego)
                self.guardar_juegos()
                listbox_juegos.delete(seleccion[0])
                
                # Actualizar combo en ventana principal
                self.combo_juegos["values"] = ["Todos"] + sorted(self.juegos)
                
                messagebox.showinfo("Éxito", "Juego eliminado correctamente")
        
        ttk.Button(ventana_juegos, text="Eliminar juego seleccionado", 
                   command=eliminar_juego).pack(pady=10)
    
    def filtrar_por_juego(self, event=None):
        """
        Filtra la lista de temas según el juego seleccionado en el combo.
        
        Args:
            event: Evento de selección en el Combobox (puede ser None si se llama programáticamente)
        """
        seleccion = self.combo_juegos.get()
        
        # Limpiar lista actual
        for item in self.lista_temas.get_children():
            self.lista_temas.delete(item)
            
        # Filtrar mensajes por juego seleccionado
        for mensaje in self.mensajes:
            if seleccion == "Todos" or mensaje.get("juego") == seleccion:
                self.lista_temas.insert("", tk.END, iid=str(mensaje["id"]), 
                                       values=(mensaje.get("titulo", "Sin título"), 
                                              mensaje["usuario"], 
                                              mensaje["fecha"],
                                              mensaje.get("juego", "General")))
    
    def actualizar_lista(self):
        """
        Actualiza la lista de temas en la interfaz.
        
        Recarga los mensajes desde el archivo y los muestra en el Treeview.
        """
        # Cargar mensajes desde el archivo
        self.cargar_mensajes()
        
        # Actualizar la lista según el filtro actual
        self.filtrar_por_juego()
    
    def mostrar_tema(self, event):
        """
        Muestra el contenido de un tema seleccionado.
        
        Actualiza el área de texto con el contenido del tema y muestra sus respuestas.
        También gestiona la habilitación de botones según el usuario.
        
        Args:
            event: Evento de selección en el Treeview (puede ser None si se llama programáticamente)
        """
        seleccion = self.lista_temas.selection()
        if not seleccion:
            return
            
        tema_id = int(seleccion[0])
        
        # Buscar el mensaje seleccionado
        mensaje = None
        for m in self.mensajes:
            if m["id"] == tema_id:
                mensaje = m
                break
                
        if not mensaje:
            return
            
        # Habilitar/deshabilitar botones según si el usuario es el autor o administrador
        if mensaje["usuario"] == self.usuario or self.is_admin:
            self.btn_editar.config(state=tk.NORMAL)
            self.btn_eliminar.config(state=tk.NORMAL)
        else:
            self.btn_editar.config(state=tk.DISABLED)
            self.btn_eliminar.config(state=tk.DISABLED)
            
        # Mostrar el contenido del tema
        self.texto_tema.config(state=tk.NORMAL)
        self.texto_tema.delete(1.0, tk.END)
        
        titulo = mensaje.get("titulo", "Sin título")
        juego = mensaje.get("juego", "General")
        
        self.texto_tema.insert(tk.END, f"Tema: {titulo}\n", "titulo")
        self.texto_tema.insert(tk.END, f"Juego: {juego}\n", "juego")
        self.texto_tema.insert(tk.END, f"De: {mensaje['usuario']}\n")
        self.texto_tema.insert(tk.END, f"Fecha: {mensaje['fecha']}\n\n")
        self.texto_tema.insert(tk.END, f"{mensaje['contenido']}\n")
        
        # Configurar estilos de texto
        self.texto_tema.tag_configure("titulo", font=("Arial", 12, "bold"))
        self.texto_tema.tag_configure("juego", font=("Arial", 10, "italic"))
        self.texto_tema.config(state=tk.DISABLED)
        
        # Limpiar respuestas anteriores
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Limpiar referencias a botones previos
        self.botones_respuestas = []
        
        # Mostrar las respuestas
        if mensaje['respuestas']:
            for respuesta in mensaje['respuestas']:
                # Crear un frame para cada respuesta
                frame_respuesta = ttk.Frame(self.scrollable_frame, relief=tk.GROOVE, borderwidth=1)
                frame_respuesta.pack(fill=tk.X, expand=True, padx=5, pady=5)
                
                # Información y contenido de la respuesta
                ttk.Label(frame_respuesta, 
                         text=f"De: {respuesta['usuario']} - {respuesta['fecha']}", 
                         font=("Arial", 9, "bold")).pack(anchor=tk.W, padx=5, pady=2)
                
                texto_respuesta = scrolledtext.ScrolledText(frame_respuesta, wrap=tk.WORD, height=4)
                texto_respuesta.pack(fill=tk.X, padx=5, pady=2)
                texto_respuesta.insert(tk.END, respuesta['contenido'])
                texto_respuesta.config(state=tk.DISABLED)
                
                # Botones de editar/eliminar para respuestas del usuario actual o para admin
                if respuesta['usuario'] == self.usuario or self.is_admin:
                    frame_botones = ttk.Frame(frame_respuesta)
                    frame_botones.pack(fill=tk.X, padx=5, pady=2, anchor=tk.E)
                    
                    btn_editar = ttk.Button(frame_botones, text="Editar", 
                                           command=lambda id=respuesta['id']: self.editar_respuesta(id))
                    btn_editar.pack(side=tk.LEFT, padx=2)
                    
                    btn_eliminar = ttk.Button(frame_botones, text="Eliminar", 
                                             command=lambda id=respuesta['id']: self.eliminar_respuesta(id))
                    btn_eliminar.pack(side=tk.LEFT, padx=2)
                    
                    # Guardar referencia a los botones
                    self.botones_respuestas.append((btn_editar, btn_eliminar))
        else:
            ttk.Label(self.scrollable_frame, text="No hay respuestas todavía.").pack(pady=10)
    
    def editar_respuesta(self, id_respuesta):
        """
        Permite al usuario editar su propia respuesta o al administrador editar cualquier respuesta.
        
        Abre una ventana para editar el contenido de una respuesta y actualiza los datos.
        
        Args:
            id_respuesta (int): ID de la respuesta que se va a editar
        """
        seleccion = self.lista_temas.selection()
        if not seleccion:
            return
            
        tema_id = int(seleccion[0])
        
        # Buscar el mensaje y la respuesta
        for mensaje in self.mensajes:
            if mensaje["id"] == tema_id:
                for respuesta in mensaje["respuestas"]:
                    if respuesta["id"] == id_respuesta and (respuesta["usuario"] == self.usuario or self.is_admin):
                        # Abrir ventana de edición
                        ventana_editar = tk.Toplevel(self.master)
                        ventana_editar.title("Editar respuesta")
                        ventana_editar.geometry("500x300")
                        
                        ttk.Label(ventana_editar, text="Contenido:").pack(anchor=tk.W, padx=10, pady=5)
                        texto_editar = scrolledtext.ScrolledText(ventana_editar, wrap=tk.WORD, height=10)
                        texto_editar.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
                        texto_editar.insert(tk.END, respuesta["contenido"])
                        
                        def guardar_cambios():
                            nuevo_contenido = texto_editar.get(1.0, tk.END).strip()
                            if not nuevo_contenido:
                                messagebox.showwarning("Aviso", "El contenido no puede estar vacío")
                                return
                                
                            respuesta["contenido"] = nuevo_contenido
                            
                            # Agregar nota si un administrador ha editado el mensaje
                            if self.is_admin and respuesta["usuario"] != self.usuario:
                                respuesta["fecha"] = datetime.datetime.now().strftime("%Y-%m-%d") + " (editado por admin)"
                            else:
                                respuesta["fecha"] = datetime.datetime.now().strftime("%Y-%m-%d") + " (editado)"
                            
                            self.guardar_mensajes()
                            self.mostrar_tema(None)
                            
                            ventana_editar.destroy()
                            messagebox.showinfo("Éxito", "Respuesta actualizada correctamente")
                            
                        ttk.Button(ventana_editar, text="Guardar cambios", 
                                   command=guardar_cambios).pack(pady=10)
                        return
    
    def eliminar_respuesta(self, id_respuesta):
        """
        Elimina una respuesta creada por el usuario o cualquier respuesta si es administrador.
        
        Pide confirmación antes de eliminar y actualiza los datos y la vista.
        
        Args:
            id_respuesta (int): ID de la respuesta que se va a eliminar
        """
        seleccion = self.lista_temas.selection()
        if not seleccion:
            return
            
        tema_id = int(seleccion[0])
        
        # Pedir confirmación
        if not messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta respuesta?"):
            return
            
        # Buscar el mensaje y eliminar la respuesta
        for mensaje in self.mensajes:
            if mensaje["id"] == tema_id:
                # Si es admin, puede eliminar cualquier respuesta
                if self.is_admin:
                    mensaje["respuestas"] = [r for r in mensaje["respuestas"] if r["id"] != id_respuesta]
                    self.guardar_mensajes()
                    self.mostrar_tema(None)
                    messagebox.showinfo("Éxito", "Respuesta eliminada correctamente (acción de administrador)")
                    return
                else:
                    # Si no es admin, solo puede eliminar sus propias respuestas
                    mensaje["respuestas"] = [r for r in mensaje["respuestas"] 
                                           if not (r["id"] == id_respuesta and r["usuario"] == self.usuario)]
                    
                    self.guardar_mensajes()
                    self.mostrar_tema(None)
                    messagebox.showinfo("Éxito", "Respuesta eliminada correctamente")
                    return
    
    def enviar_respuesta(self):
        """
        Añade una respuesta al tema seleccionado.
        
        Verifica que se haya seleccionado un tema y que el texto de la respuesta
        no esté vacío. Añade la respuesta al tema y actualiza la vista.
        
        Returns:
            None
        """
        seleccion = self.lista_temas.selection()
        respuesta = self.texto_respuesta.get(1.0, tk.END).strip()
        
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un tema para responder")
            return
        
        if not respuesta:
            messagebox.showwarning("Aviso", "Escribe una respuesta")
            return
        
        tema_id = int(seleccion[0])
        
        # Buscar el mensaje
        for i, mensaje in enumerate(self.mensajes):
            if mensaje["id"] == tema_id:
                # Generar ID para la respuesta
                nuevo_id = 1
                if mensaje["respuestas"]:
                    nuevo_id = max([r["id"] for r in mensaje["respuestas"]]) + 1
                
                # Agregar la respuesta al tema seleccionado
                nueva_respuesta = {
                    "id": nuevo_id,
                    "usuario": self.usuario,
                    "fecha": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "contenido": respuesta
                }
                
                mensaje["respuestas"].append(nueva_respuesta)
                
                # Guardar cambios
                self.guardar_mensajes()
                
                # Limpiar el área de respuesta
                self.texto_respuesta.delete(1.0, tk.END)
                
                # Actualizar la visualización del tema
                self.mostrar_tema(None)
                messagebox.showinfo("Éxito", "Tu respuesta ha sido publicada")
                return
    
    def crear_nuevo_tema(self):
        """
        Abre una ventana para crear un nuevo tema.
        
        Permite al usuario introducir un título, seleccionar un juego y añadir contenido
        para un nuevo tema, lo añade a la lista de mensajes y actualiza la vista.
        """
        ventana_nuevo = tk.Toplevel(self.master)
        ventana_nuevo.title("Nuevo tema")
        ventana_nuevo.geometry("700x500")
        
        ttk.Label(ventana_nuevo, text="Título:").pack(anchor=tk.W, padx=10, pady=5)
        titulo_entry = ttk.Entry(ventana_nuevo, width=50)
        titulo_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Selector de juego
        frame_juego = ttk.Frame(ventana_nuevo)
        frame_juego.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_juego, text="Juego:").pack(side=tk.LEFT)
        
        combo_juego_nuevo = ttk.Combobox(frame_juego, state="readonly", width=30)
        combo_juego_nuevo["values"] = ["General"] + sorted(self.juegos)
        combo_juego_nuevo.current(0)  # Seleccionar "General" por defecto
        combo_juego_nuevo.pack(side=tk.LEFT, padx=5)
        
        # Opción para agregar un nuevo juego
        def abrir_agregar_juego():
            ventana_agregar = tk.Toplevel(ventana_nuevo)
            ventana_agregar.title("Agregar nuevo juego")
            ventana_agregar.geometry("400x150")
            
            ttk.Label(ventana_agregar, text="Nombre del nuevo juego:").pack(anchor=tk.W, padx=10, pady=10)
            
            nuevo_juego_entry = ttk.Entry(ventana_agregar, width=40)
            nuevo_juego_entry.pack(fill=tk.X, padx=10, pady=5)
            
            def agregar_juego_y_seleccionar():
                juego = nuevo_juego_entry.get().strip()
                
                if not juego:
                    messagebox.showwarning("Aviso", "Ingresa un nombre de juego")
                    return
                    
                if juego in self.juegos:
                    messagebox.showwarning("Aviso", "Este juego ya existe en la lista")
                    return
                
                self.juegos.append(juego)
                self.juegos.sort()
                self.guardar_juegos()
                
                # Actualizar combos
                combo_juego_nuevo["values"] = ["General"] + sorted(self.juegos)
                combo_juego_nuevo.set(juego)
                
                self.combo_juegos["values"] = ["Todos"] + sorted(self.juegos)
                
                ventana_agregar.destroy()
                messagebox.showinfo("Éxito", f"Juego '{juego}' añadido correctamente")
            
            ttk.Button(ventana_agregar, text="Agregar", 
                       command=agregar_juego_y_seleccionar).pack(pady=10)
        
        ttk.Button(frame_juego, text="Nuevo juego", 
                   command=abrir_agregar_juego).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(ventana_nuevo, text="Contenido:").pack(anchor=tk.W, padx=10, pady=5)
        contenido_text = scrolledtext.ScrolledText(ventana_nuevo, wrap=tk.WORD, height=10)
        contenido_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        def guardar_tema():
            titulo = titulo_entry.get().strip()
            juego = combo_juego_nuevo.get()
            contenido = contenido_text.get(1.0, tk.END).strip()
            
            if not titulo or not contenido:
                messagebox.showwarning("Aviso", "Completa el título y el contenido")
                return
            
            # Generar ID único para el tema
            nuevo_id = 1
            if self.mensajes:
                nuevo_id = max([m["id"] for m in self.mensajes]) + 1
            
            nuevo_tema = {
                "id": nuevo_id,
                "usuario": self.usuario,
                "fecha": datetime.datetime.now().strftime("%Y-%m-%d"),
                "titulo": titulo,
                "contenido": contenido,
                "juego": juego,
                "respuestas": []
            }
            
            self.mensajes.append(nuevo_tema)
            
            # Guardar en archivo
            self.guardar_mensajes()
            
            # Actualizar la lista según filtro actual
            self.actualizar_lista()
            
            # Si estamos filtrando por un juego específico y creamos un tema de otro juego, cambiar al filtro "Todos"
            filtro_actual = self.combo_juegos.get()
            if filtro_actual != "Todos" and filtro_actual != juego:
                self.combo_juegos.current(0)  # Seleccionar "Todos"
                self.filtrar_por_juego()
            
            ventana_nuevo.destroy()
            messagebox.showinfo("Éxito", "Tu tema ha sido publicado")
            
        ttk.Button(ventana_nuevo, text="Publicar", command=guardar_tema).pack(pady=10)
    
    def editar_tema(self):
        """
        Permite al usuario editar su propio tema o al administrador editar cualquier tema.
        
        Verifica que el usuario sea el autor del tema o administrador antes de permitir la edición.
        Abre una ventana para editar el título, juego y contenido del tema.
        """
        seleccion = self.lista_temas.selection()
        if not seleccion:
            return
            
        tema_id = int(seleccion[0])
        
        # Buscar el mensaje
        for mensaje in self.mensajes:
            if mensaje["id"] == tema_id and (mensaje["usuario"] == self.usuario or self.is_admin):
                # Abrir ventana de edición
                ventana_editar = tk.Toplevel(self.master)
                ventana_editar.title("Editar tema")
                ventana_editar.geometry("700x500")
                
                ttk.Label(ventana_editar, text="Título:").pack(anchor=tk.W, padx=10, pady=5)
                titulo_entry = ttk.Entry(ventana_editar, width=50)
                titulo_entry.pack(fill=tk.X, padx=10, pady=5)
                titulo_entry.insert(0, mensaje.get("titulo", ""))
                
                # Selector de juego
                frame_juego = ttk.Frame(ventana_editar)
                frame_juego.pack(fill=tk.X, padx=10, pady=5)
                
                ttk.Label(frame_juego, text="Juego:").pack(side=tk.LEFT)
                
                combo_juego = ttk.Combobox(frame_juego, state="readonly", width=30)
                combo_juego["values"] = ["General"] + sorted(self.juegos)
                
                # Seleccionar el juego actual del tema
                juego_actual = mensaje.get("juego", "General")
                try:
                    combo_juego.set(juego_actual)
                except:
                    combo_juego.current(0)  # Si el juego ya no existe, seleccionar "General"
                
                combo_juego.pack(side=tk.LEFT, padx=5)
                
                ttk.Label(ventana_editar, text="Contenido:").pack(anchor=tk.W, padx=10, pady=5)
                contenido_text = scrolledtext.ScrolledText(ventana_editar, wrap=tk.WORD, height=10)
                contenido_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
                contenido_text.insert(tk.END, mensaje["contenido"])
                
                def guardar_cambios():
                    titulo = titulo_entry.get().strip()
                    juego = combo_juego.get()
                    contenido = contenido_text.get(1.0, tk.END).strip()
                    
                    if not titulo or not contenido:
                        messagebox.showwarning("Aviso", "Completa todos los campos")
                        return
                        
                    mensaje["titulo"] = titulo
                    mensaje["contenido"] = contenido
                    mensaje["juego"] = juego
                    
                    # Agregar nota si un administrador ha editado el mensaje
                    if self.is_admin and mensaje["usuario"] != self.usuario:
                        mensaje["fecha"] = datetime.datetime.now().strftime("%Y-%m-%d") + " (editado por admin)"
                    else:
                        mensaje["fecha"] = datetime.datetime.now().strftime("%Y-%m-%d") + " (editado)"
                    
                    self.guardar_mensajes()
                    
                    # Actualizar la lista y la vista
                    self.actualizar_lista()
                    self.lista_temas.selection_set(str(tema_id))
                    self.mostrar_tema(None)
                    
                    ventana_editar.destroy()
                    messagebox.showinfo("Éxito", "Tema actualizado correctamente")
                    
                ttk.Button(ventana_editar, text="Guardar cambios", 
                           command=guardar_cambios).pack(pady=10)
                return
                
        # Si llegamos aquí, no se encontró el tema o el usuario no es el autor ni administrador
        messagebox.showerror("Error", "No tienes permiso para editar este tema")
    
    def eliminar_tema(self):
        """
        Elimina un tema creado por el usuario o cualquier tema si es administrador.
        
        Verifica que el usuario sea el autor del tema o administrador antes de permitir la eliminación.
        Pide confirmación y actualiza la vista después de eliminar el tema.
        """
        seleccion = self.lista_temas.selection()
        if not seleccion:
            return
            
        tema_id = int(seleccion[0])
        
        # Verificar que el usuario sea el autor o administrador
        tema_encontrado = False
        es_autor = False
        
        for mensaje in self.mensajes:
            if mensaje["id"] == tema_id:
                tema_encontrado = True
                if mensaje["usuario"] == self.usuario:
                    es_autor = True
                elif not self.is_admin:
                    messagebox.showerror("Error", "No tienes permiso para eliminar este tema")
                    return
        
        if not tema_encontrado:
            messagebox.showerror("Error", "Tema no encontrado")
            return
            
        # Pedir confirmación
        if self.is_admin and not es_autor:
            if not messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este tema como administrador?"):
                return
        else:
            if not messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este tema y todas sus respuestas?"):
                return
            
        # Eliminar el tema
        self.mensajes = [m for m in self.mensajes if m["id"] != tema_id]
        
        # Guardar cambios
        self.guardar_mensajes()
        
        # Actualizar la lista
        self.actualizar_lista()
        
        # Limpiar el área de tema
        self.texto_tema.config(state=tk.NORMAL)
        self.texto_tema.delete(1.0, tk.END)
        self.texto_tema.config(state=tk.DISABLED)
        
        # Limpiar respuestas
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Desactivar botones
        self.btn_editar.config(state=tk.DISABLED)
        self.btn_eliminar.config(state=tk.DISABLED)
        
        if self.is_admin and not es_autor:
            messagebox.showinfo("Éxito", "Tema eliminado correctamente (acción de administrador)")
        else:
            messagebox.showinfo("Éxito", "Tema eliminado correctamente")