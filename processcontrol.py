import serial
import cv2


sensor_temperatura = serial.Serial('COM1', 9600)


temperatura = float(sensor_temperatura.readline().decode())


camera = cv2.VideoCapture(0)

class AtuadorVentilacao:
    def __init__(self):
        # comunicação com o sistema de ventilação
        self.comunicacao = serial.Serial('COM2', 9600)
        
    def ativar(self):
       
        self.comunicacao.write(b'ON')
        
    def desativar(self):
       
        self.comunicacao.write(b'OFF')

atuador_ventilacao = AtuadorVentilacao()

while True:
    ret, frame = camera.read()
    cv2.imshow('Processo de pintura', frame)
    if temperatura > 30:
        atuador_ventilacao.ativar()
    else:
        atuador_ventilacao.desativar()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


sensor_temperatura.close()
camera.release()
cv2.destroyAllWindows()