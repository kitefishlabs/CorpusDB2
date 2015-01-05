# segment.py - Spans, Segments and Segmentations
# CorpusDB2 - Corpus-based processing for audio.
"""
    Basic containers for segments of time-based and frame-based data.
    Unexplained for now, should be fairly clear what's happening...
"""
__version__ = '1.0'
__author__ = 'Thomas Stoll'
__copyright__ = "Copyright (C) 2014 Thomas Stoll, Kitefish Labs, All Rights Reserved"
__license__ = "gpl 2.0 or higher"
__email__ = 'tms@kitefishlabs.com'

import os, re, json
import numpy as np
from corpusdb2.datacollection import DataNode

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
        if start_frame < 0:
            raise ValueError("Start frame must be positive.")
        if dur_frames is not None and dur_frames < 1:
            raise ValueError("dur_frames/end_frames should be greater than 0.")
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
    
    def mean(self):
        return np.mean(self.features, 0)
    def var(self):
        return np.var(self.features, 0)

    def logmean(self):
        return np.log(np.mean(self.features, 0))
    def logvar(self):
        return np.log(np.var(self.features, 0))
    

class Segmentation(object):
    """
    A Segmentation consists of frame segments.
    Each segment has a start, end, and implicit duration in frames.
    """
    def __init__(self, dnodepath, metadata=None):
        if dnodepath is None:
            return "Error: a data node JSON metadata path is required."
        self._initialize(metadata)
        self._datanode = None
        self.frame_spans = []
        self.read_datanode_json(dnodepath)

    def _initialize(self, metadata):
        """
        Initialize + check metadata.
        """
        # TODO:
        # self.reset()
        self.metadata = self.default_metadata()
        self._check_metadata(metadata)
    
    @staticmethod
    def default_metadata():
        """
        	These entries are provisional and should be available for checking later whether the analysis has been done.
        """
        metadata = {
            'rootpath' : '~/comp/corpusdb2/fulltest/',
            'dir' : 'seg',
            'datanode' : '',
            'overlap' : 0,
            'frames' : -1,
            'cols' : -1,
            'duration' : -1
        }
        return metadata

    def _check_metadata(self, metadata=None):
        self.metadata = metadata if metadata is not None else self.metadata
        md = self.default_metadata()
        for k in md.keys():
            self._update_metadata(k, self.metadata.get(k, md[k]))
        return self.metadata

    def _update_metadata(self, k, val):
        print '_update'
        self.metadata[str(k)] = val
        self.__setattr__(k, self.metadata[k])
    
    def read_datanode_json(self, dnodepath):
        # check path???
        print dnodepath
        self._datanode = DataNode(metadata=load_any_json(str(dnodepath)))
        print self._datanode
        if int(self._datanode.dims[1]) is None:
            # first dim is # of frames
            self._update_metadata('cols', 1)
            self._update_metadata('frames', int(self._datanode.dims[1]))
        else:
            self._update_metadata('cols', int(self._datanode.dims[0]))
            self._update_metadata('frames', int(self._datanode.dims[1]))
            

#     def get_full_segpath(self, data_md, mflag=False, alt=None):
#         # basename, just in case?
#         dir = 'seg'
#         if alt is not None:
#             dir = str(alt)
#         filename = os.path.basename(self.filename)
#         extstring = self.available_features[self.feature.__class__.__name__] # well aren't we clever
# #         print 'dir: ', dir
#         if mflag:
#             extstring += ".json"
#         return os.path.join(
#             os.path.expanduser(self.rootpath),
#             dir,
#             (str(filename)+extstring))

    def time_spans_to_frames(self, span_list):
        pass

    def frames_to_time_spans(self, frame_list):
        pass
    
    def __getitem__(self, index):
        return self.frame_spans[index]

    def __setitem__(self, index, segment):
        self.check_segment_data(segment)
        self.frame_spans[index]=segment
    
    def __delitem__(self, index):
        if self.frame_spans[index] is not None:
            del self.frame_spans[index]
        else:
            raise IndexError("Attempting to delete an item that does not exist.")

    def __len__(self):
        return len(self.frame_spans)

    def check_segment_data(self, segment):
    	""" Only accept FrameSegments (for now). """
        if type(segment) is not FrameSegment:
            raise ValueError("Segmentation requires a Segment")
    
    # do all error- and logic-checking in caller, for now...
    def append(self, segment):
    	""" Append a FrameSegment and return the size + resulting frame spans. """
    	# check that segment data is a FrameSegment type
        self.check_segment_data(segment)
        self.frame_spans.append(segment)
        return (len(self.frame_spans), self.frame_spans)

    def assign_single_full_segment(self):
    	""" Map all frames from an audio file to a single segment. """
        self.append(FrameSegment(0,self.frames, features=self._datanode.load_data()))
        return self
    
    def assign_segments_by_hierarchical_clustering(self):
        pass
    
    def __repr__(self):
        return self.frame_spans.__repr__()

    # for now, assume that we will get a np array
#     read_raw_data_node(self):
#         self.datanode.get_

def load_any_json(jsonfile):
    json_data=open(jsonfile)
    return json.load(json_data)

from scipy import sparse

def generate_connectivity_matrix(size, loop_flag=False):
		"""
		Generate a square connectivity matrix with positive connections from t -> t-1 (identity) and t -> t+1; link end to beginning if loop_flag is True.
		Returns a sparse 
		"""
		eye = np.identity(size, dtype=np.int8)
		nn1 = np.add( np.roll(eye, 1, axis=0), np.roll(eye, 1, axis=1))
		
		if not loop_flag:
			nn1[-1,0] = 0
			nn1[0,-1] = 0
		#print nn1[:30,:30]
		return sparse.csr_matrix(nn1)

