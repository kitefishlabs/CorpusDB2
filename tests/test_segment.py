from corpusdb2.segment import FrameSpan, FrameSegment, Segmentation
import numpy as np
from corpusdb2.datacollection import DataNode, DataNodeCollection
from bregman.features import LinearFrequencySpectrum

from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises


class TestSegments(object):
    @classmethod
    def setup_class(klass):
        """This method is run once for each class before any tests are run"""
        pass
            
    @classmethod
    def teardown_class(klass):
        """This method is run once for each class _after_ all tests are run"""
        pass
    
    def setUp(self):
        """This method is run once before _each_ test method is executed"""
        self.fseg = FrameSegment(0, 10)
        self.fseg2 = FrameSegment(10, dur_frames=12)
        
    def teardown(self):
        """This method is run once after _each_ test method is executed"""

    def test_segments(self):
        assert_equal(self.fseg.frame_span.start_frame, 0)
        assert_equal(self.fseg.frame_span.end_frame, 10)
        assert_equal(self.fseg.frame_span.dur_frames, 10)
        assert_equal(self.fseg2.frame_span.start_frame, 10)
        assert_equal(self.fseg2.frame_span.end_frame, 22)
        assert_equal(self.fseg2.frame_span.dur_frames, 12)
    
