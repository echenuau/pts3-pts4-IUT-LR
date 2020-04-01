from Server import Server
import threading
import time

server = Server(4010)
server.start()
time.sleep(30)
server.exit()