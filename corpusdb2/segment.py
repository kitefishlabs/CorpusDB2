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

import os, re, json
import numpy as np

"""
Basic containers for segments of time-based and frame-based data.
    Unexplained for now, should be fairly clear what's happening...
"""

class TimeSpan(object):   
    def __init__(self, start_time=None, end_time=None, dur_time=None):
        if start_time==None:
            raise ValueError("start_time must be provided")
        self.start_time=float(start_time)
        if end_time==None and start_time==None:
            raise ValueError("One of end_time or dur_time must be supplied")                
        self.dur_time = float(end_time) - self.start_time if dur_time is None else float(dur_time)
        self.end_time = self.start_time + float(dur_time) if end_time is None else float(end_time)
        if abs(self.end_time - self.start_time - self.dur_time)>np.finfo(np.float32).eps:
            raise ValueError("Inconistent end_time and dur_time provided")
    def __repr__(self):
        return "start_time=%.3f, end_time=%.3f, dur_time=%.3f"%(self.start_time, self.end_time, self.dur_time)

class FrameSpan(object):   
    def __init__(self, start_frame=None, end_frame=None, dur_frames=None):
        if start_frame==None:
            raise ValueError("start_frame must be provided")
        self.start_frame=float(start_frame)
        if end_frame==None and start_frame==None:
            raise ValueError("One of end_frame or dur_frames must be supplied")                
        self.dur_frames = float(end_frame) - self.start_frame if dur_frames is None else float(dur_frames)
        self.end_frame = self.start_frame + float(dur_frames) if end_frame is None else float(end_frame)
        if abs(self.end_frame - self.start_frame - self.dur_frames)>np.finfo(np.float32).eps:
            raise ValueError("Inconistent end_frame and dur_frames provided")
    def __repr__(self):
        return "start_frame=%.3f, end_frame=%.3f, dur_frames=%.3f"%(self.start_frame, self.end_frame, self.dur_frames)


class TimeSegment(object):
    def __init__(self, start_time=None, end_time=None, dur_time=None, features=None, label=''):
        self.time_span = TimeSpan(start_time, end_time, dur_time)
        self.features = [] if features is None else features
        self.label = str(label)
    def __repr__(self):
        return "(label=%s, %s, %s)"%(self.label, self.time_span.__repr__(), self.features.__repr__())

class FrameSegment(object):
    def __init__(self, start_frame=None, end_frame=None, dur_frames=None, features=None, label=''):
        self.frame_span = FrameSpan(start_frame, end_frame, dur_frames)
        self.features = [] if features is None else features
        self.label = str(label)
    def __repr__(self):
        return "(label=%s, %s, %s)"%(self.label, self.frame_span.__repr__(), self.features.__repr__())


class Segmentation(object):
    """
    A Segmentation consists of frame segments.
    Each segment has a start, end, and implicit duration in frames.
    """
    def __init__(self, datanode, metadata=None):
        if datanode is None:
            return "Error: a data node is required."
        self.data_node = datanode
        self.frame_spans = []
#         self.read_raw_data_node(self.datanode)

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
            'segpath' : '~/comp/corpusdb2/fulltest/snd/',
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

    def time_spans_to_frames(self, span_list):
        pass

    def frames_to_time_spans(self, frame_list):
        pass
    
    def __getitem__(self, index):
        return self.frame_spans[index]

    def __setitem__(self, index, segment):
        if type(segment) is not Segment:
            raise ValueError("Segmentation requires a Segment")
        self.frame_spans[index]=segment

    def __len__(self):
        return len(self.frame_spans)

    def append(self, segment):
        if type(segment) is not Segment:
            raise ValueError("Segmentation requires a Segment")
        self.frame_spans.append(segment)

    def __repr__(self):
        return self.frame_spans.__repr__()

    # for now, assume that we will get a np array
#     read_raw_data_node(self):
#         self.datanode.get_