#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='skyrandoms',
      version='v0.1',
      author='Johnny Greco',
      author_email='jgreco@astro.princeton.edu',
      packages=['skyrandoms'],
      url='https://github.com/johnnygreco/skyrandoms',
      description='build a database of random ra & decs')
