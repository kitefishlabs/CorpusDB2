#!/usr/bin/env python
import glob

from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib'] 

setup(name='CorpusDB2',
      version='0.1',
      description='CorpusDB Python Toolkit',
      long_description="""This package provides tools for analyzing, manipulating, storing, retrieving, and viewing information processing operations on audio files and graphs of audio processing modules.""",
      author='Thomas M. Stoll, Kitefish Labs',      
      author_email='tms [AT] kitefishlabs [DOT] com',
      url='http://github.com/kitefishlabs/CorpusDB2',
      license='GPL v. 2.0 or higher',
      platforms=['OS X (any)', 'Linux (any)', 'Windows (any)'],
      packages=['corpusdb2'],
      data_files=[('corpusdb2/audio/', glob.glob('corpusdb2/audio/*.wav')),
                  ('corpusdb2/examples/', glob.glob('corpusdb2/examples/*.py'))]
     )
