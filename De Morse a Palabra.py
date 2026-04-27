# Se transcribe cada Morse a Letra donde 1 es punto y 0 es espacio
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


# Pruebas
print(binario_a_texto(["01", "000"], 0))                    # NO
print(binario_a_texto(["111", "000", "111"], 0))            # SOS
print(binario_a_texto(["1111", "1", "1011", "1001"], 0))    # HELP