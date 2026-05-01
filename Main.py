# ─────────────────────────────────────────────
# StrangerTEC — MicroPython Raspberry Pi Pico W
# Comunicación por cable USB serial con la PC
# ─────────────────────────────────────────────

import sys
import time
from machine import Pin, PWM

# ─────────────────────────────────────────────
# PINES
# ─────────────────────────────────────────────

PIN_DATOS = Pin(27, Pin.OUT)   # Datos hacia U1 (74LS164)
PIN_CLK   = Pin(26, Pin.OUT)   # Clock compartido U1 y U2

LED_FILA1 = Pin(15, Pin.OUT)   # Fila 1: A C E G I K M O Q S U W Y
LED_FILA2 = Pin(14, Pin.OUT)   # Fila 2: B D F H J L N P R T V X Z
LED_FILA3 = Pin(13, Pin.OUT)   # Fila 3: 0 1 2 3 4 5 6 7 8 9 - +

buzzer = PWM(Pin(5))           # Buzzer pasivo
buzzer.freq(200)               # Frecuencia del sonalert

boton = Pin(16, Pin.IN, Pin.PULL_DOWN)  # Botón jugador 2

# ─────────────────────────────────────────────
# REGISTROS DE CORRIMIENTO 74LS164
# ─────────────────────────────────────────────

def enviar_bit(bit):
    PIN_DATOS.value(bit)
    PIN_CLK.value(1)
    time.sleep_us(10)
    PIN_CLK.value(0)

def encender_columna(columna):
    for i in range(16, 0, -1):
        enviar_bit(1 if i == columna else 0)

def apagar_columnas():
    for i in range(16):
        enviar_bit(0)

def encender_fila(fila):
    LED_FILA1.value(1 if fila == 1 else 0)
    LED_FILA2.value(1 if fila == 2 else 0)
    LED_FILA3.value(1 if fila == 3 else 0)

def apagar_filas():
    LED_FILA1.value(0)
    LED_FILA2.value(0)
    LED_FILA3.value(0)

# ─────────────────────────────────────────────
# MAPA DE LETRAS A COORDENADAS (fila, columna)
# ─────────────────────────────────────────────

MAPA_LETRAS = {
    "A": (1, 1),  "C": (1, 2),  "E": (1, 3),  "G": (1, 4),
    "I": (1, 5),  "K": (1, 6),  "M": (1, 7),  "O": (1, 8),
    "Q": (1, 9),  "S": (1, 10), "U": (1, 11), "W": (1, 12),
    "Y": (1, 13),
    "B": (2, 1),  "D": (2, 2),  "F": (2, 3),  "H": (2, 4),
    "J": (2, 5),  "L": (2, 6),  "N": (2, 7),  "P": (2, 8),
    "R": (2, 9),  "T": (2, 10), "V": (2, 11), "X": (2, 12),
    "Z": (2, 13),
    "0": (3, 1),  "1": (3, 2),  "2": (3, 3),  "3": (3, 4),
    "4": (3, 5),  "5": (3, 6),  "6": (3, 7),  "7": (3, 8),
    "8": (3, 9),  "9": (3, 10), "-": (3, 11), "+": (3, 12),
}

# ─────────────────────────────────────────────
# MODO LUZ — muestra letra por letra con LEDs
# ─────────────────────────────────────────────

def mostrar_letra_led(letra):
    if letra not in MAPA_LETRAS:
        return
    fila, columna = MAPA_LETRAS[letra]
    encender_columna(columna)
    encender_fila(fila)
    time.sleep(1)
    apagar_filas()
    apagar_columnas()
    time.sleep(0.5)

def mostrar_palabra_led(palabra):
    for letra in palabra:
        mostrar_letra_led(letra)

# ─────────────────────────────────────────────
# MODO SONIDO — recibe binario con | de separador
# ejemplo: "1111|000|1011|10" = HOLA
# 1 = punto (pip corto), 0 = raya (piiip largo)
# ─────────────────────────────────────────────

UNIDAD = 0.2

def sonar_simbolo(simbolo):
    if simbolo == "1":
        buzzer.duty_u16(30000)
        time.sleep(UNIDAD)
    else:
        buzzer.duty_u16(30000)
        time.sleep(UNIDAD * 3)
    buzzer.duty_u16(0)
    time.sleep(UNIDAD)

def mostrar_palabra_sonido(binario):
    letras_binario = binario.split("|")
    for codigo in letras_binario:
        for simbolo in codigo:
            sonar_simbolo(simbolo)
        time.sleep(UNIDAD * 3)

# ─────────────────────────────────────────────
# CAPTURA MORSE DEL JUGADOR 2
# buzzer suena en tiempo real mientras presiona
# punto < 200ms, raya >= 200ms
# pausa letra = 600ms, pausa palabra = 1400ms
# ─────────────────────────────────────────────

def capturar_morse_boton():
    lista_codigos = []
    codigo_actual = ""
    palabra_lista = False

    sys.stdout.write("# Esperando jugador 2...\n")

    while not palabra_lista:
        if boton.value() == 1:
            tiempo_inicio = time.ticks_ms()

            # Buzzer suena mientras presiona
            buzzer.duty_u16(20000)
            while boton.value() == 1:
                pass
            buzzer.duty_u16(0)

            duracion = time.ticks_diff(time.ticks_ms(), tiempo_inicio)

            if duracion < 200:
                codigo_actual = codigo_actual + "1"
                sys.stdout.write("# .\n")
            else:
                codigo_actual = codigo_actual + "0"
                sys.stdout.write("# -\n")

            tiempo_espera = time.ticks_ms()
            while boton.value() == 0:
                pausa = time.ticks_diff(time.ticks_ms(), tiempo_espera)

                # Pausa de letra (600ms)
                if pausa >= 600 and codigo_actual != "":
                    lista_codigos.append(codigo_actual)
                    sys.stdout.write("# letra: " + codigo_actual + "\n")
                    codigo_actual = ""

                # Pausa de palabra (1400ms)
                if pausa >= 1400:
                    palabra_lista = True
                    break

    return lista_codigos

# ─────────────────────────────────────────────
# DETERMINA EL MODO POR EL CONTENIDO
# con "|" es binario (sonido), sin "|" es texto (luz)
# ─────────────────────────────────────────────

def procesar_mensaje(mensaje):
    if "|" in mensaje:
        sys.stdout.write("# Modo sonido\n")
        mostrar_palabra_sonido(mensaje)
    else:
        sys.stdout.write("# Modo luz\n")
        mostrar_palabra_led(mensaje)

# ─────────────────────────────────────────────
# PROGRAMA PRINCIPAL — comunicación por cable
# ─────────────────────────────────────────────

sys.stdout.write("# StrangerTEC Pico lista, esperando palabra...\n")

while True:
    # Lee la palabra que manda la PC por cable USB
    linea = sys.stdin.readline().strip()

    if linea == "":
        continue

    sys.stdout.write("# Recibido: " + linea + "\n")

    # Muestra la palabra segun el modo
    procesar_mensaje(linea)

    # Captura morse del jugador 2
    lista_codigos = capturar_morse_boton()

    # Envia respuesta a la PC separada por comas
    # Esta es la unica linea sin # para que la PC la procese
    respuesta = ",".join(lista_codigos)
    sys.stdout.write(respuesta + "\n")