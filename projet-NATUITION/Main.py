import time
import os
from SensorProcessing import SensorProcessing
from AnalogDigitalConverter import AnalogDigitalConverter

adc0 = AnalogDigitalConverter(0)


path = os.path.abspath(os.getcwd())

sP = SensorProcessing(path,adc0)

print("Démarrage de la session.")
sP.startSession()

time.sleep(10)

print("Arrêt de la session.")
sP.endSession()