from vipy3.core import *
from vipy3.core.in_conn import InConn

#EXECUTOR IMPORTS BEGIN#
import torch
import torch.nn as nn

import collections
try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict
#EXECUTOR IMPORTS END#

class ViLinear(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

    def initialize_values(self):
        self.inputs = [ InConnInt(self,'x', 28, min=-1, max=10000),
                        InConnInt(self,'y', 28, min=-1, max=10000),
                        InConn(self,'seq',None, type='net_seq')
                        ]
        self.outputs = [ OutConn(self,'seq', 'default_executor', type='net_seq') ]

    #EXECUTOR CODE BEGIN#
    def default_executor(self, x, y, seq):
        global NET_CNTR
        if not('NET_CNTR' in globals()):
            NET_CNTR = 0
        NET_CNTR += 1

        if seq == None:
            seq = OrderedDict([])

        f = nn.Linear(x, y)

        seq.update({'linear'+str(NET_CNTR) : f})
        return seq
    #EXECUTOR CODE END#

