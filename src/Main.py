import time
import os
from SensorProcessing import SensorProcessing

#When the robot is turning on execute these functions
#----------------------------------
path = os.path.abspath(os.getcwd())

sP = SensorProcessing(path,0)

sP.startServer()

print("[Main] Server launch, launch client...")

os.system('bash -c "cd emulatorGPS && python MainEmulator.py; bash" &')
#time for client laaunch and connection to server for RTK coordinate
time.sleep(0.5)

print("[Main] Start of the session")
sP.startSession()
#----------------------------------



#For the demonstration 
time.sleep(2)


#Call the following functions when the robot will be shutdown
#----------------------------------
print("[Main] Termination of the session.")
sP.endSession()

sP.stopServer()
#----------------------------------
