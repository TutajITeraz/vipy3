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

class ViCrossEntropyLoss(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

    def initialize_values(self):
        self.inputs = [ ]
        self.outputs = [ OutConn(self,'loss_function', 'default_executor', type='loss_function') ]

    #EXECUTOR CODE BEGIN#
    def default_executor(self):
        return nn.CrossEntropyLoss()
    #EXECUTOR CODE END#

