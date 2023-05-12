# coding=utf8
""" Output

Output methods
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__version__		= "1.0.0"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2022-03-03"

# Limit exports
__all__ = [ 'color', 'error', 'verbose' ]

# Python imports
import sys

# Pip imports
from termcolor import colored

def color(color_, msg, eol='\n'):
	"""Color

	Prints bold messages in a specific color

	Arguments:

		arg (str): The message to print
		eol (str): The string to place at the end of the message

	Returns:
		None
	"""
	sys.stdout.write(
		colored(
			'%s%s' % (msg, eol),
			color=color_,
			attrs=['bold']
		)
	)

def error(msg, eol='\n'):
	"""Error

	Print bold red text to stderr

	Arguments:
		msg (str): The message to print
		eol (str): The string to place at the end of the message

	Returns:
		None
	"""
	sys.stderr.write(
		colored(
			'%s%s' % (msg, eol),
			color='red',
			attrs=['bold']
		)
	)

def verbose(msg, eol='\n'):
	"""Verbose

	Print bold white text to stdout

	Arguments
		msg (str): The message to print
		eol (str): The string to place at the end of the message

	Returns:
		None
	"""
	sys.stdout.write(
		colored(
			'%s%s' % (msg, eol),
			color='white',
			attrs=['bold']
		)
	)