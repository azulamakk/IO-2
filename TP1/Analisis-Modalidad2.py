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

    return turnoJugador(jugadorInfo)

def ronda(jugadores):
    segundosJugados = 0
    for jugador, _ in jugadores.items():
        segundosJugados += 7
        if turnoJugador(jugadores[jugador]):
            return (True, segundosJugados)

    return (False, segundosJugados)

muestras = [25, 100, 500, 1000, 5000, 10000]

for cantidadMuestras in muestras:
    minutosJugadosN = []
    cantRondasN = []
    for i in range(cantidadMuestras):
        (minutosJugados, cantRondas) = run(4)
        minutosJugadosN.append(minutosJugados)
        cantRondasN.append(cantRondas)
        
    print(f"\nResultados para {cantidadMuestras} muestras con 4 jugadores:")
    print("Minutos jugados:")
    print("Media:", np.mean(minutosJugadosN))
    print("Desviación estándar:", np.std(minutosJugadosN))
    print("Máximo:", np.max(minutosJugadosN))
    print("Mínimo:", np.min(minutosJugadosN))
    print("Q1:", np.percentile(minutosJugadosN, 25))
    print("Mediana:", np.median(minutosJugadosN))
    print("Q3:", np.percentile(minutosJugadosN, 75))
    
    plt.hist(minutosJugadosN, bins=20, color='navy', edgecolor='black')
    plt.title(f'Histograma de Minutos Jugados para 4 jugadores ({cantidadMuestras} muestras)')
    plt.xlabel('Minutos jugados')
    plt.ylabel('Frecuencia')
    plt.grid(True)
    plt.show()

    plt.hist(cantRondasN, bins=20, color='navy', edgecolor='black')
    plt.title(f'Histograma de Cantidad de Rondas para 4 jugadores ({cantidadMuestras} muestras)')
    plt.xlabel('Cantidad de rondas')
    plt.ylabel('Frecuencia')
    plt.grid(True)
    plt.show()