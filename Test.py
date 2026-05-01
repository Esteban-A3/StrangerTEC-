# ─────────────────────────────────────────────
# StrangerTEC — Código de prueba de componentes
# Prueba: LEDs, buzzer y botón
# ─────────────────────────────────────────────

from machine import Pin, PWM
import time

# ── Pines ──
PIN_DATOS = Pin(27, Pin.OUT)
PIN_CLK   = Pin(26, Pin.OUT)

LED_FILA1 = Pin(15, Pin.OUT)
LED_FILA2 = Pin(14, Pin.OUT)
LED_FILA3 = Pin(13, Pin.OUT)

buzzer = PWM(Pin(5))
buzzer.freq(200)

boton = Pin(16, Pin.IN, Pin.PULL_DOWN)

# ── Funciones de registro ──
def enviar_bit(bit):
    PIN_DATOS.value(bit)
    PIN_CLK.value(1)
    time.sleep_us(10)
    PIN_CLK.value(0)

def encender_columna(columna):
    for i in range(16, 0, -1):
        if i == columna:
            enviar_bit(1)
        else:
            enviar_bit(0)

def apagar_columnas():
    for i in range(16):
        enviar_bit(0)

def apagar_filas():
    LED_FILA1.value(0)
    LED_FILA2.value(0)
    LED_FILA3.value(0)

# ─────────────────────────────────────────────
# PRUEBA 1: LEDs de columna (registro 74LS164)
# Enciende uno por uno del LED1 al LED13
# ─────────────────────────────────────────────
print("PRUEBA 1: LEDs de columna uno por uno...")
LED_FILA1.value(1)   # encendemos fila 1 para ver las columnas
for columna in range(1, 14):
    print(f"  Columna {columna} encendida")
    encender_columna(columna)
    time.sleep(0.8)
    apagar_columnas()
    time.sleep(0.2)

LED_FILA1.value(0)
print("PRUEBA 1 terminada\n")
time.sleep(1)

# ─────────────────────────────────────────────
# PRUEBA 2: LEDs de fila (directos)
# Enciende LED14, LED15 y LED16
# ─────────────────────────────────────────────
print("PRUEBA 2: LEDs de fila directos...")
encender_columna(1)   # columna 1 encendida para verlos

print("  Fila 1 (LED14)")
LED_FILA1.value(1)
time.sleep(1)
LED_FILA1.value(0)
time.sleep(0.3)

print("  Fila 2 (LED15)")
LED_FILA2.value(1)
time.sleep(1)
LED_FILA2.value(0)
time.sleep(0.3)

print("  Fila 3 (LED16)")
LED_FILA3.value(1)
time.sleep(1)
LED_FILA3.value(0)
time.sleep(0.3)

apagar_columnas()
print("PRUEBA 2 terminada\n")
time.sleep(1)

# ─────────────────────────────────────────────
# PRUEBA 3: Buzzer
# Suena 3 veces
# ─────────────────────────────────────────────
print("PRUEBA 3: Buzzer...")
for i in range(3):
    print(f"  Pitido {i + 1}")
    buzzer.duty_u16(30000)
    time.sleep(0.3)
    buzzer.duty_u16(0)
    time.sleep(0.3)

print("PRUEBA 3 terminada\n")
time.sleep(1)

# ─────────────────────────────────────────────
# PRUEBA 4: Botón
# Esperá que presiones el botón 3 veces
# ─────────────────────────────────────────────
print("PRUEBA 4: Botón — presioná 3 veces...")
presiones = 0
while presiones < 3:
    if boton.value() == 1:
        presiones = presiones + 1
        print(f"  Presión detectada! ({presiones}/3)")
        buzzer.duty_u16(20000)   # pitito de confirmación
        time.sleep(0.1)
        buzzer.duty_u16(0)
        while boton.value() == 1:   # espera que suelten
            pass
        time.sleep(0.2)

print("PRUEBA 4 terminada\n")
print("=== TODAS LAS PRUEBAS COMPLETADAS ===")