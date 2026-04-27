import random     #Libreria para poder elegir una palabra ramdom

def elegir_palabra_al_azar():
    palabras = ["SOS", "HELP", "HEY", "HI", "HOLA", "BYE", "OK", "YES", "NO", "CODE"]       #Lista con las diez palabras
    return random.choice(palabras)     #comando de la libreria para elegir una "Al azar"

palabra = elegir_palabra_al_azar()     #Variable con el resultado
print(f"Palabra elegida: {palabra}")   #Prueba de la funcion