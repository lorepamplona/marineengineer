import serial
import numpy as np
from scipy.optimize import minimize
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Inicia a comunicação com os sensores do sistema de propulsão
sensor_velocidade = serial.Serial('COM1', 9600)
sensor_direcao = serial.Serial('COM2', 9600)
sensor_temperatura = serial.Serial('COM3', 9600)

# Define as constantes do sistema de propulsão
potencia_maxima = 5000
angulo_maximo = 30
temperatura_maxima = 80

class Atuador:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    def ativar(self, valor):
        if valor:
            GPIO.output(self.pin, GPIO.HIGH)
        else:
            GPIO.output(self.pin, GPIO.LOW)

atuador_potencia = Atuador(18)
atuador_angulo = Atuador(23)

# Monitora os sensores do sistema de propulsão e atua nos atuadores
def controlador_propulsao():
    while True:
        velocidade = float(sensor_velocidade.readline().decode())
        direcao = float(sensor_direcao.readline().decode())
        temperatura = float(sensor_temperatura.readline().decode())
        potencia = calcular_potencia(velocidade, direcao, temperatura)
        angulo = calcular_angulo(velocidade, direcao, temperatura)
        atuador_potencia.ativar(potencia)
        atuador_angulo.ativar(angulo)

# Calcula a potência necessária para atingir a velocidade desejada
def calcular_potencia(velocidade_desejada, direcao_desejada, temperatura):
    def funcao_objetivo(potencia):
        velocidade = calcular_velocidade(potencia, temperatura)
        return (velocidade - velocidade_desejada) ** 2
    resultado = minimize(funcao_objetivo, potencia_maxima, bounds=((0, potencia_maxima),))
    return resultado.x[0]

# Calcula o ângulo necessário para atingir a direção desejada
def calcular_angulo(velocidade, direcao_desejada, temperatura):
    direcao_atual = calcular_direcao(temperatura)
    erro_direcao = direcao_desejada - direcao_atual
    return np.clip(erro_direcao, -angulo_maximo, angulo_maximo)

# Calcula a velocidade atual com base na potência e na temperatura
def calcular_velocidade(potencia, temperatura):
    return 10 * potencia / temperatura

# Calcula a direção atual com base na temperatura
def calcular_direcao(temperatura):
    return temperatura / 10

# Encerra a comunicação com os sensores do sistema de propulsão
sensor_velocidade.close()
sensor_direcao.close()
sensor_temperatura.close()
