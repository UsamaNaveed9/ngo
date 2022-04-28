# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in ngo/__init__.py
from ngo import __version__ as version

setup(
	name='ngo',
	version=version,
	description='ngo',
	author='smb',
	author_email='usamanaveed9263',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
