import tkinter as tk
from tkinter import messagebox
import os
from tkinter import ttk
from PIL import ImageGrab
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import locale


class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Historial Médico")
        self.conexion_bd = sqlite3.connect("clinica_veterinaria.db")
        self.cursor_bd = self.conexion_bd.cursor()

        # Crear los atributos de instancia
        self.medicamentos_var = tk.StringVar(self.root)
        self.cantidad_medicamentos_var = tk.StringVar(self.root)

        # Crear el Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, columnspan=5, rowspan=8, padx=10, pady=10)

        # Sección de la interfaz gráfica para el historial médico
        self.mostrar_historial_medico()
        
        # Establecer configuración regional para formato de moneda
        locale.setlocale(locale.LC_ALL, '')

        # Botones
        self.guardar_button = tk.Button(self.root, text="Guardar Consulta", command=self.guardar_consulta)
        self.guardar_button.grid(row=8, column=4, padx=10, pady=10)

        self.imprimir_button = tk.Button(self.root, text="Imprimir", command=self.imprimir_pantalla)
        self.imprimir_button.grid(row=3, column=4, padx=10, pady=10)

    def mostrar_historial_medico(self):
        # Título
        titulo_label = tk.Label(self.root, text="HISTORIAL MÉDICO", font=("Helvetica", 16, "bold"), bg="#ADD8E6")
        titulo_label.grid(row=0, column=1, columnspan=4, sticky="w", padx=10, pady=10)
        
        # Paciente
        paciente_label = tk.Label(self.root, text="Paciente", bg="#ADD8E6")
        paciente_label.grid(row=1, column=0, sticky="w", padx=10)
        
        # Obtener nombres de pacientes de la base de datos
        pacientes = self.obtener_nombres_pacientes()
        
        # Lista desplegable para los pacientes
        paciente_var = tk.StringVar(self.root)
        paciente_var.set("Seleccione un paciente")  # Valor por defecto
        if not pacientes:
            pacientes = ["No hay pacientes disponibles"]  # Handle empty list case
        paciente_menu = tk.OptionMenu(self.root, paciente_var, *pacientes)
        paciente_menu.grid(row=2, column=0, sticky="w", padx=10)

        # Fecha
        fecha_label = tk.Label(self.root, text="Fecha", bg="#ADD8E6")
        fecha_label.grid(row=1, column=1, sticky="w", padx=10)
        fecha_entry = tk.Entry(self.root)
        fecha_entry.grid(row=2, column=1, sticky="w", padx=10)

        # Etiqueta "Doctor"
        self.doctor_label = tk.Label(self.root, text="Doctor", bg="#ADD8E6")
        self.doctor_label.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        # Lista de opciones para el Doctor obtenida de la base de datos
        doctor_var = tk.StringVar(self.root)
        doctor_var.set("Seleccione un doctor")  # Valor por defecto
        doctores = self.obtener_nombres_doctores()
        doctor_menu = tk.OptionMenu(self.root, doctor_var, *doctores)
        doctor_menu.grid(row=2, column=2, sticky="w", padx=10, pady=5)

        # Hora
        hora_label = tk.Label(self.root, text="Hora", bg="#ADD8E6")
        hora_label.grid(row=0, column=3, sticky="w", padx=10, pady=5)
        hora_entry = tk.Entry(self.root)
        hora_entry.grid(row=0, column=4, sticky="w", padx=10, pady=5)

        # Diagnóstico de Ingreso
        diagnostico_ingreso_label = tk.Label(self.root, text="Diagnóstico de Ingreso", bg="#ADD8E6")
        diagnostico_ingreso_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        diagnostico_ingreso_text = tk.Text(self.root, height=3, width=60)
        diagnostico_ingreso_text.grid(row=4, column=0, columnspan=4, sticky="w", padx=10, pady=5)

        # Tratamiento
        tratamiento_label = tk.Label(self.root, text="Tratamiento", bg="#ADD8E6")
        tratamiento_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)
        tratamiento_text = tk.Text(self.root, height=3, width=60)
        tratamiento_text.grid(row=6, column=0, columnspan=4, sticky="w", padx=10, pady=5)

        # Lista desplegable para Medicamentos
        self.medicamentos_var.set("Seleccione un medicamento")  # Valor por defecto

        # Obtener nombres de medicamentos de la base de datos
        nombres_medicamentos = self.obtener_nombres_medicamentos()

        # Si hay medicamentos en la base de datos, los agregamos a la lista desplegable
        if nombres_medicamentos:
            medicamentos_menu = tk.OptionMenu(self.root, self.medicamentos_var, *nombres_medicamentos)
        else:
            medicamentos_menu = tk.OptionMenu(self.root, self.medicamentos_var, "No hay medicamentos disponibles")
         
        medicamentos_menu.grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Actualizar existencias cuando se seleccione un medicamento
        self.medicamentos_var.trace('w', self.actualizar_existencias)

        # Entrada para la Cantidad de Medicamentos (solo números)
        self.cantidad_medicamentos_entry = tk.Entry(self.root, textvariable=self.cantidad_medicamentos_var, validate='key', validatecommand=(self.root.register(self.validar_numeros), '%P'))
        self.cantidad_medicamentos_entry.grid(row=8, column=2, columnspan=2, sticky="w", padx=10, pady=5)

        # Tabla de Medicamentos
        self.tabla_medicamentos = ttk.Treeview(self.root, columns=("medicamento", "cantidad", "precio"), show="headings")
        self.tabla_medicamentos.heading("medicamento", text="Nombre del Medicamento")
        self.tabla_medicamentos.heading("cantidad", text="Cantidad de Medicamento")
        self.tabla_medicamentos.heading("precio", text="Precio del Medicamento")
        self.tabla_medicamentos.grid(row=9, column=0, columnspan=4, sticky="w", padx=10, pady=10)
    
    def validar_numeros(self, value_if_allowed):
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        else:
            return False

    def obtener_nombres_pacientes(self):
        # Consulta para obtener nombres de pacientes
        self.cursor_bd.execute("SELECT nombre FROM pacientes")
        pacientes = self.cursor_bd.fetchall()
        nombres_pacientes = [paciente[0] for paciente in pacientes]
        return nombres_pacientes

    def obtener_nombres_doctores(self):
        # Consulta para obtener nombres de doctores
        self.cursor_bd.execute("SELECT nombres FROM medicos")
        doctores = self.cursor_bd.fetchall()
        nombres_doctores = [doctor[0] for doctor in doctores]
        return nombres_doctores

    def cargar_medicos(self):
        # Consultar la base de datos y cargar los nombres de los médicos
        self.cursor_bd.execute("SELECT nombres FROM medicos")
        medicos = self.cursor_bd.fetchall()
        nombres = [medico[0] for medico in medicos]

        # Asignar los nombres de los médicos al Combobox
        self.medicos_combo['values'] = nombres

    def obtener_nombres_medicamentos(self):
        # Consulta para obtener nombres de medicamentos
        self.cursor_bd.execute("SELECT nombre FROM medicamentos")
        medicamentos = self.cursor_bd.fetchall()
        nombres_medicamentos = [medicamento[0] for medicamento in medicamentos]
        return nombres_medicamentos

    def obtener_existencias_medicamentos(self):
        # Obtener el medicamento seleccionado en la lista desplegable
        medicamento_seleccionado = self.medicamentos_var.get()

        if medicamento_seleccionado == "Seleccione un medicamento":
            return 0

        # Consulta para obtener las existencias del medicamento seleccionado
        self.cursor_bd.execute("SELECT existencias FROM medicamentos WHERE nombre=?", (medicamento_seleccionado,))
        existencias = self.cursor_bd.fetchone()

        if existencias:
            return existencias[0]
        else:
            return 0

    def actualizar_existencias(self, *args):
        existencias = self.obtener_existencias_medicamentos()
        if existencias == 0:
            messagebox.showwarning("Advertencia", "No hay existencias disponibles para este medicamento.")
        else:
            self.cantidad_medicamentos_entry.delete(0, tk.END)
            self.cantidad_medicamentos_entry.insert(0, str(existencias))

    def guardar_consulta(self):
        # Validación de la cantidad de medicamentos
        cantidad = self.cantidad_medicamentos_var.get()
        medicamento = self.medicamentos_var.get()
        if not cantidad.isdigit():
            messagebox.showerror("Error", "La cantidad de medicamentos debe ser un número")
        elif medicamento == "Seleccione un medicamento":
            messagebox.showerror("Error", "Debe seleccionar un medicamento")
        else:
            cantidad = int(cantidad)
            existencias = self.obtener_existencias_medicamentos()
            if cantidad > existencias:
                messagebox.showerror("Error", "La cantidad de medicamentos excede las existencias disponibles.")
            elif cantidad == 0:
                messagebox.showerror("Error", "La cantidad de medicamentos no puede ser 0. Actualice las existencias.")
            else:
                # Obtener el precio del medicamento desde la base de datos
                self.cursor_bd.execute("SELECT precio FROM medicamentos WHERE nombre=?", (medicamento,))
                precio_unitario = self.cursor_bd.fetchone()[0]

                # Calcular el precio total
                precio_total = cantidad * precio_unitario

                # Formatear precio_total como moneda
                precio_total_moneda = locale.currency(precio_total, grouping=True)

                # Añadir la entrada a la tabla de medicamentos
                self.tabla_medicamentos.insert("", "end", values=(medicamento, cantidad, precio_total_moneda))

                messagebox.showinfo("Éxito", "Consulta guardada correctamente.")

    def imprimir_pantalla(self):
    # Capturar la pantalla de la ventana principal
      x = self.root.winfo_rootx()
      y = self.root.winfo_rooty()
      w = self.root.winfo_width()
      h = self.root.winfo_height()
      image = ImageGrab.grab((x, y, x + w, y + h))
    
      # Guardar la imagen como PNG
      image.save("pantalla.png")

      # Crear un PDF y agregar la imagen
      pdf = canvas.Canvas("pantalla.pdf", pagesize=letter)
      pdf.drawImage("pantalla.png", 0, 0, width=letter[0], height=letter[1])
      pdf.save()
 
      # Abrir el archivo PDF generado
      os.system("start pantalla.pdf")  # Para sistemas Windows
      # os.system("xdg-open pantalla.pdf")  # Para sistemas Linux
     # os.system("open pantalla.pdf")  # Para sistemas macOS

# Crear la ventana principal de la aplicación
root = tk.Tk()
root.configure(bg="#ADD8E6")  # Establecer el color de fondo de la ventana principal
app = Aplicacion(root)
root.mainloop()
