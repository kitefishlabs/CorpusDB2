

from corpusdb2.nodegraph import BregmanNodeGraph
import numpy as np
from bregman.features import LinearFrequencySpectrum

from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises


class TestA(object):
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
        self.bng = BregmanNodeGraph(sndpath='/Users/kfl/dev/git/public_projects/CorpusDB2/tests')
        
    def teardown(self):
        """This method is run once after _each_ test method is executed"""

    def test_init(self):
        
        assert_equal(self.bng.sndpath, '/Users/kfl/dev/git/public_projects/CorpusDB2/tests')

    def test_read_wav(self):
        self.bng.readWavFile('testsnd.wav')
        assert_equal(self.bng.audio_file, 'testsnd.wav')
        assert_equal(self.bng.sr, 44100)
        assert_equal(self.bng.fmt, 'pcm16')
        assert_not_equal(self.bng.rawaudio, None)
    
    def test_wav_first_sample(self):
        self.bng.readWavFile('testsnd.wav')
        assert_equal(self.bng.rawaudio[0], -0.005096435546875)

    def test_analysis_read_wav(self):
        """
        Calling processWavFile should call through to readWav, exactly as above.
        """
        self.bng.processWavFile('testsnd.wav')
        assert_equal(self.bng.audio_file, 'testsnd.wav')
        assert_equal(self.bng.sr, 44100)
        assert_equal(self.bng.fmt, 'pcm16')
        assert_not_equal(self.bng.rawaudio, None)

    def test_analysis(self):
        self.bng.processWavFile('testsnd.wav')
        assert_equal(type(self.bng._feature), type(LinearFrequencySpectrum()))
        assert_equal(self.bng.X.shape, self.bng.dims)
        assert_equal(self.bng.X.shape, (8193, 26))        
        assert_equal(self.bng.X[0, 0], 5.9111043810844421e-05)

