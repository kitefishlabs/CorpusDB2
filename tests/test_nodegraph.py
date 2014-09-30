import os
from corpusdb2.nodegraph import BregmanNodeGraph
import numpy as np
from bregman.features import LinearFrequencySpectrum, LogFrequencySpectrum

from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises


class TestNodeGraph(object):
    correct_filename = 'testsnd.wav'
    correct_root = '/Users/kfl/dev/git/public_projects/CorpusDB2/tests/'
    correct_sndfile = os.path.join(correct_root, 'snd', correct_filename)
    correct_ngjson = os.path.join(correct_root, 'ng', (correct_filename+'.json'))

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
        self.bng = BregmanNodeGraph(metadata={
            'rootpath':'/Users/kfl/dev/git/public_projects/CorpusDB2/tests/',
            'filename':'testsnd.wav'
        })
    
    def teardown(self):
        """This method is run once after _each_ test method is executed"""

    def test_init(self):
        assert_equal(self.bng.rootpath, TestNodeGraph.correct_root)
        assert_equal(self.bng.filename, TestNodeGraph.correct_filename)
    
    def test_read_wav(self):
        self.bng._readWavFile()
        assert_equal(self.bng.sr, 44100)
        assert_equal(self.bng.fmt, 'pcm16')
        assert_not_equal(self.bng.rawaudio, None)
    
    def test_wav_first_sample(self):
        self.bng._readWavFile()
        assert_equal(self.bng.rawaudio[0], -0.005096435546875)

    def test_analysis_read_wav(self):
        """
        Calling processWavFile should call through to readWav, exactly as above.
        """
        self.bng.processWavFile()
        assert_equal(self.bng.sr, 44100)
        assert_equal(self.bng.fmt, 'pcm16')
        assert_not_equal(self.bng.rawaudio, None)

    def test_analysis(self):
        self.bng.processWavFile()
        assert_equal(isinstance(self.bng.feature, LinearFrequencySpectrum().__class__), True)
        assert_equal(self.bng.X.shape, self.bng.dims)
        assert_equal(self.bng.X.shape, (8193, 26))        
        assert_equal(self.bng.X[0, 0], 5.9111043810844421e-05)

    def test_analysis_of_feature(self):
        self.bnglog = BregmanNodeGraph(metadata={
            'rootpath':'/Users/kfl/dev/git/public_projects/CorpusDB2/tests/',
            'filename':'testsnd.wav',
            'feature' : LogFrequencySpectrum
        })
        self.bnglog.processWavFile()
        assert_equal(isinstance(self.bnglog.feature, LogFrequencySpectrum().__class__), True)
        assert_equal(self.bnglog.X.shape, self.bnglog.dims)
        assert_equal(self.bnglog.X.shape, (95, 26))
        assert_equal(self.bnglog.X[0, 0], 6.77744419673909e-05)

