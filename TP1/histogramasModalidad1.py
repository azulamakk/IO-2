# En este archivo se simula el caso en el que el lobo, al tocar color negro solo tira una pared, la cual elige aleatoriamente
import random
import numpy as np
import matplotlib.pyplot as plt

colores = ['negro', 'rojo', 'azul', 'violeta', 'verde', 'amarillo']
coloresNecesariosTecho = ['azul', 'violeta', 'verde', 'amarillo']


def run(cantidadJugadores):
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
        (final, segundosJugados) = ronda(jugadores)
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

def turnoJugador(jugadorInfo):
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

    return turnoJugador(jugadorInfo)

def ronda(jugadores):
    segundosJugados = 0
    for jugador, _ in jugadores.items():
        segundosJugados += 7
        if turnoJugador(jugadores[jugador]):
            return (True, segundosJugados)

    return (False, segundosJugados)


def simulacion_y_grafico(cantidadJugadores, cantidadMuestras):
    resultados = []
    for _ in range(cantidadMuestras):
        minutos, _ = run(cantidadJugadores)
        resultados.append(minutos)

    plt.hist(resultados, bins=20, alpha=0.7, color='navy')
    plt.xlabel('Minutos jugados', fontname='Times New Roman')
    plt.ylabel('Frecuencia', fontname='Times New Roman')
    plt.title(f'Histograma de minutos jugados ({cantidadJugadores} jugadores, {cantidadMuestras} muestras). Modalidad I.', fontname='Times New Roman')
    plt.grid(False)
    plt.show()

simulacion_y_grafico(4, 10000)