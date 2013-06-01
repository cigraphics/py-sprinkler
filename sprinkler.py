import logging
import time
import yaml

try:
	import RPi.GPIO as gpio
except ImportError:
	print("Error importing RPi.GPIO; you are either running the script without sudo priviledges, or running the script on a machine that is not Raspberry (the lib is missing nevertheless)")

"""
Runner for sprinklers.
"""
class Sprinkler:
	defaultConfigurationFile = 'configuration.yaml'

	"""
	Delegates to the second constructor with default 
	configuration.
	"""
	def __init__(self):
		self.__init__(defaultConfigurationFile)

	def __init__(self, configurationFile, duration, pinConfiguration):
		self.configurationFile = configurationFile
		self.duration = duration
		self.pinConfiguration = pinConfiguration

		self._setup()

	def _setup(self):
		# Read configuration file. We're interested in
		# 'pidFile' and 'logMultipleRuns'
		_config = open(self.configurationFile)
		_map = yaml.safe_load(_config)
		_config.close()

		self.pinFile = _map["configFile"]
		self.logMultipleRuns = _map["logMultipleRuns"]
		if (self.pidFile is None):
			raise "Missing pidFile in configuration"
		if (self.logMultipleRuns is None):
			self.logMultipleRuns = False

		# configure gpio mode
		gpio.setmode(gpio.BOARD)
		for pin in self.pinConfiguration:
			try:
				gpio.setup(pin, gpio.OUT)
			except gpio.InvalidChannelException:
				logging.error('Unable to configure pin %d', pin)

	def operate(self):
		# Read the pid file. The sprinkler will only
		# run if it not currently running.
		_f = open(self.pidFile)
		_isRunning = int(_f.read())
		if (_isRunning is True):
			logging.warn('Sprinkler is already running.')
			return
		else:
			_f.write("1")
		_f.close()

		# Set the pin to high and sleep for given
		# number of seconds
		for pin in self.pinConfiguration:
			gpio.output(pin, gpio.HIGH)

		# sleep
		time.sleep(self.duration)

		for pin in self.pinConfiguration:
			gpio.output(pin, gpio.LOW)

		_f = open(self.pidFile)
		_f.write("0")
		_f.close()
