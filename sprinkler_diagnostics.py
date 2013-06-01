import time
import datetime
import json
import sys
import logging
import logging.config

import sprinkler

def main(args):
	if (len(args) < 3):
		print('Usage: python sprinkler_diagnostics.py <logger configuration file> <jsonFile> <pin>')
		sys.exit(2)

	# Configure logger
	logging.config.fileConfig(args[0])

	fileContents = open(args[1])
	# Load the json structure
	_json = json.load(fileContents)
	configurationFile = _json["configurationFile"]
	fileContents.close()

	# Start a sprinkler for 60 seconds, for the provided pin
	sprinkler.Sprinkler(args[1], configurationFile, 60, [ int(args[2]) ])

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
	main(sys.argv[1:])				