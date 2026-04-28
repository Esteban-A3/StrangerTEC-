import tkinter as tk
from tkinter import Toplevel
import random
# STRANGERTEC — Ventana principal del juego

#Variables para las funciones
# Variables para capturar el morse del jugador 1
tiempo_presion    = 0       # cuando se presionó espacio
codigo_actual     = ""      # los 1s y 0s de la letra actual
lista_codigos     = []      # lista de letras en binario
id_letra          = None    # id del after para separar letra
id_palabra        = None    # id del after para fin de palabra
j1_listo          = False   # si jugador 1 ya terminó

#Funciones utilizadas
def elegir_palabra_al_azar():
    palabras = ["SOS", "HELP", "HEY", "HI", "HOLA", "BYE", "OK", "YES", "NO", "CODE"]
    return random.choice(palabras)

def binario_a_texto(codigos, indice):

    if indice == len(codigos):    #Se compara para poder terminar la funcion ya que si el indice es igual a su largo significa que ya leeyo el codigo
        return ""

    codigo = codigos[indice]     #Se crea una variable para que sea mas facil la valoracion

    if codigo == "10":
        letra = "A"
    elif codigo == "0111":
        letra = "B"
    elif codigo == "0101":
        letra = "C"
    elif codigo == "011":
        letra = "D"
    elif codigo == "1":
        letra = "E"
    elif codigo == "1101":
        letra = "F"
    elif codigo == "001":
        letra = "G"
    elif codigo == "1111":
        letra = "H"
    elif codigo == "11":
        letra = "I"
    elif codigo == "1000":
        letra = "J"
    elif codigo == "010":
        letra = "K"
    elif codigo == "1011":
        letra = "L"
    elif codigo == "00":
        letra = "M"
    elif codigo == "01":
        letra = "N"
    elif codigo == "000":
        letra = "O"
    elif codigo == "1001":
        letra = "P"
    elif codigo == "0010":
        letra = "Q"
    elif codigo == "101":
        letra = "R"
    elif codigo == "111":
        letra = "S"
    elif codigo == "0":
        letra = "T"
    elif codigo == "110":
        letra = "U"
    elif codigo == "1110":
        letra = "V"
    elif codigo == "100":
        letra = "W"
    elif codigo == "0110":
        letra = "X"
    elif codigo == "0100":
        letra = "Y"
    elif codigo == "0011":
        letra = "Z"
    elif codigo == "10000":
        letra = "1"
    elif codigo == "11000":
        letra = "2"
    elif codigo == "11100":
        letra = "3"
    elif codigo == "11110":
        letra = "4"
    elif codigo == "11111":
        letra = "5"
    elif codigo == "01111":
        letra = "6"
    elif codigo == "00111":
        letra = "7"
    elif codigo == "00011":
        letra = "8"
    elif codigo == "00001":
        letra = "9"
    elif codigo == "00000":
        letra = "0"
    elif codigo == "10101":
        letra = "+"
    elif codigo == "011110":
        letra = "-"
    else:
        letra = "?"         #Por si se ingresa una secuencia no Valorada
    return letra + binario_a_texto(codigos, indice + 1)   #Recursividad sinple una ves valorada la variable letra, se agrega y se vuelve a repetir la funcion


#Funcion para determinar que ha escrito el usuario que juega en la computadora 
def capturar_morse_j1(ventana, label_resultado, label_estado, palabra_sistema):
    global tiempo_presion, codigo_actual, lista_codigos
    global id_letra, id_palabra, j1_listo

    # Reiniciamos todas las variables a utilizar para evitar errores
    tiempo_presion = 0
    codigo_actual  = ""
    lista_codigos  = []
    j1_listo       = False

    def al_presionar(evento):
        global tiempo_presion, id_letra, id_palabra

        # Cancela los timers de separación porque el usuario sigue escribiendo
        if id_letra:
            ventana.after_cancel(id_letra)
        if id_palabra:
            ventana.after_cancel(id_palabra)

        # Guardamos el momento en que se presionó
        tiempo_presion = ventana.winfo_fpixels('1i')  # truco para obtener tiempo
        import time
        tiempo_presion = time.time()

    def al_soltar(evento):
        global tiempo_presion, codigo_actual, lista_codigos
        global id_letra, id_palabra
        import time
        
        

        # Calculamos cuánto duró la presión
        duracion = time.time() - tiempo_presion

        # Punto o raya según duración
        if duracion < 0.2:
            codigo_actual = codigo_actual + "1"   # punto
        else:
            codigo_actual = codigo_actual + "0"   # raya

        # Timer para separar letra (0.6s sin tocar)
        id_letra = ventana.after(600, separar_letra)

        # Timer para terminar palabra (1.4s sin tocar)
        id_palabra = ventana.after(1400, terminar_palabra)

        # Mostramos punto o raya según lo que escribió, lo que hace es escribir texto
        if duracion < 0.2:
            label_resultado.config(text=label_resultado.cget("text") + ".")
        else:
            label_resultado.config(text=label_resultado.cget("text") + "_")

    def separar_letra():
        global codigo_actual, lista_codigos
        if codigo_actual != "":
            lista_codigos.append(codigo_actual)
            codigo_actual = ""
             # Espacio visual para separar letras
            label_resultado.config(text=label_resultado.cget("text") + " ")

    def terminar_palabra():
        global lista_codigos, j1_listo

        # Por si quedó una letra sin guardar
        if codigo_actual != "":
            lista_codigos.append(codigo_actual)

        palabra_usuario = binario_a_texto(lista_codigos, 0)

        # Solo mostramos el mensaje de espera, sin revelar la palabra
        label_estado.config(text="Jugador 1 listo, esperando Jugador 2...")
        j1_listo = True
        ventana.unbind("<KeyPress-space>")
        ventana.unbind("<KeyRelease-space>")

        # Desvinculamos el espacio para que no siga capturando
        ventana.unbind("<space>")

    # Vinculamos presión y soltura de la barra espaciadora
    ventana.bind("<KeyPress-space>",   al_presionar)
    ventana.bind("<KeyRelease-space>", al_soltar)



# Colores de la ventana pricipal(inspirado en Stranger Things)
COLOR_FONDO      = "#000000"   # fondo negro
COLOR_ROJO       = "#cc0000"   # rojo principal
COLOR_ROJO_TENUE = "#660000"   # rojo oscuro para detalles
COLOR_BLANCO     = "#e8e8e8"   # texto principal
COLOR_GRIS       = "#888888"   # texto secundario

#Fuentes utilizadas
FUENTE_TITULO  = ("Courier", 42, "bold")
FUENTE_LABEL   = ("Courier", 11)
FUENTE_GRANDE  = ("Courier", 14)
FUENTE_BOTON   = ("Courier", 12, "bold")
FUENTE_PEQUENA = ("Courier", 9)

#Variable para guardar referencia del parpadeo
id_parpadeo = None

# PANTALLA 1 — Inicio (presiona cualquier tecla para pasar a la siguiente)
def mostrar_pantalla_inicio():
    # Limpia la ventana actual
    for widget in ventana.winfo_children(): #Define todos los elementos de la pantalla
        widget.destroy() #Los destruye

    # Título principal
    titulo = tk.Label(ventana,text="StrangerTEC",bg=COLOR_FONDO,fg=COLOR_ROJO,font=FUENTE_TITULO)
    titulo.pack(pady=(100, 5))

    # Subtítulo
    subtitulo = tk.Label(ventana, text="EL JUEGO DEL OTRO LADO",bg=COLOR_FONDO,fg=COLOR_ROJO_TENUE,font=("Courier", 10, "bold"))
    subtitulo.pack()

    # Mensaje parpadeante
    mensaje = tk.Label(ventana,text="— PRESIONA CUALQUIER TECLA —",bg=COLOR_FONDO,fg=COLOR_BLANCO,font=FUENTE_LABEL)
    mensaje.pack(pady=(60, 0))

    # Función para el efecto de parpadeo
    def parpadear(visible):
        global id_parpadeo   #Trae la variable que determina si el parpadeo existe
        if not mensaje.winfo_exists(): #Verifica si se elimino los objetos de esta pantalla, si es asi desactiva el parpadeo
            return 
        if visible: #Si el valor es verdad, se muestra texto
            mensaje.config(fg=COLOR_BLANCO)
        else: #Si es mentira no se muestra
            mensaje.config(fg=COLOR_FONDO)
        #Se llama a sí misma cada 600ms, e invierte el valor
        #Se guarda la posicion del parpadeo para poder cancelarlo después
        id_parpadeo = ventana.after(600, parpadear, not visible)
    parpadear(True)  # Posicion inicial

    # Cualquier tecla lleva a la pantalla de nombres
    ventana.bind("<Key>", lambda e: mostrar_pantalla_nombres())
    # Clic también funciona
    ventana.bind("<Button-1>", lambda e: mostrar_pantalla_nombres())

# PANTALLA 2 — Ingreso de nombres
def mostrar_pantalla_nombres():
    global id_parpadeo   #Se trae la variable parpadeo a la funcion
    # Cancelamos el parpadeo antes de destruir los widgets
    if id_parpadeo:
        ventana.after_cancel(id_parpadeo)
    
    #Se elimina la funcion que hacia que al presionar cualquier tecla te lleva a la siguiente ventana
    ventana.unbind("<Key>")   #Detecta cualquier tecla
    ventana.unbind("<Button-1>") #Detecta cualquier click

    for widget in ventana.winfo_children():   #Escaneo objetos de la anterior ventana
        widget.destroy() #Los destruye

    # Título de sección
    tk.Label(ventana,text="INGRESAR JUGADORES",bg=COLOR_FONDO,fg=COLOR_ROJO,font=("Courier", 18, "bold")).pack(pady=(80, 40))

    #Jugador 1
    tk.Label(ventana, text="JUGADOR 1", bg=COLOR_FONDO,fg=COLOR_GRIS, font=FUENTE_PEQUENA).pack()

    entrada_j1 = tk.Entry(ventana,bg="#0f0f0f",fg=COLOR_BLANCO,font=FUENTE_GRANDE,
        insertbackground=COLOR_ROJO,    # cursor rojo
        relief=tk.FLAT,   #Para el estilo del borde
        bd=0,highlightthickness=1, #Groesor y un tipo de groesor segundario cuando se selecciona el campo
        highlightcolor=COLOR_ROJO, #Color del campo si esta activo
        highlightbackground=COLOR_ROJO_TENUE, #Color del campo si esta inactivo
        width=20 #Espacio entre letras
    )
    entrada_j1.pack(pady=(0, 20))
    entrada_j1.focus()

    #Jugador 2, se usa la misma logica que el jugador 1
    tk.Label(ventana, text="JUGADOR 2", bg=COLOR_FONDO, fg=COLOR_GRIS, font=FUENTE_PEQUENA).pack()
    entrada_j2 = tk.Entry(ventana,bg="#0f0f0f",fg=COLOR_BLANCO,font=FUENTE_GRANDE,insertbackground=COLOR_ROJO,
        relief=tk.FLAT,bd=0,highlightthickness=1,highlightcolor=COLOR_ROJO,highlightbackground=COLOR_ROJO_TENUE,width=20
    )
    entrada_j2.pack(pady=(0, 20))

    #Texto del ensaje de error por si no se escribio nada
    label_error = tk.Label(ventana,text="",bg=COLOR_FONDO,fg=COLOR_ROJO,font=FUENTE_PEQUENA)
    label_error.pack()

    #Botón de continuar
    def al_continuar():
        nombre1 = entrada_j1.get().strip().upper()
        nombre2 = entrada_j2.get().strip().upper()

        # Validación básica por si no se escribio nada en los campos del nombre
        if nombre1 == "" or nombre2 == "":
            label_error.config(text="⚠  Ingresa ambos nombres") #Texto de error, llama al label definido para estos casos
            return

        # Si todo está bien, debe mostrar los nombres seleccionados
        mostrar_pantalla_reglas(nombre1, nombre2)
    
    #Boton de Continuar
    boton = tk.Button(ventana,text="CONTINUAR  →",bg=COLOR_FONDO,fg=COLOR_ROJO,font=FUENTE_BOTON,relief=tk.FLAT,bd=0, activebackground=COLOR_ROJO_TENUE,
        activeforeground=COLOR_BLANCO,cursor="hand2",command=al_continuar)
    boton.pack(pady=20)

#Pantalla de Regas y Juego: muestran las reglas y como jugar
def mostrar_pantalla_reglas(nombre1, nombre2):  
    for widget in ventana.winfo_children():  #Escanea y destruye
        widget.destroy() 

    # Título
    tk.Label(ventana,text="REGLAS DEL JUEGO",bg=COLOR_FONDO,fg=COLOR_ROJO,font=("Courier", 18, "bold")).pack(pady=(40, 30))
    # Cada regla como label separado
    reglas = [
        "Interpreta el mensaje en Morse y repítelo correctamente.",
        "",
        "•  Pulso corto  =  Punto  (.)",
        "•  Pulso largo  =  Raya  (-)",
        "•  Gana quien tenga más aciertos y mejor precisión.",
        "•  Respeta ritmo y espacios para evitar errores.",
        "•  Recuerda: Simbolo=0,2s, Letra=0,6s, Finalizar Palabra=1,4s.",
    ]

    for linea in reglas:tk.Label(ventana,text=linea, bg=COLOR_FONDO,fg=COLOR_BLANCO,
    font=("Courier", 11),justify="left").pack(anchor="w", padx=80) #Iteracion para crear texto para cada regla

    # Botón para Avanzar al lobby
    tk.Button(ventana,text="ENTENDIDO  →",bg=COLOR_FONDO,fg=COLOR_ROJO,font=FUENTE_BOTON,relief=tk.FLAT,bd=0,activebackground=COLOR_ROJO_TENUE,activeforeground=COLOR_BLANCO,cursor="hand2",
        command=lambda: mostrar_pantalla_lobby(nombre1, nombre2)
    ).pack(pady=40)

# PANTALLA 3 — Lobby en este se confirma los jugadores y se asigna la puntuacion inicial
def mostrar_pantalla_lobby(nombre1, nombre2):
    for widget in ventana.winfo_children(): #Designar objetos de la pantalla anterior
        widget.destroy() #Destruirlos

    #Esquina superior izquierda: jugadores y puntuación
    frame_jugadores = tk.Frame(ventana, bg=COLOR_FONDO) #Basico; fondo y color de la nueva pantalla
    frame_jugadores.place(x=20, y=15)

    #Jugador 1: Texto indicando jugador, Nombre y Puntaje inicial
    tk.Label(frame_jugadores, text="JUGADOR 1", bg=COLOR_FONDO,
             fg=COLOR_GRIS, font=FUENTE_PEQUENA).grid(row=0, column=0, sticky="w")

    tk.Label(frame_jugadores, text=nombre1, bg=COLOR_FONDO,
             fg=COLOR_BLANCO, font=("Courier", 13)).grid(row=1, column=0, sticky="w")

    tk.Label(frame_jugadores, text="PTS: 0", bg=COLOR_FONDO,
             fg=COLOR_ROJO, font=FUENTE_PEQUENA).grid(row=2, column=0, sticky="w", pady=(0, 10))

    #Jugador 2: Texto indicando jugador, Nombre y Puntaje inicial
    tk.Label(frame_jugadores, text="JUGADOR 2", bg=COLOR_FONDO,
             fg=COLOR_GRIS, font=FUENTE_PEQUENA).grid(row=3, column=0, sticky="w")

    tk.Label(frame_jugadores, text=nombre2, bg=COLOR_FONDO,
             fg=COLOR_BLANCO, font=("Courier", 13)).grid(row=4, column=0, sticky="w")

    tk.Label(frame_jugadores, text="PTS: 0", bg=COLOR_FONDO,
             fg=COLOR_ROJO, font=FUENTE_PEQUENA).grid(row=5, column=0, sticky="w")

    # Centro: mensaje y botón iniciar
    frame_centro = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_centro.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame_centro,text="LISTOS PARA EL DESAFÍO", bg=COLOR_FONDO,fg=COLOR_GRIS,font=("Courier", 10, "bold")).pack(pady=(0, 30))

    boton_iniciar = tk.Button(frame_centro,text="  INICIAR JUEGO  ",bg=COLOR_ROJO,fg=COLOR_BLANCO,font=FUENTE_BOTON,relief=tk.FLAT,bd=0,
        activebackground=COLOR_ROJO_TENUE,activeforeground=COLOR_BLANCO,cursor="hand2", command=lambda: mostrar_pantalla_juego(nombre1, nombre2))  # Aquí se conectará la lógica del juego
    boton_iniciar.pack()

#PANTALLA 4 - Inicio del juego
def mostrar_pantalla_juego(nombre1, nombre2, puntos1=0, puntos2=0):
    for widget in ventana.winfo_children():  #Escanear elementos de la pantalla anterior
        widget.destroy() #Eliminarlos

    # Elegimos palabra al azar con la funcion definida con una variable
    palabra = elegir_palabra_al_azar()

    #Se mantienen la puntuacion
    frame_jugadores = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_jugadores.place(x=20, y=15)

    tk.Label(frame_jugadores, text="JUGADOR 1", bg=COLOR_FONDO,
             fg=COLOR_GRIS, font=FUENTE_PEQUENA).grid(row=0, column=0, sticky="w")
    tk.Label(frame_jugadores, text=nombre1, bg=COLOR_FONDO,
             fg=COLOR_BLANCO, font=("Courier", 13)).grid(row=1, column=0, sticky="w")
    tk.Label(frame_jugadores, text=f"PTS: {puntos1}", bg=COLOR_FONDO,
             fg=COLOR_ROJO, font=FUENTE_PEQUENA).grid(row=2, column=0, sticky="w", pady=(0, 10))

    tk.Label(frame_jugadores, text="JUGADOR 2", bg=COLOR_FONDO,
             fg=COLOR_GRIS, font=FUENTE_PEQUENA).grid(row=3, column=0, sticky="w")
    tk.Label(frame_jugadores, text=nombre2, bg=COLOR_FONDO,
             fg=COLOR_BLANCO, font=("Courier", 13)).grid(row=4, column=0, sticky="w")
    tk.Label(frame_jugadores, text=f"PTS: {puntos2}", bg=COLOR_FONDO,
             fg=COLOR_ROJO, font=FUENTE_PEQUENA).grid(row=5, column=0, sticky="w")

    # Texto que indica la palabra que eligio el sistema 
    tk.Label(ventana,text="PALABRA A DESCIFRAR",bg=COLOR_FONDO,fg=COLOR_GRIS, font=FUENTE_PEQUENA).place(relx=0.5, rely=0.35, anchor="center")
    tk.Label(ventana, text=palabra, bg=COLOR_FONDO,fg=COLOR_ROJO,font=("Courier", 32, "bold")).place(relx=0.5, rely=0.45, anchor="center")

    # Mensaje que sale en la esquina inferiopr derecha donde ponen los controles
    frame_controles = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_controles.place(relx=0.98, rely=0.95, anchor="se")

    tk.Label(frame_controles, text="CONTROLES", bg=COLOR_FONDO,
             fg=COLOR_GRIS, font=FUENTE_PEQUENA).pack(anchor="e")
    tk.Label(frame_controles, text=f"{nombre1}  →  ESPACIO", bg=COLOR_FONDO,
             fg=COLOR_BLANCO, font=FUENTE_PEQUENA).pack(anchor="e")
    tk.Label(frame_controles, text=f"{nombre2}  →  BOTÓN", bg=COLOR_FONDO,
             fg=COLOR_BLANCO, font=FUENTE_PEQUENA).pack(anchor="e")
    
    
    # Label donde se ve el morse en tiempo real
    label_resultado = tk.Label(
        ventana,
        text="Morse: ",
        bg=COLOR_FONDO,
        fg=COLOR_BLANCO,
        font=FUENTE_LABEL
    )
    label_resultado.place(relx=0.5, rely=0.65, anchor="center")

    # Label de estado (jugador listo o no)
    label_estado = tk.Label(
        ventana,
        text="",
        bg=COLOR_FONDO,
        fg=COLOR_GRIS,
        font=FUENTE_PEQUENA
    )
    label_estado.place(relx=0.5, rely=0.75, anchor="center")

    # Arrancamos la captura del jugador 1
    capturar_morse_j1(ventana, label_resultado, label_estado, palabra)


# VENTANA PRINCIPAL
ventana = tk.Tk()
ventana.title("StrangerTEC")
ventana.geometry("800x600")
ventana.config(bg=COLOR_FONDO)
ventana.resizable(False, False)

# Empieza en la pantalla de inicio
mostrar_pantalla_inicio()

#Loop principal para mantener la pantalla abierta
ventana.mainloop()