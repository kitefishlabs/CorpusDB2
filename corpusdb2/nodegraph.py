# nodegraph.py - nodegraphs
# CorpusDB2 - Corpus-based processing for audio.
"""
    Graph of Nodes.
        Nodes encapsulate audio processsing.
        1:1 relationship to source file (optional).
        1:M relationship to (potential) DataCollections.
"""
__version__ = '1.0'
__author__ = 'Thomas Stoll'
__copyright__ = "Copyright (C) 2014 Thomas Stoll, Kitefish Labs, All Rights Reserved"
__license__ = "gpl 2.0 or higher"
__email__ = 'tms@kitefishlabs.com'

import sys, time, os, glob, pickle, pdb
import numpy as np
from bregman.suite import *
# try:
# 	have_sklearn = True
# except ImportError:
# 	print 'WARNING: sklearn not found. PCA, KMeans + Ward (hierarchical) clustering disabled.'
# 	have_sklearn = False

DEFAULT_IMAGESC_KWARGS={'origin':'upper', 'cmap':P.cm.hot, 'aspect':'auto', 'interpolation':'nearest'}

class BregmanNodeGraph:
    """
    Based on Features class of Bregman Audio Toolkit.
    """
    def __init__(self, arg=None, **kwargs):
        self.audio_file = ''
        self.rawaudio = None
        self.sr = 0
        self.fmt = ''
        self.X = None
        self._feature = None
    
    def readWavFile(self, file):
        """
            Simply read raw audio data into class var.
        """
        snd_dir = os.path.expanduser('~/dev/git/public_projects/genomicmosaic/snd/')
        self.audio_file = file
        self.rawaudio, self.sr, self.fmt = wavread(os.path.join(snd_dir, self.audio_file))
    
    def processWavFile(self, wav_filename, feature=LinearFrequencySpectrum):
        self.read_wav_file(wav_filename)
        if self.rawaudio is not None:
            self._feature = feature(self.rawaudio)
            self.X = self._feature.X
            self.dims = np.shape(self.X)
        else:
            return self.rawaudio # None
