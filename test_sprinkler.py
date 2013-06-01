# Tests for sprinkler.py
import unittest
import time
import pickle
from mock import *

# We need to mock RPi (that is used internally by 
# the sprinkler to active the pins) in order to make
# the test run.
mock = Mock()
with patch.dict('sys.modules', {'RPIO': mock, 'RPi': mock}):
	import sprinkler

	class SprinklerTest(unittest.TestCase):

		def setUp(self):
			self.sprinkler = sprinkler.Sprinkler('configuration.yaml', 5, [ 1, 2 ])

		def test_when_operate_called_setup_pid(self):
			# when
			self.sprinkler.start()
			time.sleep(0.5) # Just make sure sprinkler has read the file
			# then - we know the pid location
			_f = open('/tmp/sprinkler.pid')
			_isRunning = pickle.load(_f)
			_f.close()
			# assert
			assert _isRunning is 1

		def test_when_finished_operate_setup_pid_to_0(self):
			# when
			#self.sprinkler.start()
			time.sleep(0.5) # Just make sure sprinkler has read the file
			# then
			time.sleep(6)
			_f = open('/tmp/sprinkler.pid')
			_isRunning = pickle.load(_f)
			_f.close()
			# assert
			assert _isRunning is 0
