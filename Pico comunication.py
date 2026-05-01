import tkinter as tk
from tkinter import Toplevel
import random
import time
import serial
import serial.tools.list_ports
import threading
# ─────────────────────────────────────────────
# STRANGERTEC — Ventana principal del juego
# ─────────────────────────────────────────────

#Variables para las funciones, son globales

#Variable de la palabra al azar elegida por el sistema
palabra_sistema = ""   #Palabra que el sistema eligio empieza en nada

#Variables de los nombres
nombre1 = ""
nombre2 = ""

#Variables del marcador
puntos1  = 0    #Score jugador 1
puntos2  = 0    #Score jugador 1
ronda_actual = 1     #Ronda actual
rondas_max   = 3     #Rondas maximas

# Estado de jugadores por ronda
j1_termino = False   #Variable para saber si el jugador 1 termino
j2_termino = False   #Variable para saber si el jugador 1 termino
palabra_j1 = ""      #Palabra escrita por el jugador 1
palabra_j2 = ""      #Palabra escrita por el jugador 2
label_estado    = None    #Texto que dice si un jugador termino, empiza sin nada
label_resultado = None    #Texto que dice lo que el jugador uno escribe, empiza sin nada

# Variables para capturar el morse del jugador 1
tiempo_presion    = 0       #cuando se presionó espacio, empieza en cero
codigo_actual     = ""      #Es lo que va escribiendo el usuario, empiza vacio
lista_codigos     = []      # lista de letras en binario
id_letra          = None    #Identificar si se escribio una letra
id_palabra        = None    #Identificar el fin de la palabra
j1_listo          = False   #Variable para saber si el jugador 1 termino


#Funciones utilizadas
def elegir_palabra_al_azar():
    palabras = ["SOS", "HELP", "HEY", "HI", "HOLA", "BYE", "OK", "YES", "NO", "CODE"]
    return random.choice(palabras)

#Funcion que traduce el morse expresado como binario a texto
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

#Funcion que cuenta los errores
def contar_errores(palabra_original, palabra_usuario, indice):
    # caso base: si el indice llega al final
    if indice == len(palabra_original) or indice == len(palabra_usuario):
        # Esta resta es para comprobar si la palabra escrita por el usuario es del mismo tamaño, si lo es pone 0, sino agrega la diferencia como un errores
        return abs(len(palabra_original) - len(palabra_usuario))
    
    if palabra_original[indice] != palabra_usuario[indice]:  #Si en la posicion determinada por el indice es diferente
        return 1 + contar_errores(palabra_original, palabra_usuario, indice + 1)
    else:   #Recursividad simple, suma uno al indice para poder escanear las posiciones de las palabras
        return contar_errores(palabra_original, palabra_usuario, indice + 1)

#Función que obtiene el porcentaje de errores
def calcular_porcentaje(palabra_original, errores):
    largo = len(palabra_original)   #Calcula el largo
    aciertos = largo - errores      #Resta el largo con los errores encontrados con la otra funcion
    aciertos = max(0, aciertos) #si es negativo lo fuerza a 0 
    porcentaje = (aciertos * 100) / largo  #Realiza aritmetica basica para obtener el porcentaje
    return porcentaje

#Funcion que evalua si los dos jugadores terminaron
def evaluar_jugadores_listos(nombre1, nombre2):
    global j1_termino, j2_termino

    if j1_termino and j2_termino: # Si los dos terminaron, vamos a resultados 
        mostrar_pantalla_resultados(nombre1, nombre2, palabra_sistema, palabra_j1, palabra_j2)
    elif j1_termino and not j2_termino:
        label_estado.config(text=f"{nombre1} listo, esperando a {nombre2}...")
    elif j2_termino and not j1_termino:
        label_estado.config(text=f"{nombre2} listo, esperando a {nombre1}...")
    #Se modifico hizo variable gloval label_estado

#Funcion que convierte la palabra a morse, usando binario
def palabra_a_binario(palabra):
    MORSE_BINARIO = {
        "A": "10",    "B": "0111",  "C": "0101",  "D": "011",
        "E": "1",     "F": "1101",  "G": "001",   "H": "1111",
        "I": "11",    "J": "1000",  "K": "010",   "L": "1011",
        "M": "00",    "N": "01",    "O": "000",   "P": "1001",
        "Q": "0010",  "R": "101",   "S": "111",   "T": "0",
        "U": "110",   "V": "1110",  "W": "100",   "X": "0110",
        "Y": "0100",  "Z": "0011",
        "1": "10000", "2": "11000", "3": "11100", "4": "11110",
        "5": "11111", "6": "01111", "7": "00111", "8": "00011",
        "9": "00001", "0": "00000", "+": "10101", "-": "011110",
    }
    resultado = []
    for letra in palabra:
        if letra in MORSE_BINARIO:
            resultado.append(MORSE_BINARIO[letra])  #Une la palabra en una lista de binarios
    # letras separadas por | 
    return "|".join(resultado)

#Funcion que envia la palabra a la maqueta tiene dos partes:


#Primera encuentra si la pico esta conectada a un puerto
def encontrar_puerto_pico():
    return "COM7"
def encontrar_puerto_pico_2():
    # Busca automaticamente el puerto de la Pico
    puertos = serial.tools.list_ports.comports()

    for puerto in puertos: #Busca en todos los puertos
        if "USB Serial" in puerto.description or "Pico" in puerto.description:  #Intenta buscar una dispositivo
            return puerto.device
    return None  #Si no encontro nada devuelve literalmente nada

#Segunda envia la palabra a la pico dependiendo del modo de juego
def enviar_a_pico(palabra):
    # Prepara el mensaje según el modo de salida
    if modo_salida.get() == "luz":
        mensaje = palabra                    # texto plano
    else:
        mensaje = palabra_a_binario(palabra) # binario con | 

    #Si tiene puesto que se comuniquen con cable(predeterminado);
    if modo_comunicacion.get() == "cable":
        # Envío por cable serial
        puerto = encontrar_puerto_pico()
        if puerto is None:
            print("No se encontró la Pico")
            return None
        try:
            pico = serial.Serial(puerto, 115200, timeout=10)  #envia mensaje a la pico con la palabra codificada
            pico.write((mensaje + "\n").encode()) #Reescribe la variable escrita en la pico
            print("Enviado a Pico:", mensaje) #Solo se ve en la terminal es para confirmar
            # Espera respuesta del jugador 2
            respuesta = pico.readline().decode().strip()   #Una vez tiene la respuesta, la lee, decodifica y la escribe
            pico.close()   #Cierra la coneccion
            print("Respuesta Pico:", respuesta)  #Solo se vee en la pc es para saber que llego correctamente
            return respuesta 
        except Exception as e:
            print("Error serial:", e)  #Si para algo avisa por medio de la terminal
            return None
    else:
        # WiFi — se implementará después
        print("WiFi pendiente")
        return None

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
        if id_letra:       #contador para saber si han pasado los 0,6s que tiene que esperar para finalizar la letra
            ventana.after_cancel(id_letra)  #Reinicia el contador
        if id_palabra:     #contador para saber si han a pasado los 1,4ss que tiene que esperar para finalizar la palabra
            ventana.after_cancel(id_palabra) #Reinicia el contador

        # Guardamos el momento en que se presionó
        tiempo_presion = time.time() #Se inicia el tiempo

    def al_soltar(evento):
        global tiempo_presion, codigo_actual, lista_codigos
        global id_letra, id_palabra
        
        # Calculamos cuánto duró la presión, con el tiempo actual-tiempo de inicio
        duracion = time.time() - tiempo_presion

        #Se va calculando la letra, recordar que el morse esta traducido en binario
        if duracion < 0.2: #Tiempo para que termine el simbolo(punto o espacio)
            codigo_actual = codigo_actual + "1"   # agregar 1
        else:
            codigo_actual = codigo_actual + "0"   # agregar 0

        # Timer para separar letra (0.6s sin tocar)
        id_letra = ventana.after(600, separar_letra)

        # Timer para terminar palabra (1.4s sin tocar)
        id_palabra = ventana.after(1400, terminar_palabra)

        # Mostramos punto o raya según lo que escribió, lo que hace es escribir texto
        if duracion < 0.2:   #Indica que escribio simbolo(punto o espacio)
            label_resultado.config(text=label_resultado.cget("text") + ".")   #Texto inficando punto en tiempo real
        else:
            label_resultado.config(text=label_resultado.cget("text") + "_")    #Texto indicando espacio en tiempo real

    def separar_letra():
        global codigo_actual, lista_codigos
        if codigo_actual != "":
            lista_codigos.append(codigo_actual)   #Se une las letras en una lista, ya que la funcion de morse a texto solo lee listas tipo ["1111","0101"]
            codigo_actual = ""
             # Espacio visual para separar letras
            label_resultado.config(text=label_resultado.cget("text") + " ")    #Texto indicando espacio en tiempo real

    def terminar_palabra():
        global lista_codigos, j1_termino, palabra_j1

        # Por si quedó una letra sin guardar
        if codigo_actual != "":
            lista_codigos.append(codigo_actual)  #Se une las letras en una lista, ya que la funcion de morse a texto solo lee listas tipo ["1111","0101"]

        palabra_j1 =  binario_a_texto(lista_codigos, 0)  #Palabra final del usuario evaluada en texto
        j1_termino=True #Envia mensaje diciendo que ya termino el jugador 1

        #Se quitan los eventos donde se registra el espacio
        ventana.unbind("<KeyPress-space>")     
        ventana.unbind("<KeyRelease-space>")

        evaluar_jugadores_listos(nombre1,nombre2) # Se llama a la funcion para cominicar que ya termino

    # Vinculamos los eventos de presión y soltura de la barra espaciadora al iniciar la funcion
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
        global nombre1,nombre2  #Se traen los nombres para modificarlos globalmente
        nombre1 = entrada_j1.get().strip().upper()  #Esto es configuracion de lectura: hace lee lo que se puso, elimina espacios y hace todo en mayuscula
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
    
    #Boton para abrir los ajustes del juego
    tk.Button(ventana,text="⚙ AJUSTES",bg=COLOR_FONDO,fg=COLOR_GRIS,font=FUENTE_PEQUENA,relief=tk.FLAT, bd=0,cursor="hand2",
        command=lambda: mostrar_pantalla_ajustes(mostrar_pantalla_nombres)).pack()#Esto es para exportar toda la pantalla y poder eliminarla

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
        "•  Pulso largo  =  Raya  (_)",
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
        activebackground=COLOR_ROJO_TENUE,activeforeground=COLOR_BLANCO,cursor="hand2", command=lambda: mostrar_pantalla_juego(nombre1, nombre2, puntos1, puntos2))  # Aquí se conectará la lógica del juego
    boton_iniciar.pack()

#PANTALLA 4 - Juego
def mostrar_pantalla_juego(nombre1, nombre2, puntos1, puntos2):
    for widget in ventana.winfo_children():  #Escanear elementos de la pantalla anterior
        widget.destroy() #Eliminarlos

    global palabra_sistema # Se importa la variable de palabra del sistema
    #Se modifica la variable
    palabra_sistema = elegir_palabra_al_azar()

    global label_estado, label_resultado#Se importa el texto de estado de los jugadores y lo que escribe el jugador 1 en la pantalla
    #Texto que indiga si un jugador termino
    label_estado = tk.Label(ventana,text="",bg=COLOR_FONDO,fg=COLOR_GRIS,font=FUENTE_PEQUENA)
    label_estado.place(relx=0.5, rely=0.80, anchor="center")

    #Texto de lo que escribe el jugador en la pantalla
    label_resultado = tk.Label(ventana,text="Morse: ",bg=COLOR_FONDO,fg=COLOR_BLANCO,font=FUENTE_LABEL)
    label_resultado.place(relx=0.5, rely=0.65, anchor="center")


    global j1_termino, j2_termino, palabra_j1, palabra_j2   #Se importa las variables de los estados del jugador y sus palabras
    #Se reinician los estados globales para volver a evaluar en la siguiente ronda
    j1_termino = False
    j2_termino = False
    palabra_j1 = ""
    palabra_j2 = ""
    
    #Inicia la funcion que activa el reconocimiento de la palabra escrita por el jugador 1
    capturar_morse_j1(ventana, label_resultado, label_estado, palabra_sistema)
    
    #Funcion para evaluar al jugador 2 el que usa la maqueta
    def hilo_pico():
        global palabra_j2, j2_termino
        respuesta = enviar_a_pico(palabra_sistema) #Ejecuta la funcion para enviar el mensaje a la pico
        if respuesta:
            # La respuesta viene como "111,000,111" separado por comas
            lista_j2 = respuesta.split(",") #Agrega los parentesis necesarios para que la funcion lo reconosca y la convierte en lista
            palabra_j2 = binario_a_texto(lista_j2, 0) #Lo envia a la funcion
        else:
            palabra_j2 = "?"  #Por si se envio algo que no se puede evaluar
        j2_termino = True  #Si ya regreso la palabra indica que ya termino
        evaluar_jugadores_listos(nombre1, nombre2)  #Envia a evaluar para ver si ya termino

    # Corremos en un hilo para no bloquear la interfaz ya que al esperar la respuesta no corre lo demas
    hilo = threading.Thread(target=hilo_pico)  #Define la funcion de evaluar al jugador 2 como hilo segundario
    hilo.daemon = True  #Si se ciera el pricipal este tambien se cierra
    hilo.start() #Se inicia

    #Se mantienen la puntuacion
    frame_jugadores = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_jugadores.place(x=20, y=15)

    #Texto de la puntuacion de los jugadores
    tk.Label(frame_jugadores, text="JUGADOR 1", bg=COLOR_FONDO,fg=COLOR_GRIS, font=FUENTE_PEQUENA).grid(row=0, column=0, sticky="w")
    tk.Label(frame_jugadores, text=nombre1, bg=COLOR_FONDO,fg=COLOR_BLANCO, font=("Courier", 13)).grid(row=1, column=0, sticky="w")
    tk.Label(frame_jugadores, text=f"PTS: {puntos1}", bg=COLOR_FONDO,fg=COLOR_ROJO, font=FUENTE_PEQUENA).grid(row=2, column=0, sticky="w", pady=(0, 10))

    tk.Label(frame_jugadores, text="JUGADOR 2", bg=COLOR_FONDO, fg=COLOR_GRIS, font=FUENTE_PEQUENA).grid(row=3, column=0, sticky="w")
    tk.Label(frame_jugadores, text=nombre2, bg=COLOR_FONDO, fg=COLOR_BLANCO, font=("Courier", 13)).grid(row=4, column=0, sticky="w")
    tk.Label(frame_jugadores, text=f"PTS: {puntos2}", bg=COLOR_FONDO,fg=COLOR_ROJO, font=FUENTE_PEQUENA).grid(row=5, column=0, sticky="w")

    if mostrar_palabra.get():  #Si se activo el ajuste para mostrar la palabra del sistema
        #Texto que indica la palabra que eligio el sistema 
        tk.Label(ventana,text="PALABRA A DESCIFRAR",bg=COLOR_FONDO,fg=COLOR_GRIS, font=FUENTE_PEQUENA).place(relx=0.5, rely=0.35, anchor="center")
        tk.Label(ventana, text=palabra_sistema, bg=COLOR_FONDO,fg=COLOR_ROJO,font=("Courier", 32, "bold")).place(relx=0.5, rely=0.45, anchor="center")

    #Mensaje que sale en la esquina inferior derecha donde ponen los controles
    frame_controles = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_controles.place(relx=0.98, rely=0.95, anchor="se")

    tk.Label(frame_controles, text="CONTROLES", bg=COLOR_FONDO,fg=COLOR_GRIS, font=FUENTE_PEQUENA).pack(anchor="e")
    tk.Label(frame_controles, text=f"{nombre1}  →  ESPACIO", bg=COLOR_FONDO, fg=COLOR_BLANCO, font=FUENTE_PEQUENA).pack(anchor="e")
    tk.Label(frame_controles, text=f"{nombre2}  →  BOTÓN", bg=COLOR_FONDO,fg=COLOR_BLANCO, font=FUENTE_PEQUENA).pack(anchor="e")

    # Texto de estado (jugador listo o no)
    label_estado = tk.Label(ventana,text="",bg=COLOR_FONDO,fg=COLOR_GRIS,font=FUENTE_PEQUENA)
    label_estado.place(relx=0.5, rely=0.75, anchor="center")

#PANTALLA 5 - Calcular y mover score
def mostrar_pantalla_resultados(nombre1, nombre2, palabra_sistema, palabra_j1, palabra_j2):
    global puntos1, puntos2, ronda_actual    #Se importan las variables del score
 
    for widget in ventana.winfo_children():  #Escanear objetos de la pantalla anterior
        widget.destroy()  #Eliminar

    # Calculamos errores y porcentaje de cada jugador
    errores1     = contar_errores(palabra_sistema, palabra_j1, 0)
    errores2     = contar_errores(palabra_sistema, palabra_j2, 0)
    porcentaje1  = calcular_porcentaje(palabra_sistema, errores1)
    porcentaje2  = calcular_porcentaje(palabra_sistema, errores2)

    # Determinamos ganador de la ronda y sumamos punto a las variables globales
    if porcentaje1 > porcentaje2:
        ganador_ronda = nombre1
        puntos1 = puntos1 + 1
    elif porcentaje2 > porcentaje1:
        ganador_ronda = nombre2
        puntos2 = puntos2 + 1
    else:
        ganador_ronda = "EMPATE"
    
    #Texto de rondas restantes
    rondas_restantes = rondas_max - ronda_actual   #Se modifica la variable de rondas
    tk.Label(ventana,text=f"RONDA {ronda_actual} DE {rondas_max}  —  Rondas restantes: {rondas_restantes}",bg=COLOR_FONDO, fg=COLOR_GRIS,font=FUENTE_PEQUENA).pack(pady=(20, 0))

    #Título de la ventana
    tk.Label(ventana,text="RESULTADOS",bg=COLOR_FONDO,fg=COLOR_ROJO,font=("Courier", 22, "bold")).pack(pady=(10, 30))

    #Frame con los porcentajes obtenidos por los usuarios
    frame_resultados = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_resultados.pack()

    #Texto porcentaje jugador 1
    tk.Label(frame_resultados, text=nombre1, bg=COLOR_FONDO,fg=COLOR_GRIS, font=FUENTE_PEQUENA).grid(row=0, column=0, padx=60)
    tk.Label(frame_resultados, text=f"{porcentaje1:.0f}%", bg=COLOR_FONDO,
             fg=COLOR_BLANCO, font=("Courier", 42, "bold")).grid(row=1, column=0, padx=60)

    #Separador para verse bello
    tk.Label(frame_resultados, text="VS", bg=COLOR_FONDO,fg=COLOR_ROJO, font=("Courier", 18, "bold")).grid(row=1, column=1, padx=20)

    #Texto porcentaje jugador 2
    tk.Label(frame_resultados, text=nombre2, bg=COLOR_FONDO,fg=COLOR_GRIS, font=FUENTE_PEQUENA).grid(row=0, column=2, padx=60)
    tk.Label(frame_resultados, text=f"{porcentaje2:.0f}%", bg=COLOR_FONDO,fg=COLOR_BLANCO, font=("Courier", 42, "bold")).grid(row=1, column=2, padx=60)

    #Texto con el ganador de la ronda
    if ganador_ronda == "EMPATE":
        texto_ganador = "— RONDA EMPATADA —"
    else:
        texto_ganador = f"— {ganador_ronda} GANA LA RONDA —"  #Pone el nombre del jugador mas el texto indicado

    tk.Label(ventana,text=texto_ganador, bg=COLOR_FONDO,fg=COLOR_ROJO,font=("Courier", 13, "bold")).pack(pady=20)

    #Texto con el puntaje acumulado de los dos jugadores
    tk.Label(ventana,text=f"{nombre1}  {puntos1}  —  {puntos2}  {nombre2}",bg=COLOR_FONDO,fg=COLOR_BLANCO,font=("Courier", 13)).pack()

    # Botón continuar
    def al_continuar():
        global ronda_actual   #Importa variable de la ronda

        # Verificamos si ya se jugaron todas las rondas
        if ronda_actual >= rondas_max:
            if puntos1 == puntos2:  #Si los puntos son iguales se envia a la pantalla de desempate
                mostrar_pantalla_desempate(nombre1, nombre2)
            else: #si no son iguales se envia a la pantalla de ganador
                mostrar_pantalla_ganador(nombre1, nombre2)
        else: # si no se jugaron todas las rondas se suma uno a la ronta y se continua
            ronda_actual = ronda_actual + 1
            mostrar_pantalla_juego(nombre1, nombre2, puntos1, puntos2)
    
    #Boton para continuar la partida
    tk.Button(ventana, text="CONTINUAR  →", bg=COLOR_FONDO,fg=COLOR_ROJO,font=FUENTE_BOTON,relief=tk.FLAT,
        bd=0,activebackground=COLOR_ROJO_TENUE,activeforeground=COLOR_BLANCO,cursor="hand2",command=al_continuar).pack(pady=30)
    
    #Boton para cambiar la configuracion de la partida
    tk.Button(ventana,text="⚙ AJUSTES",bg=COLOR_FONDO,fg=COLOR_GRIS,font=FUENTE_PEQUENA,relief=tk.FLAT,bd=0,
        cursor="hand2",command=lambda: mostrar_pantalla_ajustes(lambda: mostrar_pantalla_resultados(nombre1, nombre2, palabra_sistema, "????", "????"))).pack()

#PANTALLA 5.2 - Desempate
def mostrar_pantalla_desempate(nombre1, nombre2):
    for widget in ventana.winfo_children():  #Escanear objetos de la pantalla
        widget.destroy()  #Eliminarlos

    # Título y subtitulos de la pantalla
    tk.Label(ventana,text="¡EMPATE!",bg=COLOR_FONDO,fg=COLOR_ROJO,font=("Courier", 36, "bold")).pack(pady=(80, 10))

    tk.Label(ventana,text="ninguno pudo definirlo...",bg=COLOR_FONDO,fg=COLOR_GRIS,font=("Courier", 11)).pack()

    tk.Label(ventana,text="SE VIENE LA RONDA EXTRA",bg=COLOR_FONDO,fg=COLOR_BLANCO,font=("Courier", 14, "bold")).pack(pady=(30, 50))

    #Texto con el puntaje actual
    tk.Label(ventana,text=f"{nombre1}  {puntos1}  —  {puntos2}  {nombre2}",bg=COLOR_FONDO,fg=COLOR_GRIS,font=("Courier", 12)).pack()

    #Botón y funcion de ronda extra
    def al_continuar():
        global ronda_actual, rondas_max, tiempo_ronda_extra  #Se importan variables
        rondas_extra = ronda_actual - rondas_max + 1  # cuántas extras llevamos
        #Se calcula el tiempo según la ronda extra
        tiempo_ronda_extra = max(5, 15 - ((rondas_extra - 1) * 3))

        #Se suma 1 a la ronda actual y a la ronda extra
        rondas_max   = rondas_max + 1
        ronda_actual = ronda_actual + 1
        mostrar_pantalla_juego(nombre1, nombre2, puntos1, puntos2)  #Activa la pantalla del juego con las rondas extras

    #Ajustes del boton ronda extra
    tk.Button(ventana,text="JUGAR RONDA EXTRA  →",bg=COLOR_FONDO,fg=COLOR_ROJO,font=FUENTE_BOTON,relief=tk.FLAT,bd=0,activebackground=COLOR_ROJO_TENUE,
        activeforeground=COLOR_BLANCO,cursor="hand2",command=al_continuar).pack(pady=30)
    
    #Boton para aceptar empate, menos llamativo que el de ronda extra
    tk.Button(ventana,text="ACEPTAR EMPATE",bg=COLOR_FONDO,fg=COLOR_GRIS,font=FUENTE_PEQUENA,relief=tk.FLAT,bd=0,activebackground=COLOR_ROJO_TENUE,
        activeforeground=COLOR_BLANCO,cursor="hand2",command=lambda: mostrar_pantalla_ganador(nombre1, nombre2)).pack(pady=(0, 10))

#PANTALLA 6 - GANADOR
def mostrar_pantalla_ganador(nombre1, nombre2):
    for widget in ventana.winfo_children(): #Analizar objetos en la pantalla anterior
        widget.destroy() #Eliminar objetos

    #determinacion del ganador final, comparacion de puntos
    if puntos1 > puntos2:
        ganador = nombre1
        perdedor = nombre2
    elif puntos2 > puntos1:
        ganador = nombre2
        perdedor = nombre1
    else:
        ganador = "EMPATE"

    # Título y subtitulos de la pantalla
    if ganador == "EMPATE":
        tk.Label(ventana, text="— EMPATE FINAL —", bg=COLOR_FONDO,fg=COLOR_GRIS, font=("Courier", 28, "bold")).pack(pady=(80, 10))
        tk.Label(ventana, text="ninguno pudo con el otro...", bg=COLOR_FONDO,fg=COLOR_GRIS, font=("Courier", 11)).pack()
    else:
        tk.Label(ventana, text="¡GANADOR!", bg=COLOR_FONDO,fg=COLOR_GRIS, font=("Courier", 14)).pack(pady=(60, 5))
        tk.Label(ventana, text=ganador, bg=COLOR_FONDO, fg=COLOR_ROJO, font=("Courier", 48, "bold")).pack()
        tk.Label(ventana, text=f"derrota a {perdedor}", bg=COLOR_FONDO,fg=COLOR_GRIS, font=("Courier", 11)).pack(pady=(5, 0))

    #Texto que indica los puntos obtenidos al final
    tk.Label(ventana,text=f"{nombre1}  {puntos1}  —  {puntos2}  {nombre2}",bg=COLOR_FONDO,fg=COLOR_BLANCO,font=("Courier", 14)).pack(pady=30)

    #Botón jugar de nuevo 
    def jugar_de_nuevo():
        global puntos1, puntos2, ronda_actual, rondas_max  #Importa variables y las reinicia
        puntos1      = 0
        puntos2      = 0
        ronda_actual = 1
        rondas_max   = 3
        mostrar_pantalla_inicio()

    #Ajustes del botón
    tk.Button(ventana,text="JUGAR DE NUEVO  →",bg=COLOR_FONDO,fg=COLOR_ROJO,font=FUENTE_BOTON,relief=tk.FLAT,bd=0,activebackground=COLOR_ROJO_TENUE,activeforeground=COLOR_BLANCO,
        cursor="hand2",command=jugar_de_nuevo).pack(pady=20)

#PANTALLA DE AJUSTES
def mostrar_pantalla_ajustes(pantalla_anterior):
    for widget in ventana.winfo_children(): #Escanea objetos con iteracion
        widget.destroy() #los destruye cata ves que los escanea

    #Titulo de la ventana
    tk.Label(ventana,text="AJUSTES",bg=COLOR_FONDO,fg=COLOR_ROJO,font=("Courier", 22, "bold")).pack(pady=(40, 30))

    #Modo de salida (Radiobutton = solo una opción a la vez)
    tk.Label(ventana, text="MODO DE PRESENTACIÓN DE LA PALABRA",bg=COLOR_FONDO, fg=COLOR_GRIS, font=FUENTE_PEQUENA).pack()
    frame_modos = tk.Frame(ventana, bg=COLOR_FONDO) #Caja con el boton de opcion
    frame_modos.pack(pady=(10, 5))

    # Opción luz
    tk.Radiobutton(frame_modos,text="💡 LUZ",variable=modo_salida,value="luz",bg=COLOR_FONDO,fg=COLOR_BLANCO,selectcolor=COLOR_ROJO_TENUE,
        activebackground=COLOR_FONDO,font=("Courier", 12, "bold")).grid(row=0, column=0, padx=30, sticky="w")
    # Texto explicativo
    tk.Label(frame_modos,text="La palabra se proyecta letra por letra\nencendiendo los LEDs de la maqueta.",bg=COLOR_FONDO, fg=COLOR_GRIS,
        font=FUENTE_PEQUENA, justify="left").grid(row=1, column=0, padx=30, sticky="w")

    # Opción sonido
    tk.Radiobutton(frame_modos,text="🔊 SONIDO",variable=modo_salida,value="sonido",bg=COLOR_FONDO,fg=COLOR_BLANCO,selectcolor=COLOR_ROJO_TENUE,activebackground=COLOR_FONDO,
        font=("Courier", 12, "bold")).grid(row=0, column=1, padx=30, sticky="w")
    #Texto Explicativo
    tk.Label(frame_modos,text="La palabra se transmite mediante\npulsos del buzzer de la maqueta.",bg=COLOR_FONDO, fg=COLOR_GRIS,font=FUENTE_PEQUENA, justify="left").grid(row=1, column=1, padx=30, sticky="w")

    # ── Modo de comunicación ──
    tk.Label(ventana, text="",
             bg=COLOR_FONDO).pack()  # espaciador

    tk.Label(ventana, text="MODO DE COMUNICACIÓN CON LA MAQUETA",
             bg=COLOR_FONDO, fg=COLOR_GRIS, font=FUENTE_PEQUENA).pack()

    frame_com = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_com.pack(pady=(10, 5))

    #Esto es para configurar el tipo de trasmision
    tk.Radiobutton(frame_com,text="🔌 CABLE",variable=modo_comunicacion,value="cable",bg=COLOR_FONDO,fg=COLOR_BLANCO,selectcolor=COLOR_ROJO_TENUE,
        activebackground=COLOR_FONDO,font=("Courier", 12, "bold")).grid(row=0, column=0, padx=30, sticky="w")
    tk.Label(frame_com,text="Comunicación por USB serial.\nModo predeterminado.",bg=COLOR_FONDO, fg=COLOR_GRIS,font=FUENTE_PEQUENA, justify="left"
    ).grid(row=1, column=0, padx=30, sticky="w")

    tk.Radiobutton(frame_com, text="📡 WIFI",variable=modo_comunicacion,value="wifi",bg=COLOR_FONDO,fg=COLOR_BLANCO,selectcolor=COLOR_ROJO_TENUE,
        activebackground=COLOR_FONDO,font=("Courier", 12, "bold")).grid(row=0, column=1, padx=30, sticky="w")
    #Mensaje que es que aun no esta terminada XD
    tk.Label(frame_com,text="Comunicación inalámbrica WiFi.\nRequiere configuración previa.",bg=COLOR_FONDO, fg=COLOR_GRIS,font=FUENTE_PEQUENA, justify="left"
    ).grid(row=1, column=1, padx=30, sticky="w")

    #Mostrar palabra en pantalla (Checkbutton)
    tk.Label(ventana, text="",bg=COLOR_FONDO).pack()  # espaciador
    tk.Checkbutton(ventana,text="Mostrar la palabra en pantalla durante el juego",variable=mostrar_palabra, bg=COLOR_FONDO,fg=COLOR_BLANCO,selectcolor=COLOR_ROJO_TENUE,
        activebackground=COLOR_FONDO,font=("Courier", 11)).pack()

    tk.Label(ventana,text="Desactivalo para una experiencia más desafiante.",bg=COLOR_FONDO, fg=COLOR_GRIS, font=FUENTE_PEQUENA).pack()

    # Botón volver
    tk.Button(ventana,text="← VOLVER",bg=COLOR_FONDO,fg=COLOR_ROJO,font=FUENTE_BOTON,relief=tk.FLAT,bd=0,activebackground=COLOR_ROJO_TENUE,activeforeground=COLOR_BLANCO,
        cursor="hand2",command=pantalla_anterior).pack(pady=30)

# VENTANA PRINCIPAL
ventana = tk.Tk()

# Ajustes del juego (Listas y checks)
modo_salida= tk.StringVar()   # "luz" o "sonido"
mostrar_palabra = tk.BooleanVar() # True = mostrar, False = ocultar
modo_comunicacion = tk.StringVar()  #Para la comunicacion con la placa
#Ajustes predeterminados
modo_salida.set("luz")        # predeterminado: luz
mostrar_palabra.set(False)    # predeterminado: sin texto
modo_comunicacion.set("cable") #predeterminado: Cable

ventana.title("StrangerTEC")
ventana.geometry("800x600")
ventana.config(bg=COLOR_FONDO)
ventana.resizable(False, False)

# Empieza en la pantalla de inicio
mostrar_pantalla_inicio()

#Loop principal para mantener la pantalla abierta
ventana.mainloop()