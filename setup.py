# Python imports
from setuptools import setup, find_packages
from distutils.util import convert_path

# Shared long description
with open('README.md', 'r') as oF:
	long_description=oF.read()

# Shared version
with open(convert_path('mdtsb/version.py')) as oF:
	d = {}
	exec(oF.read(), d)
	version = d['__version__']

setup(
	name='mdtsb',
	version=version,
	description='MySQL Dump to S3 Backup',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://ouroboroscoding.com/mdtsb',
	project_urls={
		'Source': 'https://github.com/ouroboroscoding/mdtsb',
		'Tracker': 'https://github.com/ouroboroscoding/mdtsb/issues'
	},
	keywords=['mysql','backup', 's3', 'aws'],
	author='Chris Nasr - OuroborosCoding',
	author_email='chris@ouroboroscoding.com',
	license='MIT',
	packages=['mdtsb'],
	install_requires=[
		'termcolor>=1.1.0'
	],
	entry_points={
		'console_scripts': ['mdtsb=mdtsb.__main__:cli']
	},
	zip_safe=True
)