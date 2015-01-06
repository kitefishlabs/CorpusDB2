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

A. Data node does not know how to read its own metadata. Other nodes/classes read a dn's 
metadata and, based on that, instantiate both the metadata and data as needed.

B. Data nodes are set up to automatically read metadata and data upon creation, given that 
such data exists and that there are no overriding flags set.

Trying B first!

"""


class DataNode(object):
    """
    Single node.
    """
    def __init__(self, arg=None, metadata=None):
        self._initialize(metadata)
    
    def _initialize(self, metadata):
        """
        Initialize important parameters
        # TODO: reset()
        """
        self.metadata = self.default_metadata()
        self._check_metadata(metadata)
    
    @staticmethod
    def default_metadata():
        metadata = {
            'rootpath' : '~/comp/corpusdb2/fulltest/',
            'filename' : 'cage.wav',
            'storage' : 'np_memmap', # 'bin', 'np_memmap' || 'db'
            'dims' : []
        }
        return metadata

    def _check_metadata(self, metadata=None):
        self.metadata = metadata if metadata is not None else self.metadata
        md = self.default_metadata()
        for k in md.keys():
            self._update_metadata(k, self.metadata.get(k, md[k]))
        return self.metadata

    def _update_metadata(self, k, val):
        self.metadata[str(k)] = val
        self.__setattr__(k, self.metadata[k])
    
    def get_full_datapath_for_nodegraph(self, ngraph, mflag=False, alt=None):
        # basename, just in case?
        dir = 'data'
        if alt is not None:
            dir = str(alt)
        filename = os.path.basename(ngraph.filename)
        extstring = ngraph.available_features[ngraph.feature.__class__.__name__] # well aren't we clever
#         print 'dir: ', dir
        if mflag:
            extstring += ".json"
        # the second return val is just the expanded filename + extension
        return (
            os.path.join(
                os.path.expanduser(self.rootpath),
                dir,
                (str(filename)+extstring)),
            (str(filename)+extstring))

    def pull_to_datanode_and_save(self, nodegraph):
        nodegraph.process_wav_file()
        if self.storage is 'np_memmap':
            if self.filename is not None:
                datapath, fullfilename = self.get_full_datapath_for_nodegraph(nodegraph)
                # since there is a mechanism pass the filename on the nodegraph
                self._update_metadata('filename', fullfilename)
                fp = np.memmap(datapath, dtype=np.float32, mode='w+', shape=nodegraph.dims)
                fp[:] = np.array(nodegraph.X[:], dtype=np.float32)
                self._update_metadata('dims', list(fp.shape))
                del fp
                # now save the updated md to disk
                md_filepath, x = self.get_full_datapath_for_nodegraph(nodegraph, True)
                j = json.dumps(self.metadata, indent=4)
                f = open(md_filepath, 'w')
                print >> f, j
                f.close()
                return (1, os.path.basename(md_filepath))
            else:
                print "Error. Unable to save metadata file!"
                return (0, None)
    
    def full_path_for_filename(self):
        return os.path.join(os.path.expanduser(self.rootpath), 'data', self.filename)
    
    def load_data(self):
        fp = np.memmap(self.full_path_for_filename(), dtype=np.float32, mode='r', shape=(self.dims[0], self.dims[1]))
        res = np.array(fp)
        del fp
        return res



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
            'dir' : 'data',
            'entries': []
        }
        return metadata

    def _check_metadata(self, metadata=None):
        print "DNC"
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
            res, fullname = node.pull_to_datanode_and_save(ng)
            if res == 1:
                print "success!"
                self.metadata['entries'] += [[ng.filename, ng.feature.__class__.__name__, fullname]]
            else:
                print "failure!"
        # for now, name it 'data.json'
        md_filepath = os.path.join(os.path.expanduser(self.metadata['rootpath']), self.metadata['dir'], 'data.json')
        j = json.dumps(self.metadata, indent=4)
        f = open(md_filepath, 'w')
        print >> f, j
        f.close()

def load_any_json(jsonfile):
    json_data=open(jsonfile)
    return json.load(json_data)
