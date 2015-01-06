# '~/comp/corpusdb2/fulltest/snd' # this is where the sounds are!

###############################################################

from corpusdb2.nodegraph import BregmanNodeGraph
from corpusdb2.datacollection import DataNode, DataNodeCollection
from bregman.features import *
import glob, itertools

ROOT = '/Users/kfl/comp/corpusdb2/fulltest'

dn = DataNode()

snds = []
for filename in glob.glob(os.path.join(ROOT,'snd','*.wav')):
    snds += [filename]

snd = os.path.basename(snds[0])

# a single node graph
myNodeGraph = BregmanNodeGraph(metadata={'rootpath':ROOT,'filename':snd,'feature':LinearFrequencySpectrum})

dn.pull_to_datanode_and_save(nodegraph=myNodeGraph)




###############################################################

from corpusdb2.nodegraph import BregmanNodeGraph
from corpusdb2.datacollection import DataNode, DataNodeCollection
from bregman.features import *
import glob, itertools

ROOT = '/Users/kfl/comp/corpusdb2/fulltest'

dc = DataNodeCollection()

snds = []
for filename in glob.glob(os.path.join(ROOT,'snd','*.wav')):
    snds += [filename]

ftrs = [LinearFrequencySpectrum, MelFrequencyCepstrum, dBPower]

# pairs of sounds and features
pairs = []
for s in snds:
    for f in ftrs:
        pairs += [[os.path.basename(s),f]]

# multiple node graphs
myNodeGraphs = [BregmanNodeGraph(metadata={'rootpath':ROOT,'filename':pair[0],'feature':pair[1]}) for pair in pairs]

# pull function for multiple nodes
dc.pull_to_datanodes_and_save(nodegraphs=myNodeGraphs)




###############################################################

from corpusdb2.nodegraph import BregmanNodeGraph
from corpusdb2.datacollection import DataNode, DataNodeCollection, load_any_json
from corpusdb2.segment import FrameSegment, Segmentation
from bregman.features import *
import os, glob, itertools

ROOT = '/Users/kfl/comp/corpusdb2/fulltest'

data = load_any_json(os.path.join(os.path.expanduser(ROOT),'data','data.json'))
entry = data['entries'][0]

segm = Segmentation(os.path.join(os.path.expanduser(ROOT),'data',entry[2]))

segm.assign_single_full_segment()

segm[0].features




###############################################################

from corpusdb2.nodegraph import BregmanNodeGraph
from corpusdb2.datacollection import DataNode, DataNodeCollection, load_any_json
from corpusdb2.segment import FrameSegment, Segmentation
from bregman.features import *
import os, glob, itertools
from pylab import plt

ROOT = '/Users/kfl/comp/corpusdb2/fulltest'

from corpusdb2.datacollection import *
data = load_any_json(os.path.join(os.path.expanduser(ROOT),'data','data.json'))
entry = data['entries'][0]

segm = Segmentation(os.path.join(os.path.expanduser(ROOT),'data',entry[2]))

segm.assign_single_full_segment()

segm[0].features

from sklearn.cluster import Ward
from scipy import sparse
from corpusdb2.segment import *

sdn = segm._datanode
x = sdn.load_data()

cm = generate_connectivity_matrix(x.shape[0])

# plot the connectivity matrix
#imagesc(cm.todense())

