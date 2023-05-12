# coding=utf8
""" MDTSB

Goes through the config of each requested database and creates the backup,
compresses it, and stores it on s3
"""

from __future__ import print_function

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__version__		= "1.1.0"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-05-12"

# Python imports
from time import sleep

# Local imports
from .output import color
from .version import __version__

def main(conf):
	"""Main

	Primary entry point into the script

	Arguments:
		conf (dict): The configuration for the apps to run

	Returns:
		bool
	"""

	color('magenta', 'MDTSB v%s\n' % __version__)