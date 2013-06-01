import logging
import time
import yaml
import threading
import pickle

#try:
import RPi
#except ImportError:
#	print("Error importing RPi.GPIO; you are either running the script without sudo priviledges, or running the script on a machine that is not Raspberry (the lib is missing nevertheless)")

"""
Runner for sprinklers.
"""
class Sprinkler(threading.Thread):

	def __init__(self, configurationFile, duration, pinConfiguration):

		super(Sprinkler, self).__init__()
		self.configurationFile = configurationFile
		self.duration = duration
		self.pinConfiguration = pinConfiguration

		self._setup()
		self.daemon = True

	def _setup(self):
		# Read configuration file. We're interested in
		# 'pidFile' and 'logMultipleRuns'
		_config = open(self.configurationFile)
		_map = yaml.safe_load(_config)
		_config.close()

		try:
			self.pidFile = _map["pidFile"]
		except KeyError:
			raise "Missing pidFile in configuration"
		try:
			self.logMultipleRuns = _map["logMultipleRuns"]
		except KeyError:
			self.logMultipleRuns = False			

		# configure gpio mode
		RPi.GPIO.setmode(RPi.GPIO.BOARD)
		for pin in self.pinConfiguration:
			try:
				RPi.GPIO.setup(pin, RPi.GPIO.OUT)
			except gpio.InvalidChannelException:
				logging.error('Unable to configure pin %d', pin)

	def run(self):
		# Read the pid file. The sprinkler will only
		# run if it not currently running.
		_isRunning = self._readPid()
		if (_isRunning is 1):
			logging.warn('Sprinkler is already running.')
			return
		else:
			logging.debug('Write pidFile with 1')
			self._writePid(1)

		# Set the pin to high and sleep for given
		# number of seconds
		for pin in self.pinConfiguration:
			RPi.GPIO.output(pin, RPi.GPIO.HIGH)

		# sleep
		time.sleep(self.duration)

		for pin in self.pinConfiguration:
			RPi.GPIO.output(pin, RPi.GPIO.LOW)

		logging.info('Finished sprinkler job')
		self._writePid(0)

	def _readPid(self):
		try:
			_f = open(self.pidFile)
			pid = pickle.load(_f)
			_f.close()
			return pid
		except IOError:
			# File does not exist yet, so we have no pid
			return 0


	def _writePid(self, isRunning):
		_f = open(self.pidFile, "w")
		pickle.dump(isRunning, _f)
		_f.close()