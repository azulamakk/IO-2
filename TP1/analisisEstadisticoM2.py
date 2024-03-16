import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kstest, norm, lognorm, gamma
import matplotlib
import seaborn as sns

plt.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.it'] = 'Times New Roman:italic'
matplotlib.rcParams['mathtext.rm'] = 'Times New Roman'
matplotlib.rcParams['mathtext.bf'] = 'Times New Roman:bold'

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
    
    min_value = min(minutosJugadosN)
    max_value = max(minutosJugadosN)
    bin_width = 0.5

    num_bins = int(np.ceil((max_value - min_value) / bin_width))

    plt.hist(minutosJugadosN, bins=num_bins, range=(min_value, max_value), color='navy', edgecolor='black')
    plt.title(f'Histograma de Minutos Jugados para 4 jugadores ({cantidadMuestras} muestras)')
    plt.xlabel('Minutos jugados')
    plt.ylabel('Frecuencia')
    plt.grid(False)
    plt.show()

    # Repite el proceso para el otro conjunto de datos (cantRondasN)
    min_value = min(cantRondasN)
    max_value = max(cantRondasN)

    num_bins = int(np.ceil((max_value - min_value) / bin_width))

    plt.hist(cantRondasN, bins=num_bins, range=(min_value, max_value), color='navy', edgecolor='black')
    plt.title(f'Histograma de Cantidad de Rondas para 4 jugadores ({cantidadMuestras} muestras)')
    plt.xlabel('Cantidad de rondas')
    plt.ylabel('Frecuencia')
    plt.grid(False)
    plt.show()
    
muestras = [10000]

for cantidadMuestras in muestras:
    minutosJugadosN = []
    cantRondasN = []
    for i in range(cantidadMuestras):
        (minutosJugados, cantRondas) = run(4)
        minutosJugadosN.append(minutosJugados)
        cantRondasN.append(cantRondas)

# Test de Kolmogorov-Smirnov para las rondas - normalidad
ks_stat_rondas, p_value_rondas = kstest(cantRondasN, 'norm', args=(np.mean(cantRondasN), np.std(cantRondasN)))

print("Test de Kolmogorov-Smirnov para la cantidad de rondas:")
print("Estadístico KS:", ks_stat_rondas)
print("Valor p:", '{:.20f}'.format(p_value_rondas))

# Test de Kolmogorov-Smirnov para los minutos jugados - normalidad
ks_stat_minutos, p_value_minutos = kstest(minutosJugadosN, 'norm', args=(np.mean(minutosJugadosN), np.std(minutosJugadosN)))

print("\nTest de Kolmogorov-Smirnov para los minutos jugados:")
print("Estadístico KS:", ks_stat_minutos)
print("Valor p:", '{:.20f}'.format(p_value_minutos))

# Test de Kolmogorov-Smirnov para las rondas - lognormal
ks_stat_rondas, p_value_rondas = kstest(cantRondasN, 'lognorm', args=(np.std(np.log(cantRondasN)), 0, np.exp(np.mean(np.log(cantRondasN)))))

print("Test de Kolmogorov-Smirnov para la cantidad de rondas:")
print("Estadístico KS:", ks_stat_rondas)
print("Valor p:", '{:.20f}'.format(p_value_rondas))

# Test de Kolmogorov-Smirnov para los minutos jugados - lognormal
ks_stat_minutos, p_value_minutos = kstest(minutosJugadosN, 'lognorm', args=(np.std(np.log(minutosJugadosN)), 0, np.exp(np.mean(np.log(minutosJugadosN)))))

print("\nTest de Kolmogorov-Smirnov para los minutos jugados:")
print("Estadístico KS:", ks_stat_minutos)
print("Valor p:", '{:.20f}'.format(p_value_minutos))

from scipy.stats import kstest, gamma

# Test de Kolmogorov-Smirnov para las rondas - gamma
shape_rondas, loc_rondas, scale_rondas = gamma.fit(cantRondasN)
ks_stat_rondas, p_value_rondas = kstest(cantRondasN, 'gamma', args=(shape_rondas, loc_rondas, scale_rondas))

print("Test de Kolmogorov-Smirnov para la cantidad de rondas:")
print("Estadístico KS:", ks_stat_rondas)
print("Valor p:", '{:.20f}'.format(p_value_rondas))

# Test de Kolmogorov-Smirnov para los minutos jugados - gamma
shape_minutos, loc_minutos, scale_minutos = gamma.fit(minutosJugadosN)
ks_stat_minutos, p_value_minutos = kstest(minutosJugadosN, 'gamma', args=(shape_minutos, loc_minutos, scale_minutos))

print("\nTest de Kolmogorov-Smirnov para los minutos jugados:")
print("Estadístico KS:", ks_stat_minutos)
print("Valor p:", '{:.20f}'.format(p_value_minutos))

# Grafico cantidad de muestras vs cantidad de jugadores
def simulacion_y_grafico(cantidadJugadores, cantidadMuestras):
    resultados = []
    for _ in range(cantidadMuestras):
        minutos, _ = run(cantidadJugadores)
        resultados.append(minutos)

    plt.hist(resultados, bins=20, alpha=0.7, color='navy')
    plt.xlabel('Minutos jugados', fontname='Times New Roman')
    plt.ylabel('Frecuencia', fontname='Times New Roman')
    plt.title(f'Histograma de minutos jugados ({cantidadJugadores} jugadores, {cantidadMuestras} muestras). Modalidad II.', fontname='Times New Roman')
    plt.grid(False)
    plt.show()

simulacion_y_grafico(4, 10000)

def simulacion_y_grafico1(cantidadJugadores, cantidadMuestras):
    resultados = []
    for _ in range(cantidadMuestras):
        _, rondas = run(cantidadJugadores)
        resultados.append(rondas)

    max_rondas = max(resultados)
    bins = np.arange(max_rondas + 2) - 0.5  
    plt.hist(resultados, bins=bins, alpha=0.7, color='navy')
    plt.xlabel('rondas jugadas', fontname='Times New Roman')
    plt.ylabel('Frecuencia', fontname='Times New Roman')
    plt.title(f'Histograma de rondas jugados ({cantidadJugadores} jugadores, {cantidadMuestras} muestras). Modalidad II.', fontname='Times New Roman')
    plt.grid(False)
    plt.show()

simulacion_y_grafico1(4, 10000)

def boxplotMinutos(datos):
    plt.boxplot(datos, patch_artist=True,boxprops=dict(facecolor='navy'))
    plt.title('Boxplot de minutos jugados. Modalidad II.')
    plt.xlabel('Minutos jugados')
    plt.grid(False)
    plt.show()

def boxplotRondas(datos):
    plt.boxplot(datos, patch_artist=True, boxprops=dict(facecolor='navy'))
    plt.title('Boxplot de cantidad de rondas. Modalidad II.')
    plt.xlabel('Cantidad de rondas')
    plt.grid(False)
    plt.show()

boxplotMinutos(minutosJugadosN)
boxplotRondas(cantRondasN)