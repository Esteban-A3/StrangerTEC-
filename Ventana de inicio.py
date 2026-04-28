import tkinter as tk
from tkinter import Toplevel

# STRANGERTEC — Ventana principal del juego

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
        mostrar_pantalla_lobby(nombre1, nombre2)
    
    #Boton de Continuar
    boton = tk.Button(ventana,text="CONTINUAR  →",bg=COLOR_FONDO,fg=COLOR_ROJO,font=FUENTE_BOTON,relief=tk.FLAT,bd=0, activebackground=COLOR_ROJO_TENUE,
        activeforeground=COLOR_BLANCO,cursor="hand2",command=al_continuar)
    boton.pack(pady=20)


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
        activebackground=COLOR_ROJO_TENUE,activeforeground=COLOR_BLANCO,cursor="hand2",command=lambda: print("¡Juego iniciado!")  # Aquí se conectará la lógica del juego
)
    boton_iniciar.pack()


# VENTANA PRINCIPAL
ventana = tk.Tk()
ventana.title("StrangerTEC")
ventana.geometry("700x500")
ventana.config(bg=COLOR_FONDO)
ventana.resizable(False, False)

# Empieza en la pantalla de inicio
mostrar_pantalla_inicio()

ventana.mainloop()