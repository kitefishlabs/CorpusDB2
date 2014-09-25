# nodegraph.py - nodegraphs
# CorpusDB2 - Corpus-based processing for audio.
"""
    Graph of Nodes.
        Nodes encapsulate audio processsing.
        1:M relationship to source file (optional).
        1:1 relationship to (potential) DataCollections.
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

class BregmanNodeGraph(object):
    """
    Based on Features class of Bregman Audio Toolkit.
    """
    sndpath = '~/dev/git/public_projects/genomicmosaic/snd/'
    audio_file = ''
    rawaudio = None
    sr = 0
    fmt = ''
    X = None
    _feature = None

    def __init__(self, arg=None, **kwargs):
        try:
            self.sndpath = kwargs['sndpath']
        except KeyError:
            print "Using default sndpath: ", os.path.expanduser(self.sndpath)
    
    def __repr__(self):
        return "%s | %s" % (self.sndpath, self.audio_file)
            
    def readWavFile(self, file):
        """
            Simply read raw audio data into class var.
        """
        self.audio_file = file
        fullpath = os.path.join(os.path.expanduser(self.sndpath), self.audio_file)
        try:
            self.rawaudio, self.sr, self.fmt = wavread(fullpath)
        except IOError:
            return "IOError! WAV read failed!"
        return self.rawaudio
    
    def processWavFile(self, wav_filename, feature=LinearFrequencySpectrum):
        self.readWavFile(wav_filename)
        if self.rawaudio is not None:
            self._feature = feature(self.rawaudio)
            self.X = self._feature.X
            self.dims = np.shape(self.X)
            return self.X, self.dims
        else:
            return None
