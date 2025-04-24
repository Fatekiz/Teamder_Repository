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
    """
    def __init__(self, master, usuario):
        """
        Inicializa la ventana del foro.
        
        Args:
            master (tk.Tk): La ventana principal de Tkinter.
            usuario (str): Nombre del usuario que ha iniciado sesión.
        """
        self.master = master
        self.master.title("Tkinder - Foro")
        self.master.geometry("1000x800")
        self.usuario = usuario
        
        # Archivo para guardar los mensajes
        self.data_file = "foro_data.json"
        
        # Para mantener referencia a los botones de las respuestas
        self.botones_respuestas = []
        
        # Cargar mensajes o crear datos iniciales
        self.cargar_mensajes()
        
        self.crear_widgets()
        
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
            else:
                # Mensajes de prueba para mostrar en el foro
                self.mensajes = [
                    {"id": 1, "usuario": "Admin", "fecha": "2025-04-10", "titulo": "Bienvenida", 
                     "contenido": "¡Bienvenidos al foro de Tkinder!", "respuestas": []},
                    {"id": 2, "usuario": "JugadorPro", "fecha": "2025-04-10", "titulo": "Busco equipo", 
                     "contenido": "Busco equipo para torneo de fin de semana", 
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
        
        # Frame para botones
        frame_botones = ttk.Frame(frame_temas)
        frame_botones.pack(pady=5, padx=10, fill=tk.X)
        
        # Botón para crear nuevo tema
        btn_nuevo_tema = ttk.Button(frame_botones, text="Nuevo tema", command=self.crear_nuevo_tema)
        btn_nuevo_tema.pack(side=tk.LEFT, padx=5)
        
        # Botón para actualizar la lista
        btn_actualizar = ttk.Button(frame_botones, text="Actualizar", command=self.actualizar_lista)
        btn_actualizar.pack(side=tk.LEFT, padx=5)
        
        # Lista de temas
        self.lista_temas = ttk.Treeview(frame_temas, columns=("titulo", "autor", "fecha"), show="headings")
        self.lista_temas.heading("titulo", text="Título")
        self.lista_temas.heading("autor", text="Autor")
        self.lista_temas.heading("fecha", text="Fecha")
        self.lista_temas.column("titulo", width=150)
        self.lista_temas.column("autor", width=100)
        self.lista_temas.column("fecha", width=100)
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
    
    def actualizar_lista(self):
        """
        Actualiza la lista de temas en la interfaz.
        
        Recarga los mensajes desde el archivo y los muestra en el Treeview.
        """
        # Limpiar lista actual
        for item in self.lista_temas.get_children():
            self.lista_temas.delete(item)
            
        # Cargar mensajes desde el archivo
        self.cargar_mensajes()
        
        # Insertar temas en la lista
        for mensaje in self.mensajes:
            self.lista_temas.insert("", tk.END, iid=str(mensaje["id"]), 
                                   values=(mensaje.get("titulo", "Sin título"), 
                                          mensaje["usuario"], 
                                          mensaje["fecha"]))
    
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
            
        # Habilitar/deshabilitar botones según si el usuario es el autor
        if mensaje["usuario"] == self.usuario:
            self.btn_editar.config(state=tk.NORMAL)
            self.btn_eliminar.config(state=tk.NORMAL)
        else:
            self.btn_editar.config(state=tk.DISABLED)
            self.btn_eliminar.config(state=tk.DISABLED)
            
        # Mostrar el contenido del tema
        self.texto_tema.config(state=tk.NORMAL)
        self.texto_tema.delete(1.0, tk.END)
        
        titulo = mensaje.get("titulo", "Sin título")
        self.texto_tema.insert(tk.END, f"Tema: {titulo}\n", "titulo")
        self.texto_tema.insert(tk.END, f"De: {mensaje['usuario']}\n")
        self.texto_tema.insert(tk.END, f"Fecha: {mensaje['fecha']}\n\n")
        self.texto_tema.insert(tk.END, f"{mensaje['contenido']}\n")
        
        # Configurar estilos de texto
        self.texto_tema.tag_configure("titulo", font=("Arial", 12, "bold"))
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
                
                # Botones de editar/eliminar solo para respuestas del usuario actual
                if respuesta['usuario'] == self.usuario:
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
        Permite al usuario editar su propia respuesta.
        
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
                    if respuesta["id"] == id_respuesta and respuesta["usuario"] == self.usuario:
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
        Elimina una respuesta creada por el usuario.
        
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
        
        Permite al usuario introducir un título y contenido para un nuevo tema,
        lo añade a la lista de mensajes y actualiza la vista.
        """
        ventana_nuevo = tk.Toplevel(self.master)
        ventana_nuevo.title("Nuevo tema")
        ventana_nuevo.geometry("700x500")
        
        ttk.Label(ventana_nuevo, text="Título:").pack(anchor=tk.W, padx=10, pady=5)
        titulo_entry = ttk.Entry(ventana_nuevo, width=50)
        titulo_entry.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(ventana_nuevo, text="Contenido:").pack(anchor=tk.W, padx=10, pady=5)
        contenido_text = scrolledtext.ScrolledText(ventana_nuevo, wrap=tk.WORD, height=10)
        contenido_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        def guardar_tema():
            titulo = titulo_entry.get().strip()
            contenido = contenido_text.get(1.0, tk.END).strip()
            
            if not titulo o...
                messagebox.showwarning("Aviso", "Completa todos los campos")
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
                "respuestas": []
            }
            
            self.mensajes.append(nuevo_tema)
            
            # Guardar en archivo
            self.guardar_mensajes()
            
            # Actualizar la lista
            self.lista_temas.insert("", tk.END, iid=str(nuevo_id), 
                                    values=(titulo, nuevo_tema["usuario"], nuevo_tema["fecha"]))
            
            ventana_nuevo.destroy()
            messagebox.showinfo("Éxito", "Tu tema ha sido publicado")
            
        ttk.Button(ventana_nuevo, text="Publicar", command=guardar_tema).pack(pady=10)
    
    def editar_tema(self):
        """
        Permite al usuario editar su propio tema.
        
        Verifica que el usuario sea el autor del tema antes de permitir la edición.
        Abre una ventana para editar el título y contenido del tema.
        """
        seleccion = self.lista_temas.selection()
        if not seleccion:
            return
            
        tema_id = int(seleccion[0])
        
        # Buscar el mensaje
        for mensaje in self.mensajes:
            if mensaje["id"] == tema_id and mensaje["usuario"] == self.usuario:
                # Abrir ventana de edición
                ventana_editar = tk.Toplevel(self.master)
                ventana_editar.title("Editar tema")
                ventana_editar.geometry("700x500")
                
                ttk.Label(ventana_editar, text="Título:").pack(anchor=tk.W, padx=10, pady=5)
                titulo_entry = ttk.Entry(ventana_editar, width=50)
                titulo_entry.pack(fill=tk.X, padx=10, pady=5)
                titulo_entry.insert(0, mensaje.get("titulo", ""))
                
                ttk.Label(ventana_editar, text="Contenido:").pack(anchor=tk.W, padx=10, pady=5)
                contenido_text = scrolledtext.ScrolledText(ventana_editar, wrap=tk.WORD, height=10)
                contenido_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
                contenido_text.insert(tk.END, mensaje["contenido"])
                
                def guardar_cambios():
                    titulo = titulo_entry.get().strip()
                    contenido = contenido_text.get(1.0, tk.END).strip()
                    
                    if not titulo or not contenido:
                        messagebox.showwarning("Aviso", "Completa todos los campos")
                        return
                        
                    mensaje["titulo"] = titulo
                    mensaje["contenido"] = contenido
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
                
        # Si llegamos aquí, no se encontró el tema o el usuario no es el autor
        messagebox.showerror("Error", "No tienes permiso para editar este tema")
    
    def eliminar_tema(self):
        """
        Elimina un tema creado por el usuario.
        
        Verifica que el usuario sea el autor del tema antes de permitir la eliminación.
        Pide confirmación y actualiza la vista después de eliminar el tema.
        """
        seleccion = self.lista_temas.selection()
        if not seleccion:
            return
            
        tema_id = int(seleccion[0])
        
        # Verificar que el usuario sea el autor
        tema_encontrado = False
        for mensaje in self.mensajes:
            if mensaje["id"] == tema_id:
                tema_encontrado = True
                if mensaje["usuario"] != self.usuario:
                    messagebox.showerror("Error", "No tienes permiso para eliminar este tema")
                    return
        
        if not tema_encontrado:
            messagebox.showerror("Error", "Tema no encontrado")
            return
            
        # Pedir confirmación
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
        
        messagebox.showinfo("Éxito", "Tema eliminado correctamente")