import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker
#FIREBASE
import firebase_admin
from firebase_admin import credentials, db
#CARGAR MODELO ENTRENADO RANDOM FOREST
import joblib

#llamamos al modelo entrenado
loaded_model = joblib.load('random_forest_model2000Data2ETQ.pkl')

# URL de Firebase
firebase_url = 'https://minstationmeteo-default-rtdb.firebaseio.com/datos.json'

# Inicializa la aplicación de Firebase con las credenciales y la URL de la base de datos
cred = credentials.Certificate('D:minstationmeteo-firebase-adminsdk-93gzs-fd2a7ac1fa.json')

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {'databaseURL': firebase_url})

#VARIABLES INICIALIZAR
# Inicializar las listas globales fuera de la función
temperatura_valores = []
humedad_valores = []
lluvia_valores = []
presion_valores = []
time = 0 #Variable para guardar los segundos 
time_valores = []
prediccion = []
prediccion_valores = []
probabilidad_lluvia = 0

# Crear la ventana principal
root = tk.Tk()
root.title("Gráficas en Tkinter")
root.geometry("690x740")
# Deshabilitar el redimensionamiento
root.resizable(False, False)

# Función para actualizar las gráficas en los frames
def actualizar_graficas():
    global humedad_valores, lluvia_valores, temperatura_valores, time_valores, presion_valores, prediccion_valores
    line1.set_data(time_valores, temperatura_valores)
    ax1.relim()
    ax1.autoscale_view()
    canvas1.draw()

    line2.set_data(time_valores, humedad_valores)
    ax2.relim()
    ax2.autoscale_view()
    canvas2.draw()

    line3.set_data(time_valores, presion_valores)
    ax3.relim()
    ax3.autoscale_view()
    canvas3.draw()

    line4.set_data(time_valores, lluvia_valores)
    line5.set_data(time_valores, prediccion_valores)  
    ax4.relim()
    ax4.autoscale_view()
    canvas4.draw()

def predecir():
    global prediccion, prediccion_valores,temperatura,humedad,presion, probabilidad_lluvia
    prediccion = loaded_model.predict([[temperatura,humedad,presion]])
    prediccion_valores.append(prediccion[0])
    print(prediccion_valores)
    # Obtener probabilidades
    probabilities = loaded_model.predict_proba([[temperatura,humedad,presion]])
    print(probabilities)
    #Solo obtener la probabilidad de la clase 1
    prob_class_1 = probabilities[:, 1]
    probabilidad_lluvia = prob_class_1[0]
    
# Función para actualizar el Label usando config()
def actualizar_label():
    global probabilidad_lluvia
    label_probabilidad_valor.config(text=probabilidad_lluvia)

# Función para guardar las gráficas
def guardar_graficas():
    fig1.savefig('grafica_temperatura.png')
    fig2.savefig('grafica_humedad.png')
    fig3.savefig('grafica_presion.png')
    fig4.savefig('grafica_lluvia.png')

#FUNCION OBTENER DATOS
def obtener_datosFirebase():
    
    global temperatura, presion, humedad, lluvia, temperatura_valores, presion_valores, humedad_valores, lluvia_valores, time, time_valores
    
    ref = db.reference('/datos')
    # Obtener datos de Firebase
    data = ref.get()
    
    # Asignar los valores a variables diferentes
    humedad = data['Humedad (0-100)% RH']
    presion = round(data['Presion Atmosferica Pa']/1000,2)
    lluvia = data['Rain']
    temperatura = data['Temperatura C']
    
    temperatura_valores.append(temperatura)
    humedad_valores.append(humedad)
    presion_valores.append(presion)
    lluvia_valores.append(lluvia)
    time_valores.append(time)
    
    
#FUNCIONES PARA QUE SE EJECUTE EN CICLO, DEPENDIENDO DEL TIEMPO QUE SE MANTENGA PRESIONADO
def on_button_press(event):
    global running
    running = True
    repeat_action()

def on_button_release(event):
    global running, temperatura_valores,presion_valores,humedad_valores,lluvia_valores,time,time_valores
    running = False

def repeat_action():
    global time
    if running:
        obtener_datosFirebase()
        time = round(time+0.5,2)
        predecir()
        actualizar_label()
        # Aquí puedes poner la acción que quieras que se repita
        root.after(400, repeat_action)  # Llama a la función cada 100 ms
        actualizar_graficas()
        
    
#Botones
boton_adquirir = tk.Button(root, text="Adquirir")#, command=guardar_datos)
boton_adquirir.grid(row=2, column=0, rowspan=2 , pady=10) 
# Vincula los eventos de presionar y liberar el botón
boton_adquirir.bind("<ButtonPress>", on_button_press)
boton_adquirir.bind("<ButtonRelease>", on_button_release)

#LABELS TEXTOS
label_probabilidad = tk.Label(root, text = "Probabilidad de que llueva")
label_probabilidad.grid(row=2, column=1 , pady=1) 

label_probabilidad_valor = tk.Label(root, text = "N/A")
label_probabilidad_valor.grid(row=3, column=1 , pady=1) 

# Crear 4 frames para las gráficas
frame1 = ttk.Frame(root, width=100, height=100)
frame1.grid(row=0, column=0, padx=5, pady=5)

frame2 = ttk.Frame(root, width=100, height=100)
frame2.grid(row=0, column=1, padx=5, pady=5)

frame3 = ttk.Frame(root, width=100, height=100)
frame3.grid(row=1, column=0, padx=5, pady=5)

frame4 = ttk.Frame(root, width=100, height=100)
frame4.grid(row=1, column=1, padx=5, pady=5)

# Crear las figuras y los ejes para las gráficas
#Frame 1
fig1, ax1 = plt.subplots(figsize=(5, 5), dpi=65)
ax1.set_title("Temperatura")
canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
canvas1.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)

#Frame 2
fig2, ax2 = plt.subplots(figsize=(5, 5), dpi=65)
ax2.set_title("Humedad Relativa")
canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
canvas2.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)

#Frame 3
fig3, ax3 = plt.subplots(figsize=(5, 5), dpi=65)
ax3.set_title("Presión Atmosférica")
ax3.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))  # Formatear eje Y con 2 decimales
canvas3 = FigureCanvasTkAgg(fig3, master=frame3)
canvas3.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)

#Frame 4
fig4, ax4 = plt.subplots(figsize=(6, 6), dpi=50)
ax4.set_title("Lluvia")
canvas4 = FigureCanvasTkAgg(fig4, master=frame4)
canvas4.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)

# Inicializar las líneas de las gráficas
line1, = ax1.plot([], [], label="Temperatura", color = "red")
line2, = ax2.plot([], [], label="Humedad")
line3, = ax3.plot([], [], label="Presión" , color = "black")
line4, = ax4.plot([], [], label="Lluvia" , color = "cyan")
line5, = ax4.plot([], [], label="Predicción", linestyle='--', color = 'green')

# Agregar leyendas a las gráficas
ax1.legend()
ax2.legend()
ax3.legend()
ax4.legend()

# Vincular la función de guardar gráficas al evento de cierre de la ventana
root.protocol("WM_DELETE_WINDOW", lambda: [guardar_graficas(), root.destroy()])


# Iniciar el bucle principal de la interfaz
root.mainloop()