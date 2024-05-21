import tkinter as tk
import subprocess
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import PhotoImage


class Paciente:
    def __init__(self, nombre, especie, raza, edad, propietario):
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad
        self.propietario = propietario
        self.historial_medico = []

    def agregar_historial(self, registro):
        self.historial_medico.append(registro)

    def obtener_historial_completo(self):
        historial_completo = "Historial Médico:\n"
        for registro in self.historial_medico:
            historial_completo += f"Fecha: {registro.fecha}, Descripción: {registro.descripcion}\n"
        return historial_completo

class RegistroMedico:
    def __init__(self, fecha, descripcion):
        self.fecha = fecha
        self.descripcion = descripcion

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Pacientes")

        # Conexión a la base de datos
        self.conn = sqlite3.connect('clinica_veterinaria.db')
        self.cursor = self.conn.cursor()

        # Interfaz gráfica
        self.notebook = ttk.Notebook(root)
        self.notebook.pack()

        # Pestaña para registrar pacientes
        self.frame_registro = tk.Frame(self.notebook)
        self.notebook.add(self.frame_registro, text="Registrar Paciente")

        self.label_nombre = tk.Label(self.frame_registro, text="Nombre:", bg="#ADD8E6")
        self.label_nombre.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_nombre = tk.Entry(self.frame_registro)
        self.entry_nombre.grid(row=0, column=1, padx=60, pady=5)

        self.label_especie = tk.Label(self.frame_registro, text="Especie:", bg="#ADD8E6")
        self.label_especie.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_especie = tk.Entry(self.frame_registro)
        self.entry_especie.grid(row=1, column=1, padx=60, pady=5)

        self.label_raza = tk.Label(self.frame_registro, text="Raza:", bg="#ADD8E6")
        self.label_raza.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_raza = tk.Entry(self.frame_registro)
        self.entry_raza.grid(row=2, column=1, padx=60, pady=5)

        self.label_edad = tk.Label(self.frame_registro, text="Edad:", bg="#ADD8E6")
        self.label_edad.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry_edad = tk.Entry(self.frame_registro)
        self.entry_edad.grid(row=3, column=1, padx=60, pady=5)

        self.label_propietario = tk.Label(self.frame_registro, text="Propietario:", bg="#ADD8E6")
        self.label_propietario.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.entry_propietario = tk.Entry(self.frame_registro)
        self.entry_propietario.grid(row=4, column=1, padx=60, pady=5)

        self.boton_registrar = tk.Button(self.frame_registro, text="Registrar Paciente", command=self.registrar_paciente, bg="#ADD8E6")
        self.boton_registrar.grid(row=5, column=0, columnspan=2, padx=40, pady=30)

        self.boton_limpiar = tk.Button(self.frame_registro, text="Limpiar", command=self.limpiar_campos, bg="#ADD8E6")
        self.boton_limpiar.grid(row=3, column=2, columnspan=2, padx=60, pady=5)

        # Pestaña para actualizar datos de pacientes
        self.frame_actualizar = tk.Frame(self.notebook)
        self.notebook.add(self.frame_actualizar, text="Actualizar Paciente")

        self.label_actualizar_nombre = tk.Label(self.frame_actualizar, text="Nombre del Paciente:", bg="#ADD8E6")
        self.label_actualizar_nombre.grid(row=0, column=0, padx=3, pady=3)
        self.entry_actualizar_nombre = tk.Entry(self.frame_actualizar)
        self.entry_actualizar_nombre.grid(row=0,column=1, padx=3, pady=3)
        self.label_actualizar_especie = tk.Label(self.frame_actualizar, text="Especie:", bg="#ADD8E6")
        self.label_actualizar_especie.grid(row=1, column=0, padx=3, pady=3)
        self.entry_actualizar_especie = tk.Entry(self.frame_actualizar)
        self.entry_actualizar_especie.grid(row=1, column=1, padx=3, pady=3)

        self.label_actualizar_raza = tk.Label(self.frame_actualizar, text="Raza:", bg="#ADD8E6")
        self.label_actualizar_raza.grid(row=2, column=0, padx=3, pady=3)
        self.entry_actualizar_raza = tk.Entry(self.frame_actualizar)
        self.entry_actualizar_raza.grid(row=2, column=1, padx=3, pady=3)

        self.label_actualizar_edad = tk.Label(self.frame_actualizar, text="Edad:", bg="#ADD8E6")
        self.label_actualizar_edad.grid(row=3, column=0, padx=3, pady=3)
        self.entry_actualizar_edad = tk.Entry(self.frame_actualizar)
        self.entry_actualizar_edad.grid(row=3, column=1, padx=3, pady=3)

        self.label_actualizar_propietario = tk.Label(self.frame_actualizar, text="Propietario:", bg="#ADD8E6")
        self.label_actualizar_propietario.grid(row=4, column=0, padx=3, pady=3)
        self.entry_actualizar_propietario = tk.Entry(self.frame_actualizar)
        self.entry_actualizar_propietario.grid(row=4, column=1, padx=3, pady=3)

        self.boton_mostrar_datos = tk.Button(self.frame_actualizar, text="Mostrar Datos", command=self.mostrar_datos_paciente, bg="#ADD8E6")
        self.boton_mostrar_datos.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.boton_actualizar =  tk.Button(self.frame_actualizar, text="Actualizar Paciente", command=self.actualizar_paciente, bg="#ADD8E6")
        self.boton_actualizar.grid(row=5, column=2, columnspan=2, padx=10, pady=10)

        self.boton_limpiar = tk.Button(self.frame_actualizar, text="Limpiar Campos", command=self.limpiar_campos, bg="#ADD8E6")
        self.boton_limpiar.grid(row=3, column=3, columnspan=2, padx=3, pady=3)

        #programar cita
        self.frame_citas = tk.Frame(self.notebook)
        self.notebook.add(self.frame_citas, text="Programar Cita")

        self.label_cita_nombre = tk.Label(self.frame_citas, text="Nombre del Paciente:", bg="#ADD8E6")
        self.label_cita_nombre.grid(row=0, column=0, padx=10, pady=5)
        self.entry_cita_nombre = tk.Entry(self.frame_citas)
        self.entry_cita_nombre.grid(row=0, column=1, padx=10, pady=5)

        self.label_cita_Consulta = tk.Label(self.frame_citas, text="ID Consulta:", bg="#ADD8E6")
        self.label_cita_Consulta.grid(row=1, column=0, padx=10, pady=5)
        self.entry_cita_Consulta = tk.Entry(self.frame_citas)
        self.entry_cita_Consulta.grid(row=1, column=1, padx=10, pady=5)

        self.label_cita_diagnostico = tk.Label(self.frame_citas, text="diagnostico:", bg="#ADD8E6")
        self.label_cita_diagnostico.grid(row=2, column=0, padx=10, pady=5)
        self.entry_cita_diagnostico = tk.Entry(self.frame_citas)
        self.entry_cita_diagnostico.grid(row=2, column=1, padx=10, pady=5)


        self.label_cita_fecha = tk.Label(self.frame_citas, text="Fecha:", bg="#ADD8E6")
        self.label_cita_fecha.grid(row=3, column=0, padx=10, pady=5)
        self.entry_cita_fecha = tk.Entry(self.frame_citas)
        self.entry_cita_fecha.grid(row=3, column=1, padx=10, pady=5)

        self.label_cita_hora = tk.Label(self.frame_citas, text="Hora:", bg="#ADD8E6")
        self.label_cita_hora.grid(row=4, column=0, padx=10, pady=5)
        self.entry_cita_hora = tk.Entry(self.frame_citas)
        self.entry_cita_hora.grid(row=4, column=1, padx=10, pady=5)

        self.boton_programar_cita = tk.Button(self.frame_citas, text="Programar Cita", command=self.programar_cita, bg="#ADD8E6")
        self.boton_programar_cita.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.boton_limpiar_cita = tk.Button(self.frame_citas, text="Limpiar Campos", command=self.limpiar_campos_cita, bg="#ADD8E6")
        self.boton_limpiar_cita.grid(row=3, column=4, columnspan=2, padx=10, pady=5)


        # Pestaña para consulta médica
        self.frame_consulta_medica = tk.Frame(self.notebook)
        self.notebook.add(self.frame_consulta_medica, text="Consulta Médica")

        self.label_id_diagnostico_consulta = tk.Label(self.frame_consulta_medica, text="ID de Consulta Médica:", bg="#ADD8E6")
        self.label_id_diagnostico_consulta.grid(row=0, column=0)
        self.entry_id_diagnostico_consulta = tk.Entry(self.frame_consulta_medica)
        self.entry_id_diagnostico_consulta.grid(row=0, column=1)

        self.boton_buscar_consulta = tk.Button(self.frame_consulta_medica, text="buscar Consulta", command=self.buscar_consulta_medica, bg="#ADD8E6")
        self.boton_buscar_consulta.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

        self.boton_limpiar_consulta = tk.Button(self.frame_consulta_medica, text="Limpiar Campos", command=self.limpiar_campos_consulta, bg="#ADD8E6")
        self.boton_limpiar_consulta.grid(row=0, column=3, columnspan=2, padx=8, pady=8)

        self.boton_historial_medico = tk.Button(self.frame_consulta_medica, text="Historial Médico", command=self.mostrar_historial_medico, bg="#ADD8E6")
        self.boton_historial_medico.grid(row=0, column=2, columnspan=1)

        self.boton_guardar = tk.Button(self.frame_consulta_medica, text="Guardar", command=self.guardar_datos, bg="#ADD8E6")
        self.boton_guardar.grid(row=2, column=2, padx=8, pady=8)

        # Crear la tabla
        self.tabla_consultas = ttk.Treeview(self.frame_consulta_medica, columns=("Nombre del Paciente", "Diagnóstico", "Fecha", "Hora"))
        self.tabla_consultas.grid(row=1, column=0, columnspan=5, padx=8, pady=8)

        # Encabezados de la tabla
        self.tabla_consultas.heading("Nombre del Paciente", text="Nombre del Paciente")
        self.tabla_consultas.heading("Diagnóstico", text="Diagnóstico")
        self.tabla_consultas.heading("Fecha", text="Fecha")
        self.tabla_consultas.heading("Hora", text="Hora")


        # Pestaña para gestionar inventario de medicamentos y suministros
        self.frame_inventario = tk.Frame(self.notebook)
        self.notebook.add(self.frame_inventario, text="Inventario")

        self.label_nombre_medicamento = tk.Label(self.frame_inventario, text="Nombre del Medicamento:", bg="#ADD8E6")
        self.label_nombre_medicamento.grid(row=0, column=0, padx=10, pady=10)
        self.entry_nombre_medicamento = tk.Entry(self.frame_inventario)
        self.entry_nombre_medicamento.grid(row=0, column=1, padx=10, pady=10)

        self.label_existencias = tk.Label(self.frame_inventario, text="Existencias:", bg="#ADD8E6")
        self.label_existencias.grid(row=1, column=0, padx=10, pady=10)
        self.entry_existencias = tk.Entry(self.frame_inventario)
        self.entry_existencias.grid(row=1, column=1, padx=10, pady=10)

        self.label_precio = tk.Label(self.frame_inventario, text="Precio:", bg="#ADD8E6")
        self.label_precio.grid(row=2, column=0, padx=10, pady=10)
        self.entry_precio = tk.Entry(self.frame_inventario)
        self.entry_precio.grid(row=2, column=1, padx=10, pady=10)

        self.boton_registrar_medicamento = tk.Button(self.frame_inventario, text="Registrar Medicamento", command=self.registrar_medicamento, bg="#ADD8E6")
        self.boton_registrar_medicamento.grid(row=3, column=0, columnspan=2, padx=10 , pady=30)

        self.boton_actualizar_existencias = tk.Button(self.frame_inventario, text="Actualizar Existencias", command=self.actualizar_existencias, bg="#ADD8E6")
        self.boton_actualizar_existencias.grid(row=3, column=2, columnspan=2, padx=10, pady=30)

        self.boton_limpiar = tk.Button(self.frame_inventario, text="Limpiar", command=self.limpiar_campos, bg="#ADD8E6")
        self.boton_limpiar.grid(row=1, column=3, padx=10)
        

        # Radio buttons para sumar o descontar existencias
        self.accion_var = tk.StringVar(value="sumar")
        self.radio_sumar = tk.Radiobutton(self.frame_inventario, text="Sumar", variable=self.accion_var, value="sumar", bg="#ADD8E6")
        self.radio_sumar.grid(row=1, column=2, padx=10)
        self.radio_descontar = tk.Radiobutton(self.frame_inventario, text="Descontar", variable=self.accion_var, value="descontar", bg="#ADD8E6")
        self.radio_descontar.grid(row=2, column=2, padx=10)

        for frame in self.notebook.winfo_children():
            frame.configure(bg="#ADD8E6")


    def mostrar_historial_medico(self):
        # Ejecutar el archivo historial_medico.py
        subprocess.Popen(["python", "historial_medico.py"])


    def buscar_consulta_medica(self):
        id_consulta = self.entry_id_diagnostico_consulta.get()
        if not id_consulta:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un ID de consulta médica.")
            return

        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('clinica_veterinaria.db')
            cursor = conn.cursor()

            # Buscar el ID de consulta en la tabla programar_cita
            cursor.execute("SELECT nombre_paciente, diagnostico, fecha, hora FROM programar_cita WHERE id_consulta = ?", (id_consulta,))
            resultado = cursor.fetchone()

            if resultado:
                nombre_paciente, diagnostico, fecha, hora = resultado
                messagebox.showinfo("Éxito", f"El ID de consulta médica {id_consulta} ha sido encontrado.")
                # Limpiar la tabla antes de insertar el nuevo resultado
                for item in self.tabla_consultas.get_children():
                    self.tabla_consultas.delete(item)
                # Insertar el resultado en la tabla
                self.tabla_consultas.insert("", "end", values=(nombre_paciente, diagnostico, fecha, hora))
            else:
                messagebox.showwarning("No encontrado", f"El ID de consulta médica {id_consulta} no se encontró.")

            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"Ha ocurrido un error: {e}")

    def limpiar_campos(self):
        self.entry_nombre_medicamento.delete(0, tk.END)
        self.entry_existencias.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_especie.delete(0, tk.END)
        self.entry_raza.delete(0, tk.END)
        self.entry_edad.delete(0, tk.END)
        self.entry_propietario.delete(0, tk.END)
        self.entry_actualizar_nombre.delete(0, 'end')
        self.entry_actualizar_especie.delete(0, 'end')
        self.entry_actualizar_raza.delete(0, 'end')
        self.entry_actualizar_edad.delete(0, 'end')
        self.entry_actualizar_propietario.delete(0, 'end')

    def limpiar_campos_consulta(self):
        self.entry_id_diagnostico_consulta.delete(0, 'end')
        self.limpiar_tabla()

    def limpiar_tabla(self):
        for item in self.tabla_consultas.get_children():
            self.tabla_consultas.delete(item)
    
    def limpiar_busqueda(self):
        # Limpiar campo de entrada
        self.entry_buscar_nombre.delete(0, tk.END)

        # Limpiar la tabla de historial
        for record in self.tree.get_children():
            self.tree.delete(record)

        # Limpiar la tabla consultas_medicas en la base de datos
        self.cursor.execute("DELETE FROM consultas_medicas")
        self.conn.commit()
    
    def limpiar_campos_cita(self):
        self.entry_cita_nombre.delete(0, 'end')
        self.entry_cita_Consulta.delete(0, 'end')
        self.entry_cita_diagnostico.delete(0, 'end')
        self.entry_cita_fecha.delete(0, 'end')
        self.entry_cita_hora.delete(0, 'end')

    def registrar_medicamento(self):
        nombre_medicamento = self.entry_nombre_medicamento.get()
        try:
            existencias = int(self.entry_existencias.get())  # Convertir a entero
            precio = float(self.entry_precio.get())  # Convertir a flotante
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos para existencias y precio.")
            return

        # Conexión a la base de datos
        try:
            conn = sqlite3.connect('clinica_veterinaria.db')
            cursor = conn.cursor()

            # Verificar si el medicamento ya existe
            cursor.execute("SELECT nombre FROM medicamentos WHERE nombre = ?", (nombre_medicamento,))
            if cursor.fetchone() is not None:
                messagebox.showerror("Error", f"El medicamento '{nombre_medicamento}' ya está registrado.")
                return

            # Insertar medicamento en la tabla
            cursor.execute("INSERT INTO medicamentos (nombre, existencias, precio) VALUES (?, ?, ?)",
                           (nombre_medicamento, existencias, precio))

            # Confirmar cambios
            conn.commit()

            messagebox.showinfo("Registro de Medicamento", f"Medicamento '{nombre_medicamento}' registrado correctamente.")
        except sqlite3.Error as e:
            messagebox.showerror("Error en la Base de Datos", f"No se pudo registrar el medicamento: {e}")
        finally:
            # Cerrar conexión
            conn.close()

    def actualizar_existencias(self):
        nombre_medicamento = self.entry_nombre_medicamento.get()
        try:
            existencias = int(self.entry_existencias.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un valor válido para existencias.")
            return

        accion = self.accion_var.get()
        # Conexión a la base de datos
        try:
            conn = sqlite3.connect('clinica_veterinaria.db')
            cursor = conn.cursor()

            # Obtener existencias actuales
            cursor.execute("SELECT existencias FROM medicamentos WHERE nombre = ?", (nombre_medicamento,))
            resultado = cursor.fetchone()

            if resultado is None:
                messagebox.showwarning("Medicamento no encontrado", f"No se encontró el medicamento '{nombre_medicamento}'.")
                return

            existencias_actuales = resultado[0]

            if accion == "sumar":
                nuevas_existencias = existencias_actuales + existencias
            else:  # descontar
                nuevas_existencias = existencias_actuales - existencias

            # Actualizar existencias en la tabla
            cursor.execute("UPDATE medicamentos SET existencias = ? WHERE nombre = ?",
                           (nuevas_existencias, nombre_medicamento))

            # Confirmar cambios
            conn.commit()

            messagebox.showinfo("Actualización de Existencias", f"Existencias del medicamento '{nombre_medicamento}' actualizadas correctamente.")
        except sqlite3.Error as e:
            messagebox.showerror("Error en la Base de Datos", f"No se pudo actualizar las existencias: {e}")
        finally:
            # Cerrar conexión
            conn.close()



    def registrar_paciente(self):
        nombre = self.entry_nombre.get()
        especie = self.entry_especie.get()
        raza = self.entry_raza.get()
        edad = self.entry_edad.get()
        propietario = self.entry_propietario.get()

        self.cursor.execute("INSERT INTO pacientes (nombre, especie, raza, edad, propietario) VALUES (?, ?, ?, ?, ?)",
                            (nombre, especie, raza, edad, propietario))
        self.conn.commit()

        messagebox.showinfo("Registro de Paciente", f"Paciente '{nombre}' registrado correctamente.")

    def mostrar_datos_paciente(self):
        # Obtener el nombre del paciente
        nombre_paciente = self.entry_actualizar_nombre.get()

        # Consultar datos del paciente en la base de datos
        self.cursor.execute("SELECT * FROM pacientes WHERE nombre=?", (nombre_paciente,))
        paciente = self.cursor.fetchone()

        # Mostrar los datos del paciente en los campos correspondientes
        if paciente:
            self.entry_actualizar_especie.insert(0, paciente[2])
            self.entry_actualizar_raza.insert(0, paciente[3])
            self.entry_actualizar_edad.insert(0, paciente[4])
            self.entry_actualizar_propietario.insert(0, paciente[5])
           
        else:
            messagebox.showerror("Error", f"No se encontró al paciente '{nombre_paciente}'.")

    def actualizar_paciente(self):
        nombre = self.entry_actualizar_nombre.get()
        especie = self.entry_actualizar_especie.get()
        raza = self.entry_actualizar_raza.get()
        edad = self.entry_actualizar_edad.get()
        propietario = self.entry_actualizar_propietario.get()

        # Actualizar datos del paciente en la base de datos
        self.cursor.execute("UPDATE pacientes SET especie=?, raza=?, edad=?, propietario=? WHERE nombre=?",
                            (especie, raza, edad, propietario, nombre))
        self.conn.commit()

        messagebox.showinfo("Actualización de Paciente", f"Datos del paciente '{nombre}' actualizados correctamente.")
    

    def programar_cita(self):
       
        nombre_paciente = self.entry_cita_nombre.get()
        id_Consulta = self.entry_cita_Consulta.get()
        diagnostico = self.entry_cita_diagnostico.get()  # Aquí está el cambio
        fecha = self.entry_cita_fecha.get()
        hora = self.entry_cita_hora.get()

        if not nombre_paciente or not id_Consulta or not fecha or not hora:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Guardar cita en la base de datos
        self.cursor.execute("INSERT INTO programar_cita (nombre_paciente, id_Consulta, diagnostico, fecha, hora) VALUES (?, ?, ?, ?, ?)", 
                    (nombre_paciente, id_Consulta, diagnostico, fecha, hora))

        self.conn.commit()
        
        messagebox.showinfo("Éxito", "Cita programada exitosamente.")


    def guardar_consulta_medica(self):
        # Obtener el valor de id_Consulta_medica del campo de entrada
        id_Consulta_medica = self.entry_id_diagnostico_consulta.get()

        nombre_paciente = self.entry_nombre_paciente.get()
        tratamiento = self.entry_tratamiento.get()
        medicamentos = self.entry_medicamentos.get()

        # Insertar consulta médica en la base de datos
        self.cursor.execute("INSERT INTO consultas_medicas (id_Consulta_medica, nombre_paciente, tratamiento, medicamentos) VALUES (?, ?, ?, ?)",
                            (id_Consulta_medica, nombre_paciente, tratamiento, medicamentos))
        self.conn.commit()

        messagebox.showinfo("Consulta Médica Guardada", "Consulta médica registrada correctamente.")


    def guardar_datos(self):
        id_consulta = self.entry_id_diagnostico_consulta.get()
        if not id_consulta:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un ID de consulta médica para guardar los datos.")
            return

        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('clinica_veterinaria.db')
            cursor = conn.cursor()

            # Insertar datos de la tabla Treeview en la tabla consulta_medica
            for row_id in self.tabla_consultas.get_children():
                row = self.tabla_consultas.item(row_id)['values']
                cursor.execute("INSERT INTO consulta_medica (id, nombres_paciente, diagnostico, fecha, hora) VALUES (?, ?, ?, ?, ?)", (id_consulta,) + tuple(row))

            conn.commit()
            messagebox.showinfo("Éxito", "Los datos han sido guardados exitosamente.")
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error de base de datos", f"Ha ocurrido un error: {e}")

root = tk.Tk()
app = Aplicacion(root)
root.mainloop()