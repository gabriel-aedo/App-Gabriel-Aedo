import bcrypt
import mongoconn
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

"""El ejecutable de la aplicacion se llama Correos Yury. Es un nombre más descriptivo."""

class App(tk.Tk):
    """Esta clase permite que la app se ejecute, principalmente la ventana.\n
    Se le asigna un titulo a ventana además de hacer que NO sea redimensionable"""
    def __init__(self):
        super().__init__()
        self.resizable(0, 0)
        self.title("El correo de Yury")
        self.frame = None
        self.cambiar_frame(Login, Login.MEDIDAS)

    def cambiar_frame(self, nuevo_frame, medidas: str):
        """Este método permite realizar el cambio de frames.\n
        `self.frame` es la variable que alojará a los diferentes Frames de la app. Por defecto está en None.\n
        El condicional comprueba si se le asignó algún frame a la variable, y de ser así, destruye el frame actual y se cambia por el que
        esté en el parámetro `nuevo_frame`, además de que la ventana se muestra segun las medidas que se le asignen a `medidas`.\n
        Al ejecutar la app, el condicional es ignorado y pasa directamente a mostrar el Frame de la clase `Login`.
        """
        if self.frame != None:
            self.frame.destroy()
        self.frame = nuevo_frame()
        self.frame.pack(fill = tk.BOTH, expand = True)
        self.geometry(medidas)

class Usuario:
    """Clase que permite usar el RUT del usuario en las múltiples clases de la app."""

    def __init__(self):
        self.__rut = None

    def mostrar_rut(self):
        return self.__rut
    
    def actualizar_valor_rut(self, valor):
        self.__rut = valor

usuario = Usuario()

class Login(ttk.Frame):
    """Clase que muestra el Login."""
    MEDIDAS = "375x390"
    def __init__(self):
        super().__init__()

        ttk.Label(self, text = "Usuario:").pack(pady = 10)

        self.__rut_usuario = ttk.Entry(self, width = 35, justify = "center")
        self.__rut_usuario.pack(pady = 3)

        ttk.Label(self, text = "Contraseña:").pack(pady = 3)

        self.__campo_clave = ttk.Entry(self, width = 35, justify = "center", show = "•")
        self.__campo_clave.pack(pady = 3)

        ttk.Button(self, text = "Iniciar sesión", width = 35, command = self.__validar_datos).pack(pady = 15)

        self.__label_login = ttk.Label(self)
        self.__label_login.pack()

    def __buscar_rut(self):
        """Busca el RUT ingresado en el campo de 'Usuario' """
        return conn.encontrar_data({"_id": self.__rut_usuario.get()})

    def __validar_largo_datos(self):
        """Revisa si el RUT y clave ingresados tienen al menos 8 caracteres"""
        return len(self.__rut_usuario.get()) >= 8 and len(self.__campo_clave.get()) >= 8

    def __validar_rut(self):
        """Se valida que el RUT ingresado esté en la base de datos"""
        return self.__buscar_rut() is not None and self.__rut_usuario.get() == self.__buscar_rut()["_id"]
        
    def __validar_clave(self):
        """Se compara mediante bcrypt que la clave ingresada sea la misma que se ubica en la base de datos (que está hasheada)"""
        if self.__buscar_rut() is not None:
            return bcrypt.checkpw(self.__campo_clave.get().encode(), self.__buscar_rut()["clave"])
        return False
        
    def __validar_datos(self):
        """Se validan el RUT y clave ingresados, así como sus longitudes. Si todos son correctos, permite ir al inicio de la app.\n
        En caso contrario, se muestra un mensaje."""
        if all([self.__validar_largo_datos(), self.__validar_rut(), self.__validar_clave()]):
            self.__label_login["text"] = "¡Correcto!"
            usuario.actualizar_valor_rut(self.__rut_usuario.get())   
            self.__label_login.after(500, lambda: app.cambiar_frame(Inicio, Inicio.MEDIDAS))
        else:
            self.__label_login["text"] = "Nombre de usuario o clave incorrectos"
            self.__label_login.after(1000, lambda: self.__label_login.config(text = ""))

class Inicio(ttk.Frame):
    """Clase encargada de mostrar los botones según el perfil de cada usuario."""
    MEDIDAS = "300x300"
    def __init__(self):
        super().__init__()

        ttk.Label(self, text = "Bienvenido. ¿Qué harás hoy?").pack(pady = 10)

        self.__perfiles = {
            "Trabajador": [("Modificar datos", Trabajador)],
            "Personal RR.HH": [("Ingresar nuevo trabajador", FormularioRRHH), ("Tabla resumen", TablaResumen)],
            "Jefe RR.HH": [("Tabla trabajadores", TablaTrabajadores)]
        }

        self.__botones = self.__perfiles.get(conn.encontrar_data({"_id": usuario.mostrar_rut()})["cargo"], ())

        for nombre, clase in self.__botones:
            ttk.Button(self, text = nombre, command = lambda c = clase: app.cambiar_frame(c, c.MEDIDAS)).pack(pady = 5)

class Trabajador(ttk.Frame):
    """Clase encargada de mostrar los datos del trabajador, para que pueda modificarlos."""
    MEDIDAS = "575x550"
    def __init__(self):
        super().__init__()
        
        self.__container_frames = ttk.Frame(self)
        self.__container_frames.pack(fill = "both", expand = True)

        self.__marco_personal = ttk.Labelframe(self.__container_frames, text = "Datos personales")
        self.__marco_personal.pack(padx = 15, pady = 5, ipadx = 120, ipady = 2)

        self.__marco_emergencia = ttk.Labelframe(self.__container_frames, text = "Contacto de emergencia")
        self.__marco_emergencia.pack(padx = 15, pady = 5, ipadx = 120, ipady = 2)

        self.__marco_cargas = ttk.Labelframe(self.__container_frames, text = "Datos cargas familiares")
        self.__marco_cargas.pack(padx = 15, pady = 5, ipadx = 120, ipady = 2)

        ttk.Label(self.__marco_personal, text = "RUT:").grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__campo_rut = ttk.Entry(self.__marco_personal, width = 25, state = "normal")
        self.__campo_rut.insert(0, usuario.mostrar_rut())
        self.__campo_rut.config(state = "disabled")
        self.__campo_rut.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = "w")

        ttk.Label(self.__marco_personal, text = "Nombre completo:").grid(row = 2, column = 0, padx = 5, pady = 5)

        self.__campo_nombre = ttk.Entry(self.__marco_personal, width = 55)
        self.__campo_nombre.insert(0, conn.encontrar_data({"_id": usuario.mostrar_rut()})["nombre"])
        self.__campo_nombre.grid(row = 2, column = 1, padx = 5, pady = 5)

        self.__var_personal = tk.StringVar()

        self.__var_personal.set(conn.encontrar_data({"_id": usuario.mostrar_rut()})["sexo"])

        ttk.Label(self.__marco_personal, text = "Sexo:").grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "e")
        
        self.__casilla_sexo_masculino = ttk.Radiobutton(self.__marco_personal, text = "Masculino", variable = self.__var_personal, value = "Masculino")
        self.__casilla_sexo_masculino.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = "w")

        self.__casilla_sexo_femenino = ttk.Radiobutton(self.__marco_personal, text = "Femenino", variable = self.__var_personal, value = "Femenino")
        self.__casilla_sexo_femenino.grid(row = 3, column = 1, padx = 5, pady = 5)

        ttk.Label(self.__marco_emergencia, text = "Nombre contacto:").grid(row = 4, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__campo_contacto = ttk.Entry(self.__marco_emergencia, width = 55)
        self.__campo_contacto.insert(0, conn.encontrar_data({"_id": usuario.mostrar_rut()})["nombre_contacto_emergencia"])
        self.__campo_contacto.grid(row = 4, column = 1, padx = 5, pady = 5, sticky = "w")

        ttk.Label(self.__marco_emergencia, text = "Relacion con trabajador:").grid(row = 5, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__campo_relacion = ttk.Entry(self.__marco_emergencia, width = 25)
        self.__campo_relacion.insert(0, conn.encontrar_data({"_id": usuario.mostrar_rut()})["tipo_de_relacion"])
        self.__campo_relacion.grid(row = 5, column = 1, padx = 5, pady = 5, sticky = "w")

        ttk.Label(self.__marco_emergencia, text = "Teléfono:").grid(row = 6, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__campo_telefono_contacto = ttk.Entry(self.__marco_emergencia, width = 25)
        self.__campo_telefono_contacto.insert(0, conn.encontrar_data({"_id": usuario.mostrar_rut()})["telefono_contacto"])
        self.__campo_telefono_contacto.grid(row = 6, column = 1, padx = 5, pady = 5, sticky = "w")
        
        self.__frame_cargas = ttk.Frame(self.__marco_cargas)
        self.__frame_cargas.pack(fill = "both", expand = True)

        self.__frame_widgets_cargas = ttk.Frame(self.__frame_cargas)
        self.__frame_widgets_cargas.grid(row = 7, column = 0, sticky = "w")

        ttk.Label(self.__frame_widgets_cargas, text = "RUT carga:").grid(row = 7, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__campo_rut_carga = ttk.Entry(self.__frame_widgets_cargas, width = 25)
        self.__campo_rut_carga.grid(row = 7, column = 1, padx = 5, pady = 5, sticky = "w")

        ttk.Label(self.__frame_widgets_cargas, text = "Nombre carga:").grid(row = 8, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__campo_nombre_carga = ttk.Entry(self.__frame_widgets_cargas, width = 55)
        self.__campo_nombre_carga.grid(row = 8, column = 1, padx = 5, pady = 5, sticky = "w")

        ttk.Label(self.__frame_widgets_cargas, text = "Parentesco:").grid(row = 9, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__parentesco_carga = ttk.Combobox(self.__frame_widgets_cargas, state = "readonly", values = ["Cónyuge", "Hijo", "Hija"])
        self.__parentesco_carga.grid(row = 9, column = 1, padx = 5, pady = 5, sticky = "w")

        ttk.Label(self.__frame_widgets_cargas, text = "Sexo carga:").grid(row = 10, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__var_carga = tk.StringVar()

        self.__casilla_sexo_masculino = ttk.Radiobutton(self.__frame_widgets_cargas, text = "Masculino", variable = self.__var_carga, value = "Masculino")
        self.__casilla_sexo_masculino.grid(row = 10, column = 1, padx = 5, pady = 5, sticky = "w")

        self.__casilla_sexo_femenino = ttk.Radiobutton(self.__frame_widgets_cargas, text = "Femenino", variable = self.__var_carga, value = "Femenino")
        self.__casilla_sexo_femenino.grid(row = 10, column = 1, padx = 5, pady = 5)

        self.__boton_agregar_carga = ttk.Button(self.__frame_widgets_cargas, text = "Agregar carga", command = self.insertar_carga_a_lista)
        self.__boton_agregar_carga.grid(row = 11, column = 0, padx = 5, pady = 5, sticky = "w")

        self.__boton_eliminar_carga = ttk.Button(self.__frame_widgets_cargas, text = "Eliminar carga", command = self.eliminar_carga)
        self.__boton_eliminar_carga.grid(row = 11, column = 1, padx = 5, pady = 5, sticky = "w")
        
        self.__frame_tabla_cargas = ttk.Frame(self.__frame_cargas)
        self.__frame_tabla_cargas.grid(row = 12, column = 0, padx = 5, pady = 5, sticky = "w")

        self.__listbox_cargas = tk.Listbox(self.__frame_tabla_cargas, height = 3)
        self.__listbox_cargas.grid(row = 12, column = 0, ipadx = 30, sticky = "w")

        self.__array_cargas = []

        self.__boton_insertar = ttk.Button(self, text = "Guardar cambios", command = self.guardar_cambios)
        self.__boton_insertar.pack(pady = 5, anchor = "w")

        ttk.Button(self, text= "🡸", width = 10, command = lambda: app.cambiar_frame(Inicio, Inicio.MEDIDAS)).pack(pady = 5, padx = 10, side = "left", before = self.__boton_insertar)

        self.__datos_bbdd = conn.encontrar_data({"_id": usuario.mostrar_rut()})
        
        self.mostrar_cargas()

    def buscar_widgets_de_cargas_vacios(self):
        """Funciona igual que `buscar_widgets_vacios()`, pero esta es especificamente
        para los widgets de las cargas familiares, debido a que Labelframe `marco_cargas`
        contiene muchos `Frame` en su interior por un tema de estructura"""
        estado = False
        for widget in self.__frame_widgets_cargas.winfo_children():
            if isinstance(widget, (ttk.Entry, ttk.Combobox)):
                if widget.get() == "":
                    estado = True
            elif isinstance(widget, ttk.Radiobutton):
                if self.__var_carga.get() == "":
                    estado = True
        return estado
    
    def guardar_cambios(self):
        """Compara los datos del documento de MongoDB con los del formulario. Si nota algún cambio,
        se actualizará esa información. Se omiten los campos relacionados con los datos laborales y el RUT (_id).\n
        El contador `nro_datos_modificados` sirve para que el mensaje de Cambio de datos no se muestre por cada campo modificado, y solo se visualice una vez
        """
        nro_datos_modificados = 0

        campos = {
            "nombre": self.__campo_nombre.get(),
            "sexo": self.__var_personal.get(),
            "nombre_contacto_emergencia": self.__campo_contacto.get(),
            "tipo_de_relacion": self.__campo_relacion.get(),
            "telefono_contacto": self.__campo_telefono_contacto.get(),
            "cargas_familiares": "N/A" if self.__array_cargas == [] else self.__array_cargas
        }
        for dato, campo in campos.items():
            if self.__datos_bbdd.get(dato) != campo:
                conn.actualizar_data({"_id": usuario.mostrar_rut()}, {"$set": {dato: campo} })
                nro_datos_modificados += 1

        if nro_datos_modificados > 0:
            messagebox.showinfo("Cambio de datos", "Los datos han sido actualizados con exito")
            app.cambiar_frame(Inicio, Inicio.MEDIDAS)

    def insertar_carga_a_lista(self):
        """Este método ingresa la carga al Listbox, que a la vez se agrega al array `self.__array_cargas`. Tambien se evita el ingreso de datos nulos o vacíos al Listbox.\n
        Una vez que se ingresa, los datos se borran de los widgets, y queda visible el RUT de la carga en el Listbox.
        """
        if self.buscar_widgets_de_cargas_vacios():
            messagebox.showwarning("Aviso", "Todos los campos de la carga deben estar llenos")
        else:
            self.__array_cargas.append({"rut": self.__campo_rut_carga.get(), "nombre_carga": self.__campo_nombre_carga.get(), "parentesco": self.__parentesco_carga.get(), "sexo_carga": self.__var_carga.get()})
            self.__listbox_cargas.insert("end", self.__array_cargas[-1]["rut"])
            for widget in self.__frame_widgets_cargas.winfo_children():
                if isinstance(widget, (ttk.Entry)):
                    widget.delete(0, "end")
                if isinstance(widget, (ttk.Combobox)):
                    widget.set("")
                if isinstance(widget, (ttk.Radiobutton)):
                    self.__var_carga.set(None)

    def mostrar_cargas(self):
        """Muestra el RUT de las cargas familiares en el Listbox y agrega la información de las cargas al array"""
        consulta_info_cargas = [
            {"$match": {"_id": usuario.mostrar_rut()}},
            {"$unwind": "$cargas_familiares"},
            {"$project": {"_id": 0, "rut": "$cargas_familiares.rut", "nombre_carga": "$cargas_familiares.nombre_carga", "parentesco": "$cargas_familiares.parentesco", "sexo_carga": "$cargas_familiares.sexo_carga"}}]

        for carga in conn.encontrar_data_aggregate(consulta_info_cargas):
            self.__array_cargas.append(carga)
            self.__listbox_cargas.insert("end", carga.get("rut"))

    def eliminar_carga(self):
        """La carga es eliminada del Listbox y del array"""
        for x in self.__listbox_cargas.curselection():
            self.__listbox_cargas.delete(x)
            self.__array_cargas.pop(x)

class FormularioRRHH(ttk.Frame):
    """Clase encargada de permitir que el personal de RR.HH pueda ingresar a los usuarios al sistema"""
    MEDIDAS = "575x760"
    def __init__(self):
        super().__init__()

        self.__container_frames = ttk.Frame(self)
        
        self.__container_frames.pack(fill = "both", expand = True)

        self.__marco_personal = ttk.Labelframe(self.__container_frames, text = "Datos personales")
        self.__marco_personal.pack(padx = 15, pady = 5, ipadx = 120, ipady = 2)

        self.__marco_laboral = ttk.Labelframe(self.__container_frames, text = "Datos laborales")
        self.__marco_laboral.pack(padx = 15, pady = 5, ipadx = 120, ipady = 2)

        self.__marco_emergencia = ttk.Labelframe(self.__container_frames, text = "Contacto de emergencia")
        self.__marco_emergencia.pack(padx = 15, pady = 5, ipadx = 120, ipady = 2)

        self.__marco_cargas = ttk.Labelframe(self.__container_frames, text = "Datos cargas familiares")
        self.__marco_cargas.pack(padx = 15, pady = 5, ipadx = 120, ipady = 2)

        ttk.Label(self.__marco_personal, text = "RUT:").grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__campo_rut = ttk.Entry(self.__marco_personal, width = 25)
        self.__campo_rut.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = "w")

        ttk.Label(self.__marco_personal, text = "Nombre completo:").grid(row = 2, column = 0, padx = 5, pady = 5)

        self.__campo_nombre = ttk.Entry(self.__marco_personal, width = 55)
        self.__campo_nombre.grid(row = 2, column = 1, padx = 5, pady = 5)

        self.__var_personal = tk.StringVar()

        ttk.Label(self.__marco_personal, text = "Sexo:").grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "e")
        
        self.__casilla_sexo_masculino = ttk.Radiobutton(self.__marco_personal, text = "Masculino", variable = self.__var_personal, value = "Masculino")
        self.__casilla_sexo_masculino.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = "w")

        self.__casilla_sexo_femenino = ttk.Radiobutton(self.__marco_personal, text = "Femenino", variable = self.__var_personal, value = "Femenino")
        self.__casilla_sexo_femenino.grid(row = 3, column = 1, padx = 5, pady = 5)

        ttk.Label(self.__marco_laboral, text = "Dirección:").grid(row = 4, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__campo_direccion = ttk.Entry(self.__marco_laboral, width = 60)
        self.__campo_direccion.grid(row = 4, column = 1, padx = 5, pady = 5, sticky = "w")

        ttk.Label(self.__marco_laboral, text = "Teléfono:").grid(row = 5, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__campo_telefono = ttk.Entry(self.__marco_laboral, width = 23)
        self.__campo_telefono.grid(row = 5, column = 1, padx = 5, pady = 5, sticky = "w")

        ttk.Label(self.__marco_laboral, text = "Cargo:").grid(row = 6, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__cuadro_cargo = ttk.Combobox(self.__marco_laboral, state = "readonly", values = ["Trabajador", "Personal RR.HH", "Jefe RR.HH"])
        self.__cuadro_cargo.grid(row = 6, column = 1, padx = 5, pady = 5, sticky = "w")

        ttk.Label(self.__marco_laboral, text = "Fecha de ingreso:").grid(row = 7, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__campo_fecha_ingreso = ttk.Entry(self.__marco_laboral, width = 23)
        self.__campo_fecha_ingreso.grid(row = 7, column = 1, padx = 5, pady = 5, sticky = "w")

        ttk.Label(self.__marco_laboral, text = "Área:").grid(row = 8, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__areas = {
            "Logistica": ["Recepción", "Almacenamiento", "Distribución"],
            "Tecnologia": ["Desarrollo de Software", "Redes y comunicaciones"],
            "Servicio al cliente": ["Atencion al cliente", "Calidad"]
        }

        self.__cuadro_area = ttk.Combobox(self.__marco_laboral, state = "readonly", values = [area for area in self.__areas])
        self.__cuadro_area.grid(row = 8, column = 1, padx = 5, pady = 5, sticky = "w")

        ttk.Label(self.__marco_laboral, text = "Departamento:").grid(row = 9, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__cuadro_depto = ttk.Combobox(self.__marco_laboral, state = "readonly")
        self.__cuadro_depto.grid(row = 9, column = 1, padx = 5, pady = 5, sticky = "w")

        self.__cuadro_area.bind("<<ComboboxSelected>>", self.mostrar_deptos)

        ttk.Label(self.__marco_emergencia, text = "Nombre contacto:").grid(row = 10, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__campo_contacto = ttk.Entry(self.__marco_emergencia, width = 55)
        self.__campo_contacto.grid(row = 10, column = 1, padx = 5, pady = 5, sticky = "w")

        ttk.Label(self.__marco_emergencia, text = "Relacion con trabajador:").grid(row = 11, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__campo_relacion = ttk.Entry(self.__marco_emergencia, width = 25)
        self.__campo_relacion.grid(row = 11, column = 1, padx = 5, pady = 5, sticky = "w")

        ttk.Label(self.__marco_emergencia, text = "Teléfono:").grid(row = 12, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__campo_telefono_contacto = ttk.Entry(self.__marco_emergencia, width = 25)
        self.__campo_telefono_contacto.grid(row = 12, column = 1, padx = 5, pady = 5, sticky = "w")

        self.__frame_cargas = ttk.Frame(self.__marco_cargas)
        self.__frame_cargas.pack(fill = "both", expand = True)

        self.__frame_widgets_cargas = ttk.Frame(self.__frame_cargas)
        self.__frame_widgets_cargas.grid(row = 13, column = 0, sticky = "w")

        ttk.Label(self.__frame_widgets_cargas, text = "RUT carga:").grid(row = 13, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__campo_rut_carga = ttk.Entry(self.__frame_widgets_cargas, width = 25)
        self.__campo_rut_carga.grid(row = 13, column = 1, padx = 5, pady = 5, sticky = "w")

        ttk.Label(self.__frame_widgets_cargas, text = "Nombre carga:").grid(row = 14, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__campo_nombre_carga = ttk.Entry(self.__frame_widgets_cargas, width = 55)
        self.__campo_nombre_carga.grid(row = 14, column = 1, padx = 5, pady = 5, sticky = "w")

        ttk.Label(self.__frame_widgets_cargas, text = "Parentesco:").grid(row = 15, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__parentesco_carga = ttk.Combobox(self.__frame_widgets_cargas, state = "readonly", values = ["Cónyuge", "Hijo", "Hija"])
        self.__parentesco_carga.grid(row = 15, column = 1, padx = 5, pady = 5, sticky = "w")

        ttk.Label(self.__frame_widgets_cargas, text = "Sexo carga:").grid(row = 16, column = 0, padx = 5, pady = 5, sticky = "e")

        self.__var_carga = tk.StringVar()

        self.__casilla_sexo_masculino = ttk.Radiobutton(self.__frame_widgets_cargas, text = "Masculino", variable = self.__var_carga, value = "Masculino")
        self.__casilla_sexo_masculino.grid(row = 16, column = 1, padx = 5, pady = 5, sticky = "w")

        self.__casilla_sexo_femenino = ttk.Radiobutton(self.__frame_widgets_cargas, text = "Femenino", variable = self.__var_carga, value = "Femenino")
        self.__casilla_sexo_femenino.grid(row = 16, column = 1, padx = 5, pady = 5)

        self.__boton_agregar_carga = ttk.Button(self.__frame_widgets_cargas, text = "Agregar carga", command = self.insertar_carga_a_lista)
        self.__boton_agregar_carga.grid(row = 17, column = 0, padx = 5, pady = 3, sticky = "w")
        
        self.__boton_eliminar_carga = ttk.Button(self.__frame_widgets_cargas, text = "Eliminar carga", command = self.eliminar_carga)
        self.__boton_eliminar_carga.grid(row = 17, column = 1, padx = 5, pady = 5, sticky = "w")
        
        self.__frame_tabla_cargas = ttk.Frame(self.__frame_cargas)
        self.__frame_tabla_cargas.grid(row = 18, column = 0, padx = 5, pady = 5, sticky = "w")

        self.__listbox_cargas = tk.Listbox(self.__frame_tabla_cargas, height = 3)
        self.__listbox_cargas.grid(row = 18, column = 0, ipadx = 30, sticky = "w")

        self.__array_cargas = []

        self.__boton_insertar = ttk.Button(self, text = "Ingresar", command = self.ingresar_usuario)
        self.__boton_insertar.pack(pady = 5, anchor = "w")

        ttk.Button(self, text= "🡸", width = 10, command = lambda: app.cambiar_frame(Inicio, Inicio.MEDIDAS)).pack(pady = 5, padx = 10, side = "left", before = self.__boton_insertar)
        
    def buscar_widgets_vacios(self):
        """Este método permite ingresar al usuario a la BBDD.\n
        Recorre todos los Labelframe (excepto el de cargas familiares), pero recorriendo primero
        el frame que contiene a todos los Labelframe, para verificar
        si widgets como los `Entry`, `Combobox` y `Radiobutton` están completos. Si encuentra alguno
        de ellos vacío, `estado` pasa a True y el método retorna dicho estado.\n
        El Labelframe `marco_cargas` no se recorre porque existe la posibilidad de que un usuario
        no tenga cargas familiares."""
        estado = False
        for marco in self.__container_frames.winfo_children():
            if marco is self.__marco_cargas:
                continue
            for widget in marco.winfo_children():
                
                if isinstance(widget, (ttk.Entry, ttk.Combobox)):
                    if widget.get() == "":
                        estado = True
                elif isinstance(widget, ttk.Radiobutton):
                    if self.__var_personal.get() == "":
                        estado = True
        return estado
    
    
    def buscar_widgets_de_cargas_vacios(self):
        """Funciona igual que ` buscar_widgets_vacios()`, pero esta es especificamente
        para los widgets de las cargas familiares, debido a que Labelframe `marco_cargas`
        contiene muchos `Frame` en su interior por un tema de estructura"""
        estado = False
        for widget in self.__frame_widgets_cargas.winfo_children():
            if isinstance(widget, (ttk.Entry, ttk.Combobox)):
                if widget.get() == "":
                    estado = True
            elif isinstance(widget, ttk.Radiobutton):
                if self.__var_carga.get() == "":
                    estado = True

        return estado
    
    def insertar_carga_a_lista(self):
        """Este método ingresa la carga al Listbox, que a la vez se agrega al array `__array_cargas`. Tambien se evita el ingreso de datos nulos o vacíos al Listbox.\n
        Una vez que se ingresa, los datos se borran de los widgets, y queda visible el RUT de la carga en el Listbox.
        """
        if self.buscar_widgets_de_cargas_vacios():
            messagebox.showwarning("Aviso", "Todos los campos de la carga deben estar llenos")
        else:
            self.__array_cargas.append({"rut": self.__campo_rut_carga.get(), "nombre_carga": self.__campo_nombre_carga.get(), "parentesco": self.__parentesco_carga.get(), "sexo_carga": self.__var_carga.get()})
            self.__listbox_cargas.insert("end", self.__array_cargas[-1]["rut"])
            for widget in self.__frame_widgets_cargas.winfo_children():
                if isinstance(widget, (ttk.Entry)):
                    widget.delete(0, "end")
                if isinstance(widget, (ttk.Combobox)):
                    widget.set("")
                if isinstance(widget, (ttk.Radiobutton)):
                    self.__var_carga.set(None)

    def eliminar_carga(self):
        """La carga es eliminada del Listbox y del array"""
        for x in self.__listbox_cargas.curselection():
            self.__listbox_cargas.delete(x)
            self.__array_cargas.pop(x)

    def mostrar_deptos(self, evt):
        """Se muestran los departamentos del área que se haya elegido"""
        area_seleccionada = self.__cuadro_area.get()
        deptos_area = self.__areas.get(area_seleccionada, [])
        self.__cuadro_depto["values"] = deptos_area
        if self.__cuadro_depto.get() != "":
            self.__cuadro_depto.set("")
            
    def ingresar_usuario(self):
        """Se ingresa el usuario a la BBDD cuando todos los widgets de `Labelframe` (exceptuando `marco_cargas`) estén completados.\n
        Se crea una clave que consiste en 'cyury' mas los 3 últimos dígitos del RUT sin contar el dígito verificador.\n
        Muestra un mensaje de aviso si encuentra algún widget vacío, y de éxito si es el caso contrario."""
        rut_bbdd = conn.encontrar_data({"_id": self.__campo_rut.get()})
        
        if self.buscar_widgets_vacios():
            messagebox.showwarning("Aviso", "Faltan campos por rellenar")
        elif len(self.__campo_rut.get()) < 8 or len(self.__campo_rut.get()) >= 10:
            messagebox.showwarning("Aviso", "El RUT del usuario está mal escrito")
        elif rut_bbdd and rut_bbdd["_id"]:
            messagebox.showwarning("Aviso", "El RUT ya existe")
        else:
            contenido_campo_rut = self.__campo_rut.get()
            clave = "cyury" + str(contenido_campo_rut[-4:-1])
            clave_encode = clave.encode()
            salt = bcrypt.gensalt()
            clave_hasheada = bcrypt.hashpw(clave_encode, salt)
            conn.insertar_data({
                    "_id": self.__campo_rut.get(),
                    "nombre": self.__campo_nombre.get(),
                    "clave": clave_hasheada,
                    "sexo": self.__var_personal.get(),
                    "direccion": self.__campo_direccion.get(),
                    "telefono": self.__campo_telefono.get(),
                    "cargo": self.__cuadro_cargo.get(),
                    "fecha_ingreso_a_compania": self.__campo_fecha_ingreso.get(),
                    "area": self.__cuadro_area.get(),
                    "depto": self.__cuadro_depto.get(),
                    "nombre_contacto_emergencia": self.__campo_contacto.get(),
                    "tipo_de_relacion": self.__campo_relacion.get(),
                    "telefono_contacto": self.__campo_telefono_contacto.get(),
                    "cargas_familiares": "N/A" if self.__array_cargas == [] else self.__array_cargas
                })
            messagebox.showinfo("Éxito", "Usuario ingresado con éxito")

class TablaResumen(ttk.Frame):
     """Clase encargada de mostrar una tabla con los trabajadores, mostrando el RUT, nombre, sexo y cargo"""
     MEDIDAS = "975x490"
     def __init__(self):
        super().__init__()
                
        self.__columnas = ("RUT", "Nombre", "Sexo", "Cargo")

        self.__tabla = ttk.Treeview(self, columns = self.__columnas, show = "headings", height = 20)

        self.__scrollbar = ttk.Scrollbar(self, orient = "vertical", command = self.__tabla.yview)
        self.__scrollbar.pack(side = "right", fill = "y")

        self.__tabla.pack(expand = True, fill= "y", anchor = "center", ipadx = 50)

        ttk.Button(self, text= "🡸", width = 25, command = lambda: app.cambiar_frame(Inicio, Inicio.MEDIDAS)).pack(pady = 15)

        self.__tabla.heading("RUT", text = "RUT")
        self.__tabla.heading("Nombre", text = "Nombre")
        self.__tabla.heading("Sexo", text = "Sexo")
        self.__tabla.heading("Cargo", text = "Cargo")
        self.__tabla.configure(yscrollcommand = self.__scrollbar.set)
        
        for datos in conn.encontrar_data_aggregate([ {"$project": {"_id": 1, "nombre": 1, "sexo": 1, "cargo": 1} } ]):
            rut, nombre, sexo, cargo = datos["_id"], datos["nombre"], datos["sexo"], datos["cargo"]
            self.__tabla.insert("", "end", values = (rut, nombre, sexo, cargo))

class TablaTrabajadores(ttk.Frame):
    """Clase encargada de mostrar una tabla en la que se puede mostrar los trabajadores mediante filtros.\n
    Con la ayuda de eventos ( .bind() ), los filtros hacen efecto cuando se eligen."""
    MEDIDAS = "1375x550"
    def __init__(self):
        super().__init__()

        self.__columnas = ("RUT", "Nombre", "Sexo", "Cargo", "Area", "Departamento")

        self.__areas = {
            "Logistica": ["Recepción", "Almacenamiento", "Distribución"],
            "Tecnologia": ["Desarrollo de Software", "Redes y comunicaciones"],
            "Servicio al cliente": ["Atencion al cliente", "Calidad"]
        }

        self.__frame_filtros = ttk.Frame(self)
        self.__frame_filtros.pack(side = "top", anchor = "center", fill = "x", padx = 25, pady = 15)

        self.__cuadro_sexo = ttk.Combobox(self.__frame_filtros, state = "readonly", values = ["Masculino", "Femenino"])
        self.__cuadro_sexo.pack(side = "left", padx = 5)

        self.__cuadro_cargo = ttk.Combobox(self.__frame_filtros, state = "readonly", values = ["Trabajador", "Personal RR.HH", "Jefe RR.HH"])
        self.__cuadro_cargo.pack(side = "left", padx = 5)

        self.__cuadro_area = ttk.Combobox(self.__frame_filtros, state = "readonly", values = [area for area in self.__areas])
        self.__cuadro_area.pack(side = "left", padx = 5)

        self.__cuadro_depto = ttk.Combobox(self.__frame_filtros, state = "readonly")
        self.__cuadro_depto.pack(side = "left", padx = 5)

        self.__tabla_trabajadores = ttk.Treeview(self, columns = self.__columnas, show = "headings", height = 20)

        self.__scrollbar = ttk.Scrollbar(self, orient = "vertical", command = self.__tabla_trabajadores.yview)
        self.__scrollbar.pack(side = "right", fill = "y")

        self.__tabla_trabajadores.pack(expand = True, fill= "y", anchor = "center", ipadx = 50)

        ttk.Button(self, text= "🡸", width = 25, command = lambda: app.cambiar_frame(Inicio, Inicio.MEDIDAS)).pack(pady = 15)

        self.__tabla_trabajadores.heading("RUT", text = "RUT")
        self.__tabla_trabajadores.heading("Nombre", text = "Nombre")
        self.__tabla_trabajadores.heading("Sexo", text = "Sexo")
        self.__tabla_trabajadores.heading("Cargo", text = "Cargo")
        self.__tabla_trabajadores.heading("Area", text = "Área")
        self.__tabla_trabajadores.heading("Departamento", text = "Depto.")

        self.__tabla_trabajadores.configure(yscrollcommand = self.__scrollbar.set)

        self.__consulta_project = { "$project": { "_id": 1, "nombre": 1, "sexo": 1, "cargo": 1, "area": 1, "depto": 1 } }

        self.insertar_datos_a_tabla()
        
        self.__cuadro_sexo.bind("<<ComboboxSelected>>", lambda evt: self.mostrar_info_segun_filtros({"sexo": self.__cuadro_sexo.get()}))
        self.__cuadro_cargo.bind("<<ComboboxSelected>>", lambda evt: self.mostrar_info_segun_filtros({"cargo": self.__cuadro_cargo.get()}))
        self.__cuadro_area.bind("<<ComboboxSelected>>", lambda evt: self.mostrar_info_segun_filtros({"area": self.__cuadro_area.get()}))
        self.__cuadro_depto.bind("<<ComboboxSelected>>", lambda evt: self.mostrar_info_segun_filtros({"depto": self.__cuadro_depto.get()}))

        self.__filtro = {}

    def insertar_fila(self, datos):
        """Inserta los datos como RUT, nombre, sexo, cargo, area y departamento de los trabajadores a la tabla.\n
        Se usa """
        rut, nombre, sexo, cargo, area, depto = datos["_id"], datos["nombre"], datos["sexo"], datos["cargo"], datos["area"], datos["depto"]
        self.__tabla_trabajadores.insert("", "end", values = (rut, nombre, sexo, cargo, area, depto))

    def insertar_datos_a_tabla(self):
        """Se complementa con `insertar_fila()`, pues se le pasa una query de tipo aggregate (`self.__consulta_project`) con todos los datos que se mostrarán en la tabla."""
        datos_por_aggregate = conn.encontrar_data_aggregate([self.__consulta_project])
        for datos in datos_por_aggregate:
            self.insertar_fila(datos)

    def mostrar_info_segun_filtros(self, datos: dict = {}):
        """Borra los datos de la tabla, para luego obtener el valor de clave presente en el argumento que se le pase a `datos`.\n
        Cuando eso pasa, se crea en `self.__filtro` una clave, y un valor que corresponde a lo que se eligió de algún Combobox.\n
        Los valores de `self.__filtro` pueden ir cambiando mientras se elijan datos diferentes.\n
        Se hace una query de tipo aggregate que busca datos que coincidan con `self.__filtro`, y los inserta a la tabla."""
        self.__tabla_trabajadores.delete(*self.__tabla_trabajadores.get_children())
        if datos.get("sexo"):
            self.__filtro["sexo"] = datos["sexo"]
        if datos.get("cargo"):
            self.__filtro["cargo"] = datos["cargo"]
        if datos.get("area"):
            self.__filtro["area"] = datos["area"]
            self.mostrar_deptos()
        if datos.get("depto"):
            self.__filtro["depto"] = datos["depto"]
        nuevos_datos = conn.encontrar_data_aggregate([{"$match": self.__filtro}, self.__consulta_project])
        for dato in nuevos_datos:
            self.insertar_fila(dato)

    def mostrar_deptos(self):
        """Se muestran los departamentos del área que se haya elegido."""
        area_seleccionada = self.__cuadro_area.get()
        deptos_area = self.__areas.get(area_seleccionada, [])
        self.__cuadro_depto["values"] = deptos_area
        if self.__cuadro_depto.get() != "":
            self.__cuadro_depto.set("")
        
if __name__ == "__main__":
    """Aquí es donde la se muestra la ventana de la aplicacion"""
    app = App()
    conn = mongoconn.MongoConn()
    app.mainloop()