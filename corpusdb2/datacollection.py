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
    'rootpath' : '~/comp/corpusdb2/fulltest/',
    'filename' : 'cage.wav',
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
            'rootpath' : '~/comp/corpusdb2/fulltest/',
            'filename' : 'cage.wav',
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
#             print ng.filename, " || ", ng.feature, " | ", type(ng.feature)
            ng.processWavFile()
            if self.storage is 'np_memmap':
                # basename, just in case?
                filename = os.path.basename(ng.filename)
                extstring = ng.available_features[ng.feature.__class__.__name__] # well aren't we clever
                if self.filename is not None:
                    datapath = os.path.join(
                        os.path.expanduser(self.rootpath),
                        'data',
                        (str(filename)+extstring))
                    fp = np.memmap(datapath, np.float32, 'w+', shape=ng.dims)
                    fp[:] = ng.X[:]
                    del fp
                    md_filepath = os.path.join(
                        os.path.expanduser(self.rootpath),
                        'data',
                        (str(filename)+extstring+".json"))
                    j = json.dumps(self.metadata, indent=4)
                    f = open(md_filepath, 'w')
                    print >> f, j
                    f.close()
                else:
                    print "Error. Unable to save metadata file!"
    
#     def get_raw_data_from_node(self, datanode_filename):
#         
#         filepath = '~/comp/corpusdb2/fulltest/dnodes/' + datanode_filename
#         datanode_md = '~/comp/corpusdb2/fulltest/dnodes/' + datanode_filename
#         fp = np.memmap(filepath, np.float32, 'r', shape=dnode.dims)