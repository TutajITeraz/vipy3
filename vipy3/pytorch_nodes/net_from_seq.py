from vipy3.core import *

#EXECUTOR IMPORTS BEGIN#
import torch
import torch.nn as nn
#EXECUTOR IMPORTS END#
from vipy3.core.in_conn import InConn


class ViNetFromSeq(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)
        self.default_executor_name = 'get_model'

    def initialize_values(self):
        self.inputs = [ InConn(self,'net_seq',None,type='net_seq')
                        ]
        self.outputs = [ OutConn(self,'get_params', 'get_params', type='net_params'),
                         OutConn(self,'get_model', 'get_model', type='model')]
        #functions used by other functions have to have the same name and executor


    #EXECUTOR CODE BEGIN#
    def get_model(self, net_seq):
        self.model = nn.Sequential(net_seq)
        return self.model

    def get_params(self):
        self.get_exe_result('get_model')
        return self.model.parameters()
    #EXECUTOR CODE END#