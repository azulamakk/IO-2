# En este archivo se simula el caso en el que el lobo, al tocar color negro tira todas las paredes
import random

colores = ['negro', 'rojo', 'azul', 'violeta', 'verde', 'amarillo']
jugadores = dict()
segundosTotales = 0
cantRondas = 1
estadoPartida = True

def tirarDado():
    num = random.randint(0, 5)
    return colores[num]

def verificar_paredes_completadas(jugador_info):
    return all(value for key, value in jugador_info.items() if key != 'tiempoJugado')

def turnoJugador(jugador):
    global segundosTotales
    segundosJugados = 7  # Tiempo promedio por turno
    segundosTotales += segundosJugados
    jugadorInfo = jugadores[jugador]

    while True:
        color = tirarDado()

        if color == 'negro':
            jugadores[jugador] = {key: False for key in jugadores[jugador]}
            return
        elif color == 'rojo': 
            if not jugadorInfo['rojo']:
                jugadorInfo['rojo'] = True
                jugadores[jugador] = jugadorInfo
                return
        else:
            if not jugadorInfo[color]:
                jugadorInfo[color] = True
                jugadores[jugador] = jugadorInfo
                break

    return turnoJugador(jugador)

def ronda():
    global cantRondas, estadoPartida
    for jugador, _ in jugadores.items():
        turnoJugador(jugador)

    cantRondas += 1

cantidadJugadores = int(input("Por favor, ingresa la cantidad de jugadores: "))
for i in range(cantidadJugadores):
    nombre = 'jugador' + str(i + 1)
    jugadorInfo = {
        'tiempoJugado': 0,
        'rojo': False,
        'azul': False,
        'violeta': False,
        'verde': False,
        'amarillo': False
    }
    jugadores[nombre] = jugadorInfo

while estadoPartida:
    ronda()
    for jugador, info in jugadores.items():
        if verificar_paredes_completadas(info):
            estadoPartida = False
            break

minutosJugados = segundosTotales / 60

print('La cantidad de minutos jugados es:', minutosJugados)
print('La cantidad de rondas jugadas es:', cantRondas)