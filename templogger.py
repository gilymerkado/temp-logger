#!usr/bin/python3

from gi.repository import Gtk
from gi.repository import GObject

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.dates import date2num, DateFormatter

import time
import threading
from time import localtime
import serial
from datetime import datetime
import csv

from send_email import sendEmailAlert
	
class GraphWindow:
	def __init__(self, log_no):
		try:
			self.ser = serial.Serial('/dev/ttyUSB0', 9600)
		except OSError:
			print('Could not find a serial device.')
		
		# Log number
		self.log_no = log_no
		print('Starting log ', log_no)
		
		self.fig = Figure(figsize=(10, 10), dpi=80)
		self.fig.suptitle('Log ' + str(self.log_no))
		self.ax = self.fig.add_subplot(111)
		self.canvas = FigureCanvas(self.fig)
		
		self.liststore = Gtk.ListStore(str, float)
		self.treeview = Gtk.TreeView(model = self.liststore)
		
		self.xrenderer = Gtk.CellRendererText()
		self.xrenderer.set_property("editable", True)
		self.xcolumn = Gtk.TreeViewColumn("Time", self.xrenderer, text=0)
		self.xcolumn.set_min_width(100)
		self.xcolumn.set_alignment(0.5)
		self.treeview.append_column(self.xcolumn)
		
		self.yrenderer = Gtk.CellRendererText()
		self.yrenderer.set_property("editable", True)
		self.ycolumn = Gtk.TreeViewColumn("Temperature", self.yrenderer, text=1)
		self.ycolumn.set_min_width(100)
		self.ycolumn.set_alignment(0.5)
		self.treeview.append_column(self.ycolumn)
		
		self.xrenderer.connect("edited", self.xedited)
		self.yrenderer.connect("edited", self.yedited)
		
		self.listenning = True
		
		self.log_file = 'temp_data' + str(self.log_no) + '.csv'
		self.file_location = './'
		self.log = [None, None]
		
	def xedited(self, widget, path, number):
		self.liststore[path][0] = str(number.replace(',', '.'))
		self.plotpoints()
	
	def yedited(self, widget, path, number):
		self.liststore[path][1] = float(number.replace(',', '.'))
		self.plotpoints()
	
	def resetplot(self):
		self.ax.cla()
		self.ax.set_xlim(date2num(datetime.now()) - 0.001, date2num(datetime.now()))
		self.ax.set_ylim(10, 40)
		self.ax.grid(True)

	def plotpoints(self):
		self.resetplot()
		for row in self.liststore:
			#self.ax.scatter(row[0], row[1], marker='o', s=50)
			self.ax.plot_date(datetime.strptime(row[0][0:19], '%Y-%m-%d %H:%M:%S'), 
			row[1], 'bo')
		self.fig.autofmt_xdate()
		self.fig.canvas.draw()
	
	#def record(self):
		##temp_read = self.listener.recordLine()
		#self.listener.listenning = True
		#temp_read = self.listener.temp_read
		#print('Log ' + str(self.log_no) + 'record: ' + str(temp_read))
		#self.liststore.append(temp_read)
		#self.plotpoints()
	
	def recordLine(self):
		'''Listen to temperature data from the serial port, save to a 
		log file (csv) and return as a list:
		return log = [datetime_stamp, temperature]
		'''
		try:
			n = 0
			while n < 5:
				# Record temp from the defined log number
				row = self.ser.readline()
				logger = row.split(' ')[0]
				temp = row.split(' ')[1]
				if int(logger) == self.log_no:
					print('row ', str(self.log_no), row)
					date_num = date2num(datetime.now())
					self.log = [str(datetime.now()), float(temp)]
					#self.temp_read = self.log
					self.liststore.append(self.log)
					self.plotpoints()
					# Send email alert
					if temp > 5:
						sendEmailAlert(self.log_no, temp)
				row = None
				temp = None
				n += 1
				while Gtk.events_pending():
					Gtk.main_iteration()  # runs the GTK main loop as needed
				
		except:
			print('Could not read serial device')
			self.temp_read = None
		return True
	
	def updateFile(self):
		'''Add a new row to the log file'''
		if self.listenning == True:
			print(self.log)
			with open(self.file_location + self.log_file, 'ab') as f:
				writer = csv.writer(f)
				writer.writerow(self.log)
			return True
		
class Signals():
	def on_quit_menu_activate(self, widget):
		Gtk.main_quit()
	
	def on_window1_destroy(self, widget):
		Gtk.main_quit()
		
	def start_record_button_clicked(self, widget):
		self.on_menu_new_activate(self, 1)
		self.on_menu_new_activate(self, 2)
		self.on_menu_new_activate(self, 3)
		self.on_menu_new_activate(self, 4)
		self.on_menu_new_activate(self, 5)
	
	def on_menu_new_activate(self, widget, log_no):
		self.new_win_builder = Gtk.Builder()
		self.new_win_builder.add_objects_from_file('templogger.glade', ('window1', 'mainwindow', 'adjustment1'))
		self.new_win_builder.connect_signals(Signals())
		self.points = GraphWindow(log_no)
		self.myfirstwindow = self.new_win_builder.get_object('window1')
		self.sw1 = self.new_win_builder.get_object('scrolledwindow1')
		self.sw2 = self.new_win_builder.get_object('scrolledwindow2')
		statbar = self.new_win_builder.get_object('toolbar2')
		self.sw1.add_with_viewport(self.points.canvas)
		self.sw2.add_with_viewport(self.points.treeview)

		self.points.resetplot()
		self.points.plotpoints()
		
		self.points.listenning = True
		GObject.timeout_add(2000, self.points.recordLine)
		GObject.timeout_add(2000, self.points.updateFile)
		self.myfirstwindow.show_all()


builder = Gtk.Builder()
builder.add_objects_from_file('templogger.glade', ('window1', 'mainwindow', 'adjustment1'))
builder.connect_signals(Signals())

mainwindow = builder.get_object('mainwindow')
mainwindow.show_all()

#myfirstwindow.show_all()
Gtk.main()
