import time
import os
from SensorProcessing import SensorProcessing

path = os.path.abspath(os.getcwd())

sP = SensorProcessing(path,0)

print("Démarrage de la session.")
sP.startSession()

time.sleep(10)

print("Arrêt de la session.")
sP.endSession()