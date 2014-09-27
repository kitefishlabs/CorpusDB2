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

"""
These are the default params for the feature extractors:
{
    'sample_rate': 44100, # The audio sample rate
    'feature':'cqft',     # Which feature to extract (automatic for Features derived classes)
    'nbpo': 12,           # Number of Bands Per Octave for front-end filterbank
    'ncoef' : 10,         # Number of cepstral coefficients to use for cepstral features
    'lcoef' : 1,          # Starting cepstral coefficient
    'lo': 62.5,           # Lowest band edge frequency of filterbank
    'hi': 16000,          # Highest band edge frequency of filterbank
    'nfft': 16384,        # FFT length for filterbank
    'wfft': 8192,         # FFT signal window length
    'nhop': 4410,         # FFT hop size
    'window' : 'hamm',    # FFT window type 
    'log10': False,       # Whether to use log output
    'magnitude': True,    # Whether to use magnitude (False=power)
    'power_ext': ".power",# File extension for power files
    'intensify' : False,  # Whether to use critical band masking in chroma extraction
    'onsets' : False,     # Whether to use onset-synchronus features
    'verbosity' : 1       # How much to tell the user about extraction
}
Expanded for BregmanNodeGraph:
{
    'sndpath': '~/dev/git/public_projects/genomicmosaic/snd/',
    'feature': 'LinearFrequencySpectrum',
    ...
    plus the above...
}

"""

class BregmanNodeGraphMetadata(object):
    
    def __init__(self, arg=None, feature_params=None, **kwargs):
        self._initialize(feature_params)

    def _initialize(self, feature_params):
        """
        Initialize important parameters
        """
        self.reset()
        self.feature_params = self.default_params()
        self._check_feature_params(feature_params)
    
    @staticmethod
    def default_params():
        feature_params = {
            'sample_rate': 44100,
            'feature':'cqft', 
            'nbpo': 12,
            'ncoef' : 10,
            'lcoef' : 1,
            'lo': 62.5, 
            'hi': 16000,
            'nfft': 16384,
            'wfft': 8192,
            'nhop': 4410,
            'window' : 'hamm',
            'log10': False,
            'magnitude': True,
            'power_ext': ".power",
            'intensify' : False,
            'onsets' : False,
            'verbosity' : 0
            }
        return feature_params

    def _check_feature_params(self,feature_params=None):
        self.feature_params = feature_params if feature_params is not None else self.feature_params
        fp = self.default_params()
        for k in fp.keys():
            self.feature_params[k] = self.feature_params.get(k, fp[k])
            self.__setattr__(k, self.feature_params[k])
        return self.feature_params

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


"""
        if type(arg)==P.ndarray:
            self.set_audio(arg, sr=self.sample_rate)
            self.extract()
        elif type(arg)==str:
            if arg:
                self.load_audio(arg) # open file as MONO signal
                self.extract()
"""