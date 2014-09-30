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


class DataNode(object):
    """
    Single node.
    """
    def __init__(self, arg=None, metadata=None):
#         if arg ROOT +/+ DIR +/+ filename + ext +.json
        # check if node metadata exists
        # if so read json + init with that metadata; otherwise use defaults
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
    
    def get_full_datapath_for_nodegraph(self, ngraph, mflag=False, alt=None):
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

    def pull_to_datanode_and_save(self, nodegraph):
        nodegraph.process_wav_file()
        if self.storage is 'np_memmap':
            if self.filename is not None:
                datapath = self.get_full_datapath_for_nodegraph(nodegraph)
                # since there is a mechanism pass the filename on the nodegraph
                self.metadata['filename'] = nodegraph.filename
                fp = np.memmap(datapath, np.float32, 'w+', shape=nodegraph.dims)
                fp[:] = nodegraph.X[:]
                self.metadata['dims'] = list(fp.shape)
                del fp
                # now save the updated md to disk
                md_filepath = self.get_full_datapath_for_nodegraph(nodegraph, True)
                j = json.dumps(self.metadata, indent=4)
                f = open(md_filepath, 'w')
                print >> f, j
                f.close()
            else:
                print "Error. Unable to save metadata file!"



class DataNodeCollection(object):
    """
    Collection of nodes.
    """
    nodes = {}
    
    def __init__(self, arg=None, metadata=None):
#         if arg ROOT +/+ DIR +/+ filename + ext +.json
        # check if 
        
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
            'dir' : 'data'
        }
        return metadata

    def _check_metadata(self, metadata=None):
        self.metadata = metadata if metadata is not None else self.metadata
        md = self.default_metadata()
        for k in md.keys():
            self.metadata[k] = self.metadata.get(k, md[k])
            self.__setattr__(k, self.metadata[k])
        return self.metadata    
    
    def get_full_datapath_for_nodegraph(self, ngraph, mflag=False, alt=None):
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

    def pull_to_datanodes_and_save(self, nodegraphs):
        for ng in nodegraphs:
            node = DataNode()
            node.pull_to_datanode_and_save(ng)
#             md_filepath = self.get_full_datapath_for_nodegraph(ng, True)
#             j = json.dumps(self.metadata, indent=4)
#             f = open(md_filepath, 'w')
#             print >> f, j
#             f.close()