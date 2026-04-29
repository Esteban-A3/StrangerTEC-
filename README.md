# StrangerTEC Morse Translator

Proyecto desarrollado para el curso **CE-1104 Fundamentos de Sistemas Computacionales** del Instituto Tecnológico de Costa Rica.

## Descripción General
StrangerTEC Morse Translator es un sistema interactivo inspirado en *Stranger Things*, diseñado para permitir la comunicación entre jugadores mediante **código Morse** utilizando una **Raspberry Pi Pico W**, LEDs, buzzer, botones e interfaz gráfica en Python.

El proyecto combina:
- Electrónica básica
- Programación en Python
- Programación en MicroPython
- Comunicación serial / WiFi
- Diseño de documentación técnica

# Objetivo
Desarrollar una maqueta funcional capaz de transmitir, interpretar y evaluar mensajes en código Morse mediante señales luminosas, sonoras y entradas físicas.

---

# Estructura del Repositorio

## `/pc_app/`
Contiene el código de la aplicación para computadora:
- Interfaz gráfica
- Sistema de puntaje
- Lógica del juego
- Lista de frases
- Conversión texto ↔ Morse


##  `/pico_w/`
Contiene el código para la Raspberry Pi Pico W:
- Lectura de botones
- Detección de puntos y rayas
- Control de LEDs
- Control de buzzer
- Comunicación serial / WiFi


## `/docs/`
Incluye la documentación formal del proyecto:

### Documento Técnico
Contiene:
- Introducción
- Análisis de resultados
- Conclusiones
- Recomendaciones
- Diagramas del sistema
- Bibliografía

### Documento de Atributos
Contiene:
- Reglas de grupo
- Estrategias de trabajo
- Roles
- Planificación
- Coevaluación
- Evaluación de estrategias


## `/ideas/`
Documento complementario utilizado para:
- Lluvia de ideas
- Bocetos iniciales
- Propuestas de diseño
- Mejoras futuras
- Notas de planificación


## `/assets/`
Recursos visuales del proyecto:
- Diagramas
- Imágenes de referencia
- Bocetos de maqueta

# Sistema Morse
- Punto = Pulso corto
- Raya = Pulso largo
- Espacio entre símbolos = 1 unidad
- Espacio entre letras = 3 unidades
- Espacio entre palabras = 7 unidades


# Tecnologías Utilizadas
- Python
- MicroPython
- Tkinter / GUI
- Raspberry Pi Pico W
- GitHub
- Electrónica digital básica


# Integrantes
- Esteban Sánchez
- Gerald Calderón


# Estado del Proyecto
En desarrollo académico – Proyecto I Semestre 2026.

# 🚀 Notas
Este repositorio funciona como respaldo, organización y control de versiones del proyecto completo, incluyendo código, documentación y planificación.
