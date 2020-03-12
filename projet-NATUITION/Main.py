import time
from SensorProcessing import SensorProcessing
from AnalogDigitalConverter import AnalogDigitalConverter

adc0 = AnalogDigitalConverter(0)

sP = SensorProcessing("/home/pi/Desktop/sensor",adc0)

print("Démarrage de la session.")
sP.startSession()

time.sleep(100000)

print("Arrêt de la session.")
sP.endSession()