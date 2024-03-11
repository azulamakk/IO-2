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


datos_minutos = []
datos_rondas = []

for cantidadJugadores in range(1,500):
    minutosJugadosN = []
    cantRondasN = []
    for i in range(100):
        (minutosJugados, cantRondas) = run(cantidadJugadores)
        minutosJugadosN.append(minutosJugados)
        cantRondasN.append(cantRondas)

    datos_minutos.append(np.mean(minutosJugadosN))
    datos_rondas.append(np.mean(cantRondasN))

print(datos_minutos)
print(datos_rondas)

for cantidadJugadores in [1, 2, 4, 10, 25, 50, 100, 250, 500]:
    minutosJugadosN = []
    cantRondasN = []
    for i in range(100):
        (minutosJugados, cantRondas) = run(cantidadJugadores)
        minutosJugadosN.append(minutosJugados)
        cantRondasN.append(cantRondas)
        
    print(f"\nResultados para {cantidadJugadores} jugadores:")
    print("Minutos jugados:")
    print("Media:", np.mean(minutosJugadosN))
    print("Desviación estándar:", np.std(minutosJugadosN))
    print("Máximo:", np.max(minutosJugadosN))
    print("Mínimo:", np.min(minutosJugadosN))
    print("Q1:", np.percentile(minutosJugadosN, 25))
    print("Mediana:", np.median(minutosJugadosN))
    print("Q3:", np.percentile(minutosJugadosN, 75))
    print("Cantidad de rondas:", np.mean(cantRondasN))
    
plt.rc('font', family='Times New Roman')

plt.plot(range(1,500), datos_minutos, color='navy', marker='o')
plt.title('Minutos jugados vs Cantidad de jugadores. Modalidad I.')
plt.xlabel('Cantidad de jugadores')
plt.ylabel('Minutos jugados')
plt.grid(True)
plt.show()

plt.plot(range(1,500), datos_rondas, color='navy', marker='o')
plt.title('Cantidad de Rondas vs Cantidad de jugadores. Modalidad I.')
plt.xlabel('Cantidad de jugadores')
plt.ylabel('Cantidad de rondas')
plt.grid(True)
plt.show()