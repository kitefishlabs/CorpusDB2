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
    
    def get_full_datapath(self, ngraph, mflag=False, alt=None):
        # basename, just in case?
        dir = 'data'
        if alt is not None:
            dir = str(alt)
        filename = os.path.basename(ngraph.filename)
        extstring = ngraph.available_features[ngraph.feature.__class__.__name__] # well aren't we clever
        if mflag:
            extstring += ".json"
        return os.path.join(
            os.path.expanduser(self.rootpath),
            dir,
            (str(filename)+extstring))
    
    def pullToDataNodesAndSave(self, nodegraphs):
        for ng in nodegraphs:
#             print ng.filename, " || ", ng.feature, " | ", type(ng.feature)
            ng.processWavFile()
            if self.storage is 'np_memmap':
                if self.filename is not None:
                    datapath = self.get_full_datapath(ng)
                    # since there is a mechanism pass the filename on the ng
                    self.metadata['filename'] = ng.filename
                    fp = np.memmap(datapath, np.float32, 'w+', shape=ng.dims)
                    fp[:] = ng.X[:]
                    self.metadata['dims'] = list(fp.shape)
                    del fp
                    # now save the updated md to disk
                    md_filepath = self.get_full_datapath(ng, True)
                    j = json.dumps(self.metadata, indent=4)
                    f = open(md_filepath, 'w')
                    print >> f, j
                    f.close()
                else:
                    print "Error. Unable to save metadata file!"
    
#     def get_raw_data_from_node(self, datanode_filename):        
#         # load the json if it exists
#         filepath = get_full_datapath()
#         ngmd = get_fulldata
#         fp = np.memmap(filepath, np.float32, 'r', shape=dnode.dims)