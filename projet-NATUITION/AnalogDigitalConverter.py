import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class AnalogDigitalConverter:
    def __init__(self,channel):
        # Create the I2C bus
        self.i2c = busio.I2C(board.SCL, board.SDA)
        # Create the ADC object using the I2C bus
        self.adc = ADS.ADS1015(self.i2c)
        
        if(channel<0 or channel > 3):
            print("Error, the channel can't be configured (Channel must be between 0 and 3) !")
            return
        
        if(channel==0):
            # Create single-ended input on channel 0
            self.channel = AnalogIn(self.adc, ADS.P0)
            
        if(channel==1):
            # Create single-ended input on channel 1
            self.channel = AnalogIn(self.adc, ADS.P1)
    
        if(channel==2):
            # Create single-ended input on channel 2
            self.channel = AnalogIn(self.adc, ADS.P2)
    
        if(channel==3):
            # Create single-ended input on channel 3
            self.channel = AnalogIn(self.adc, ADS.P3)  

    def getVoltageOfChannel(self):
        return self.channel.voltage
    
    def getFormattedVoltage(self):
        voltage = float("{0:.3f}".format(self.getVoltageOfChannel()))
        if(voltage < 0):
            return 0. 
        else:
            return voltage