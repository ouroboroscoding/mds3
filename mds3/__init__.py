# coding=utf8
""" mds3

Goes through the config of each requested database and creates the backup,
zipes it, and stores it on s3
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__version__		= "1.1.0"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-05-12"

# Limit exports
__all__ = [ 'main' ]

# Python imports
from copy import copy
from datetime import datetime
from ntpath import basename
from subprocess import run
from time import time

# Pip imports
from jobject import jobject

# Local imports
from .output import color, error
from .s3 import put
from .version import __version__

# Constants
KEY_FIELDS = {
	'|TIMESTAMP|': lambda dt: int(time.time()),
	'|DATETIME|': lambda dt: dt.strftime('%Y%m%d%H%M%S'),
	'|DAYOFWEEK|': lambda dt: WEEKDAYS[dt.weekday()]
}
MYSQL_DUMP_FIELDS = {
	'host': '-h %s',
	'port': '-P %d',
	'user': '-u %s',
	'password': '-p%s',
	'options': '%s'
}
WEEKDAYS = {
	0: 'mon', 1: 'tue', 2: 'wed', 3: 'thu', 4: 'fri', 5: 'sat', 6: 'sun'
}

def main(conf, databases):
	"""Main

	Primary entry point into the script

	Arguments:
		conf (dict): The configuration for the apps to run
		databases (list): The list of databases to backup

	Returns:
		bool
	"""

	# Greet the user
	color('magenta', 'mds3 v%s' % __version__)

	# Go through each database name passed
	for db in databases:

		# Notify the user
		color('white', 'Working on `%s`' % db)

		# Does the db exist in the config?
		if db not in conf:
			error('`%s` does not exist in the given config, skipping' % db)
			continue

		# If there's a default section, merge it with the db conf
		if '__default__' in conf:
			config = copy(conf.__default__)
			config.update(conf[db])
		else:
			config = copy(conf[db])

		# If the bucket is missing
		if 'bucket' not in config:
			error('"bucket" missing from `%s`, skipping' % db)
			continue

		# If the profile is missing
		if 'profile' not in config:
			config.profile = 'default'

		# If the zip flag is missing
		if 'zip' not in config:
			config.zip = False

		# If the key is missing
		if 'key' not in config:
			config.key = 'backup_|DATETIME|.sql%s' % (
				db,
				config.zip and '.gz' or ''
			)

		# If there's no database, assume the name we are working on
		if 'databases' not in config:
			config.databases = db

		# Generate a date time
		dt = datetime.now()

		# Convert possible arguments to the key
		for k in KEY_FIELDS:
			if k in config.key:
				config.key = config.key.replace(k, KEY_FIELDS[k](dt))

		# Go through each of the possible config options
		lArgs = []
		for k in MYSQL_DUMP_FIELDS:
			if k in config:
				lArgs.append(MYSQL_DUMP_FIELDS[k] % config[k])

		# Get the basename
		file = basename(config.key)

		# Command
		command = 'mysqldump %(opts)s --databases %(dbs)s %(zip)s' % {
			'dbs': config.databases,
			'file': file,
			'opts': ' '.join(lArgs),
			'zip': ('zip' in config and config.zip) and '| gzip ' or ''
		}

		# Run the command to generate the sql data
		result = run(
			command,
			shell=True,
			capture_output=True
		)

		# Add the content to the config
		config.content = result.stdout

		# Store the file on S3
		put(config)

	# Return OK
	return True