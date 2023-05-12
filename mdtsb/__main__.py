# coding=utf8
""" CLI

Used for shim to run the program from the command line
"""

from __future__ import print_function

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__version__		= "1.0.0"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-05-12"

# Limit exports
__all__ = [ 'cli' ]

# Python imports
from argparse import ArgumentParser
from pathlib import Path
import json
import sys

# Pip imports
from jobject import jobject

# Local imports
from . import main

def cli():
	"""CLI

	Called from the command line to load a config file and run pylivedev

	Returns:
		uint
	"""

	# Setup the argument parser
	parser = ArgumentParser(description='MySQL Dump to S3 Backup')
	parser.add_argument('-c', '--config', nargs=1, help='The configuration file to load')
	parser.add_argument('-d', '--database', nargs='+', default=['default'], help='The database to backup')

	# Parse the arguments
	args = parser.parse_args()

	# If the config was not set
	conf_file = args.config or ('%s/.mdtsb' % Path.home())

	# Attempt to load the config file
	try:
		with open(conf_file, 'r') as oF:

			# If it's opened, decode the JSON inside and store it as a jobject
			oConf = jobject(
				json.load(oF)
			)

			# Pass the JSON to the module and close with whatever status it returns
			sys.exit(
				main(oConf, args.database) == False and 1 or 0
			)

	except IOError as e:
		print(e)

# Only run if main
if __name__ == '__main__':
	cli()