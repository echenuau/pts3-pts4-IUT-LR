import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class AnalogDigitalConverter:
	"""
		Class managing the analog digital converter. 
	"""

	def __init__(self,channel):
		"""
			Configure the I2C bus.

			:param channel: Channel number where the potentiometer is connected [0|1|2].
			**Authors of this class :** CHENUAUD Emmanuel and LAMBERT Vincent.\n  
		"""

		# Create the I2C bus.
		self.i2c = busio.I2C(board.SCL, board.SDA)
		# Create the ADC object using the I2C bus.
		self.adc = ADS.ADS1015(self.i2c)
		
		if(channel<0 or channel > 3):
			print("[AnalogDigitalConverter] Error, the channel can't be configured (Channel must be between 0 and 3) !")
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
		"""
			Return the ADC voltage.

			:return: float: ADC voltage (in volt).
		"""
		return self.channel.voltage
	
	def getFormattedVoltage(self):
		"""
			Return the formatted ADC voltage (x.xxx).

			:return: float: Formatted ADC voltage (in volt).
		"""
		voltage = float("{0:.3f}".format(self.getVoltageOfChannel()))
		if(voltage < 0):
			return 0. 
		else:
			return voltage