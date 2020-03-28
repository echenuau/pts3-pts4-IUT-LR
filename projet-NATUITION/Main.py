import time
import os
from SensorProcessing import SensorProcessing

path = os.path.abspath(os.getcwd())

sP = SensorProcessing(path,0)

sP.startServer()

print("[Main] Server launch, launch client...")

time.sleep(1)

os.system('gnome-terminal -- bash -c "cd emulatorGPS && python MainEmulator.py; bash"')

time.sleep(1)

print("[Main] Start of the session")
sP.startSession()

time.sleep(10)

print("[Main] Termination of the session.")
sP.endSession()

sP.stopServer()