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
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
import json
import sys

# Pip imports
from jobject import jobject

# Local imports
from . import help, main

def cli():
	"""CLI

	Called from the command line to load a config file and run mds3

	Returns:
		uint
	"""

	# Setup the argument parser
	parser = ArgumentParser(
		formatter_class=RawDescriptionHelpFormatter,
		description=help.description,
		epilog=help.epilog
	)
	parser.add_argument('-b', '--bucket', help='The AWS S3 bucket to put the backup on')
	parser.add_argument('-c', '--config', help='The configuration file to load (default ~/.mds3)')
	parser.add_argument('-H', '--host', default='localhost', help='The hostname of the MySQL/MariaDB server (default %(default)s)')
	parser.add_argument('-k', '--key', help='The name of the key to use to store the file on S3, defaults to backup_|DATETIME|.sql[.gz]')
	parser.add_argument('-p', '--password', help='The password used to connect to the server')
	parser.add_argument('-P', '--port', default=3306, help='The port of the MySQL/MariaDB server (default %(default)s)')
	parser.add_argument('-pr', '--profile', default='mds3', help='The profile, found in ~/.aws/config, used to connect to AWS S3 (default %(default)s)')
	parser.add_argument('-u', '--user', help='The user used to connect to the server')
	parser.add_argument('-v', '--verbose', action='store_true', help='Set to display more information when backing up the database(s)')
	parser.add_argument('-z', '--zip', action='store_true', default=False, help='Use to compress (gzip) the data before storing')
	parser.add_argument('sections', metavar="N", nargs="?", help="One or more sections in the config file to run instead of setting arguments individually. e.g. %(prog)s prod_db")

	# Parse the arguments
	args = parser.parse_args()

	# If the config was not set
	conf_file = args.config or ('%s/.mds3' % Path.home())

	# Attempt to load the config file
	try:
		with open(conf_file, 'r') as oF:

			# If it's opened, decode the JSON inside and store it as a jobject
			oConf = jobject(
				json.load(oF)
			)



	except IOError as e:
		conf = jobject({})

	# Pass the JSON to the module and close with whatever status it returns
	sys.exit(
		main(oConf, args.database) == False and 1 or 0
	)

# Only run if main
if __name__ == '__main__':
	cli()