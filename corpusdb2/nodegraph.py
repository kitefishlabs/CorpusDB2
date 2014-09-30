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

import os, json
import numpy as np
from bregman.features import LinearFrequencySpectrum, LogFrequencySpectrum, MelFrequencySpectrum, MelFrequencyCepstrum, Chromagram, dBPower
from scikits.audiolab import wavread

# DEFAULT_IMAGESC_KWARGS={'origin':'upper', 'cmap':P.cm.hot, 'aspect':'auto', 'interpolation':'nearest'}

"""
These are the default params/metadata for the feature extractors:
{
    'rootpath' : '~/comp/corpusdb2/fulltest/',
    'filename' : 'cage.wav',
    'feature' : LinearFrequencySpectrum,
    'sr': 44100,            # The audio sample rate
    'nbpo': 12,             # Number of Bands Per Octave for front-end filterbank
    'ncoef' : 10,           # Number of cepstral coefficients to use for cepstral features
    'lcoef' : 1,            # Starting cepstral coefficient
    'lo': 62.5,             # Lowest band edge frequency of filterbank
    'hi': 16000,            # Highest band edge frequency of filterbank
    'nfft': 16384,          # FFT length for filterbank
    'wfft': 8192,           # FFT signal window length
    'nhop': 4410,           # FFT hop size
    'window' : 'hamm',      # FFT window type 
    'log10': False,         # Whether to use log output
    'magnitude': True,      # Whether to use magnitude (False=power)
    'power_ext': ".power",  # File extension for power files
    'intensify' : False,    # Whether to use critical band masking in chroma extraction
    'verbosity' : 1,        # How much to tell the user about extraction
    'available_features' : [
                LinearFrequencySpectrum, # all 6 available Bregman features
                LogFrequencySpectrum, 
                MelFrequencySpectrum, 
                MelFrequencyCepstrum,
                Chromagram,
                dBPower]
}

"""


class BregmanNodeGraph(object):
    """
    Based on Features class of Bregman Audio Toolkit.
    """
    rawaudio = None
    sr = 0
    fmt = ''
    X = None
#     _feature = None

    def __init__(self, arg=None, metadata=None):
        self._initialize(metadata)
    
    def _initialize(self, metadata):
        """
        Initialize important parameters
        """
        # TODO:
        # self.reset()
        self.metadata = self.default_metadata()
        self._check_metadata(metadata)
    
    @staticmethod
    def default_metadata():
        """ metadata == params """
        metadata = {
            'rootpath' : '~/comp/corpusdb2/fulltest/',
            'filename' : 'cage.wav',
            'feature' : LinearFrequencySpectrum,
            'sr': 44100,
            'fmt' : 'pcm16',
            'nbpo': 12,
            'ncoef' : 10,
            'lcoef' : 1,
            'lo': 62.5, 
            'hi': 16000,
            'nfft': 16384,
            'wfft': 8192,
            'nhop': 4410,
            'window' : 'hamm',
            'intensify' : False,
            'verbosity' : 0,
            'available_features' : {
                'LinearFrequencySpectrum' : '.linfreqspeq',
                'LogFrequencySpectrum' : '.logfreqspeq',
                'MelFrequencySpectrum' : '.melfreqspeq',
                'MelFrequencyCepstrum' : '.mfcc',
                'Chroma' : '.chroma',
                'dBPower' : '.dbp'
            }
        }
        return metadata

    def _check_metadata(self, metadata=None):
        self.metadata = metadata if metadata is not None else self.metadata
        md = self.default_metadata()
        for k in md.keys():
            self.metadata[k] = self.metadata.get(k, md[k])
            self.__setattr__(k, self.metadata[k])
        return self.metadata
    
    def __repr__(self):
        return "%s | %s | %s" % (self.rootpath, self.filename, self.feature)
            
    def _read_wav_file(self):
        """
            Simply read raw audio data into class var.
        """
        fullsndpath = os.path.join(os.path.expanduser(self.rootpath), 'snd', self.filename)
        try:
            self.rawaudio, self.sr, self.fmt = wavread(fullsndpath)
        except IOError:
            return "IOError! WAV read failed!"
        return self.rawaudio
    
    def get_full_ngpath(self, mflag=False, alt=None):
        # basename, just in case?
        dir = 'ng'
        if alt is not None:
            dir = str(alt)
        filename = os.path.basename(self.filename)
        extstring = self.available_features[self.feature.__class__.__name__] # well aren't we clever
#         print 'dir: ', dir
        if mflag:
            extstring += ".json"
        return os.path.join(
            os.path.expanduser(self.rootpath),
            dir,
            (str(filename)+extstring))
    
    def process_wav_file(self, filename=None, ftr=None):
        if filename is not None:
            self.metadata.filename = os.path.basename(filename)
        self._read_wav_file()
        if ftr is None:
            ftr = self.feature
        if self.rawaudio is not None:
            self.feature = ftr(self.rawaudio)
            self.X = self.feature.X
            self.dims = np.shape(self.X)
            extstring = self.available_features[self.feature.__class__.__name__] # well aren't we clever
            md_filepath = self.get_full_ngpath(mflag=True)
            clean_md = self.metadata
            clean_md['feature'] = clean_md['feature'].__name__
            j = json.dumps(self.metadata, indent=4)
            f = open(md_filepath, 'w')
            print >> f, j
            f.close()
            return self.X, self.dims
        else:
            return None
        

"""
        if type(arg)==P.ndarray:
            self.set_audio(arg, sr=self.sr)
            self.extract()
        elif type(arg)==str:
            if arg:
                self.load_audio(arg) # open file as MONO signal
                self.extract()
"""