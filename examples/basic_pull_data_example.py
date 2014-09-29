# '~/comp/corpusdb2/fulltest/snd' # this is where the sounds are!

from corpusdb2.nodegraph import BregmanNodeGraph
from corpusdb2.datacollection import DataCollection
from bregman.features import *
import glob, itertools



dc = DataCollection()

snds = []
for filename in glob.glob('/Users/kfl/comp/corpusdb2/fulltest/snd/*.wav'):
    snds += [filename]

ftrs = [LinearFrequencySpectrum, MelFrequencyCepstrum, dBPower]

pairs = []
for s in snds:
    for f in ftrs:
        pairs += [[s,f]]

myNodeGraphs = [BregmanNodeGraph(metadata={'sndpath':pair[0],'feature':pair[1]}) for pair in pairs]


dc.pullToDataNodesAndSave(nodegraphs=myNodeGraphs)


