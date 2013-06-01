
import time
import datetime
import json
import sys
import logging
import logging.config

"""
Checks that current system date matches any 
dates from input file. If so, trigger the 
python runner script.
"""
class SprinklerTimeCheck:
	def __init__(self, file):
		# Read file contents
		fileContents = open(file)
		# Load the json structure
		_json = json.load(fileContents)
		self._readSchedules(_json)

		fileContents.close()

		# And finally check if any of
		# the schedules apply
		self.checkAvailableSprinklers()


	def _readSchedules(self, json):
		# Read the default configuration
		default = json["default"]

		logging.info('Going through %d sprinkler configuration(s)' % len(default["schedules"]))

		schedules = []
		for s in default["schedules"]:
			schedules.append(SprinklerStartStop(s["pinNumbers"], s["start"], s["duration"]))

		self.schedules = schedules

	"""
	Checks if any of the sprinkler schedules
	can be applied. This method will match only
	the first sprinkler, then stop.
	"""
	def checkAvailableSprinklers(self):
		now = time.localtime()
		nowDate = datetime.datetime(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
		midnight = datetime.datetime(now.tm_year, now.tm_mon, now.tm_mday, 0, 0, 0)
		secondsPastMidnight = (nowDate - midnight).seconds

		for s in self.schedules:
			# Check each sprinkler.
			if (s.canMatchCurrentSecondsPastMidnight(secondsPastMidnight)):
				# found a match
				logging.info('Found sprinkler')
			else:
				logging.debug('Sprinkler %d-%d did not match current seconds past midnight %d' % (s.start, s.start + s.duration, secondsPastMidnight))




class SprinklerStartStop:
	def __init__(self, pinsArray, start, duration):
		# calculate current time and
		# midnight.
		self.start = start
		self.duration = duration
		self.pinsArray = pinsArray

	def canMatchCurrentSecondsPastMidnight(self, secondsPastMidnight):
		return (self.start < secondsPastMidnight) and (self.start + self.duration) > secondsPastMidnight

def main(args):
	if (len(args) == 0):
		print('Usage: python check_time.py <jsonFile>')
		sys.exit(2)

	# Configure logger
	logging.config.fileConfig('logger.conf')

	SprinklerTimeCheck(args[0])

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
	main(sys.argv[1:])				