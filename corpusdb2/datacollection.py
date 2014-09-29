# datacollection.py - DataNodes and DataNodeCollections
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

"""
These are the default metadata for a data node:
{
    'sndpath' : '~/dev/git/public_projects/genomicmosaic/snd/testsnd.wav',
    'feature' : 'LinearFrequencySpectrum',
    'storage' : 'np_memmap', # 'bin', 'np_memmap' || 'db'
    'nodegraph_metadata' : '', # init empty
    'sndfile_metadata' : '', # init empty
    'exists' : {
        'sndfile' : 0,
        'sndfile_metadata' : 0,
        'nodegraph_metadata' : 0,
        'data' : 0
    }
}

"""


class DataCollection(object):
    """
    Based on Features class of Bregman Audio Toolkit.
    """
    _features = None

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
            'sndpath' : '~/comp/corpusdb2/snd/',
            'datapath' : '~/comp/corpusdb2/data/',
            'metadatapath' : '~/comp/corpusdb2/md/',
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
    
    
    def pullToDataNodesAndSave(self, sounds, nodegraphs):
        for snd in sounds:
            fullpath=os.path.join(os.path.expanduser(self.sndpath), snd)
            for ng in nodegraphs:
                ng.processWavFile()
                if self.storage is 'np_memmap':
                    # construct file name
                    extstring = ng.metadata.available_features[ng.feature.__name__]
                    filename = os.path.join(
                        os.path.expanduser(self.datapath), 
                        (str(snd)+extstring))
                    self.X = np.memmap(filename, nodegraph.X)
                    self.X.flush()

        
        