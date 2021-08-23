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

class ViOptimizer(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

    def initialize_values(self):
        self.inputs = [ InConnPercent(self,'lr',0.01),
                        InConn(self,'params',None,type='net_params')
                        ]
        self.outputs = [ OutConn(self,'optimizer', 'default_executor', type='net_optimizer') ]

    #EXECUTOR CODE BEGIN#
    def default_executor(self, params, lr):
        return torch.optim.SGD(params, lr)
    #EXECUTOR CODE END#

