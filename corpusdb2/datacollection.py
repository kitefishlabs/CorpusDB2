# datacollection.py - DataNodes and DataNodeCollections
# CorpusDB2 - Corpus-based processing for audio.
"""
    Data Collection.
        Encapsulates raw analysis data.
        1:M relationship to source file (optional).
        1:1 relationship to (potential) DataCollections.
"""
__version__ = '1.0'
__author__ = 'Thomas Stoll'
__copyright__ = "Copyright (C) 2014 Thomas Stoll, Kitefish Labs, All Rights Reserved"
__license__ = "gpl 2.0 or higher"
__email__ = 'tms@kitefishlabs.com'

import os, re, json
import numpy as np
from bregman.features import LinearFrequencySpectrum, LogFrequencySpectrum, MelFrequencySpectrum, MelFrequencyCepstrum, Chromagram, dBPower

"""
These are the default metadata for a data node:
{
    'sndpath' : '~/comp/corpusdb2/fulltest/snd/',
    'datapath' : '~/comp/corpusdb2/fulltest/data/',
    'metadatapath' : '~/comp/corpusdb2/fulltest/md/',
    'storage' : 'np_memmap', # 'bin', 'np_memmap' || 'db'
}

"""


class DataCollection(object):
    """
    Based on Features class of Bregman Audio Toolkit.
    """
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
        """ These entries should  """
        metadata = {
            'sndpath' : '~/comp/corpusdb2/fulltest/snd/',
            'datapath' : '~/comp/corpusdb2/fulltest/data/',
            'metadatapath' : '~/comp/corpusdb2/fulltest/md/',
            'storage' : 'np_memmap', # 'bin', 'np_memmap' || 'db'
        }
        return metadata

    def _check_metadata(self, metadata=None):
        self.metadata = metadata if metadata is not None else self.metadata
        md = self.default_metadata()
        for k in md.keys():
            self.metadata[k] = self.metadata.get(k, md[k])
            self.__setattr__(k, self.metadata[k])
        return self.metadata    
    
    def pullToDataNodesAndSave(self, nodegraphs):
        for ng in nodegraphs:
            print ng.feature, " | ", type(ng.feature)
            ng.processWavFile(ng.sndpath, ng.feature)
            print ng.X.shape
            if self.storage is 'np_memmap':
                # construct file name
                filename = os.path.basename(ng.sndpath)
                extstring = ng.available_features[ng.feature.__class__.__name__] # well aren't we clever
                if self.datapath is not None and self.metadatapath is not None:
                    filepath = os.path.join(
                        os.path.expanduser(self.datapath),
                        (str(filename)+extstring))
                    fp = np.memmap(filepath, np.float32, 'w+', shape=ng.dims)
                    fp[:] = ng.X[:]
                    del fp
                    md_filepath = os.path.join(
                        os.path.expanduser(self.metadatapath),
                        (str(filename)+extstring+".json"))
                    j = json.dumps(self.metadata, indent=4)
                    f = open(md_filepath, 'w')
                    print >> f, j
                    f.close()
                else:
                    print "Error. Unable to save metadata file!"
                