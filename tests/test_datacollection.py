from corpusdb2.datacollection import DataCollection
import numpy as np
from bregman.features import LinearFrequencySpectrum

from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises


class TestDataCollection(object):
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
        self.dc = DataCollection(metadata={'sndpath':'~/comp/corpusdb2/fulltest/snd/'})
        
    def teardown(self):
        """This method is run once after _each_ test method is executed"""

    def test_init(self):
        assert_equal(self.dc.sndpath, '~/comp/corpusdb2/fulltest/snd/')
    
