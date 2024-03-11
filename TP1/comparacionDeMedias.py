import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import kstest, norm, lognorm, gamma, mannwhitneyu
import matplotlib
import seaborn as sns


colores = ['negro', 'rojo', 'azul', 'violeta', 'verde', 'amarillo']
coloresNecesariosTecho = ['azul', 'violeta', 'verde', 'amarillo']

def run1(cantidadJugadores):
    jugadores = dict()
    segundosTotales = 0

    for i in range(cantidadJugadores):
        nombre = 'jugador' + str(i + 1)
        jugadorInfo = {
            'rojo': False,
            'azul': False,
            'violeta': False,
            'verde': False,
            'amarillo': False
        }
        jugadores[nombre] = jugadorInfo

    cantRondas = 0
    while True:
        (final, segundosJugados) = ronda1(jugadores)
        segundosTotales += segundosJugados
        cantRondas += 1
        if final:
            break

    minutosJugados = segundosTotales / 60

    return (minutosJugados, cantRondas)

def tirarDado():
    num = random.randint(0, 5)
    return colores[num]

def verificar_paredes_completadas(jugador_info):
    return all(value for key, value in jugador_info.items() if key != 'tiempoJugado')

def turnoJugador1(jugadorInfo):
    while True:
        color = tirarDado()

        if color == 'negro':
            colores_activos = [key for key, value in jugadorInfo.items() if key != 'tiempoJugado' and value]
            if colores_activos:
                color_desactivar = random.choice(colores_activos)
                jugadorInfo[color_desactivar] = False
            return False
        elif color == 'rojo': 
            for color in coloresNecesariosTecho:
                if not jugadorInfo[color]:
                    return False
            
            jugadorInfo['rojo'] = True
            return True
        else:
            if not jugadorInfo[color]:
                jugadorInfo[color] = True
                break

    return turnoJugador1(jugadorInfo)

def ronda1(jugadores):
    segundosJugados = 0
    for jugador, _ in jugadores.items():
        segundosJugados += 7
        if turnoJugador1(jugadores[jugador]):
            return (True, segundosJugados)

    return (False, segundosJugados)

muestras = [10000]

for cantidadMuestras in muestras:
    minutosJugadosN1 = []
    cantRondasN1 = []
    for i in range(cantidadMuestras):
        (minutosJugados, cantRondas) = run1(4)
        minutosJugadosN1.append(minutosJugados)
        cantRondasN1.append(cantRondas)

muestras1 = minutosJugadosN1, cantRondasN1

def run2(cantidadJugadores):
    jugadores = dict()
    segundosTotales = 0

    for i in range(cantidadJugadores):
        nombre = 'jugador' + str(i + 1)
        jugadorInfo = {
            'rojo': False,
            'azul': False,
            'violeta': False,
            'verde': False,
            'amarillo': False
        }
        jugadores[nombre] = jugadorInfo

    cantRondas = 0
    while True:
        (final, segundosJugados) = ronda2(jugadores)
        segundosTotales += segundosJugados
        cantRondas += 1
        if final:
            break

    minutosJugados = segundosTotales / 60

    return (minutosJugados, cantRondas)

def turnoJugador2(jugadorInfo):
    while True:
        color = tirarDado()

        if color == 'negro':
            for key in jugadorInfo:
                jugadorInfo[key] = False
            return False
        elif color == 'rojo': 
            for color in coloresNecesariosTecho:
                if not jugadorInfo[color]:
                    return False
            
            jugadorInfo['rojo'] = True
            return True
        else:
            if not jugadorInfo[color]:
                jugadorInfo[color] = True
                break

    return turnoJugador2(jugadorInfo)

def ronda2(jugadores):
    segundosJugados = 0
    for jugador, _ in jugadores.items():
        segundosJugados += 7
        if turnoJugador2(jugadores[jugador]):
            return (True, segundosJugados)

    return (False, segundosJugados)

muestras = [10000]

for cantidadMuestras in muestras:
    minutosJugadosN2 = []
    cantRondasN2 = []
    for i in range(cantidadMuestras):
        (minutosJugados, cantRondas) = run2(4)
        minutosJugadosN2.append(minutosJugados)
        cantRondasN2.append(cantRondas)

muestras2 = minutosJugadosN2, cantRondasN2

# Realizar el test de Mann-Whitney-U - Cantidad de rondas
import numpy as np
from scipy.stats import mannwhitneyu

stat, pvalue = mannwhitneyu(cantRondasN1, cantRondasN2)

print("Para la variable cantRondasN:")
print(f"Estadístico U = {stat}")
print(f"Valor p = {pvalue}")

if pvalue < 0.05:
    print("Se rechaza la hipótesis nula: hay diferencias significativas.")
else:
    print("No se puede rechazar la hipótesis nula: no hay diferencias significativas.")

# Realizar el test de Mann-Whitney-U - Minutos jugados
stat, pvalue = mannwhitneyu(minutosJugadosN1, minutosJugadosN2)

print("Para la variable cantRondasN:")
print(f"Estadístico U = {stat}")
print(f"Valor p = {pvalue}")

if pvalue < 0.05:
    print("Se rechaza la hipótesis nula: hay diferencias significativas.")
else:
    print("No se puede rechazar la hipótesis nula: no hay diferencias significativas.")
