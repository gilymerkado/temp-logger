import serial
import csv
from time import localtime
import threading

class TempListen(threading.Thread):
	'''Listener to the temperature data from the serial port.'''
	def __init__(self):
		threading.Thread.__init__(self)
		try:
			self.ser = serial.Serial('/dev/ttyUSB0', 9600)
		except OSError:
			print('Could not find a serial device.')
		self.file_location = './'
		self.log_file = 'temp_data.csv'
		self.listenning = False
		self.temp_read = None
		
	def createLogFile(self, location, datetime_stamp):
	    """Create a csv file with the temperature data."""
	    self.file_name = 'temp_data'
	    self.location = './'
	    with open(location + datetime_stamp + '.log.csv', 'wb') as f:
			self.head = [['time', 'temperature']]
			csv.writer(f).writerows(self.head)
	
	def updateFile(self, log, log_file, file_location):
		'''Add a new row to the log file'''
		print(log)
		with open(file_location + log_file, 'ab') as f:
			writer = csv.writer(f)
			writer.writerow(log)
		
	def recordLine(self):
		'''Listen to temperature data from the serial port, save to a 
		log file (csv) and return as a list:
		return log = [datetime_stamp, temperature]
		'''
		self.datetime_stamp = '%4d-%02d-%02dT%02d-%02d-%02d' % (localtime()[:6])
		try:
			print('listenLine: ' + self.ser.readline()) ## debuging, should be removed.
			#self.log = [self.datetime_stamp, self.ser.readline()]
			self.log = [1, float(self.ser.readline())]
			#self.updateFile(self.log, self.log_file, self.file_location)
			self.temp_read = self.log
			
		except:
			print('Could not read serial device')
			self.temp_read = None
	
	def run(self):
		while True:
			if self.listenning:
				print('thread is listenning')
				self.recordLine()
	
