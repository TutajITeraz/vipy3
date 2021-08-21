from vipy3.core import *
from vipy3.core.in_conn import InConn

#EXECUTOR IMPORTS BEGIN#
import torch
from torch.utils.data.sampler import SubsetRandomSampler
#EXECUTOR IMPORTS END#

class ViDataLoader(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

    def initialize_values(self):
        self.inputs = [ InConnInt(self,'batch_size', 20),
                        InConnInt(self,'num_workers', 0),
                        InConn(self,'data',None, type='tensor'),
                        InConn(self,'sampler',None, type='datasampler')
                        ]
        self.outputs = [ OutConn(self,'data', 'default_executor', type='tensor') ]

    #EXECUTOR CODE BEGIN#
    def default_executor(self, data, sampler, batch_size,num_workers):
        if sampler:
            return torch.utils.data.DataLoader(data, batch_size=batch_size, num_workers=num_workers, sampler=sampler)
        else:
            return torch.utils.data.DataLoader(data, batch_size=batch_size, num_workers=num_workers)
    #EXECUTOR CODE END#

