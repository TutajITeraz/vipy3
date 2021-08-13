from vipy3.core import *

#EXECUTOR IMPORTS BEGIN#
import torch
import numpy as np
from torch.utils.data.sampler import SubsetRandomSampler

import torch.nn as nn
import torch.nn.functional as F
#EXECUTOR IMPORTS END#

class ViRandomSampler(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

    def initialize_values(self):
        self.inputs = [ InConnPercent(self,'valid_size',default_value=0.2),
                        InConn(self,'train_data',None)
                        ]
        self.outputs = [ OutConn(self,'valid_sampler', 'get_train_sampler', type='tensor') ]

    def gen_subset_random_sampler(self, train_data, valid_size):
        num_train = len(train_data)
        indices = list(range(num_train))

        np.random.shuffle(indices)
        split = int(np.floor(valid_size * num_train))
        train_idx, valid_idx = indices[split:], indices[:split]

        # define samplers for obtaining training and validation batches
        self.train_sampler = SubsetRandomSampler(train_idx)
        self.valid_sampler = SubsetRandomSampler(valid_idx)

        #here we will save that data to self. Self will be replaced with NodeName_

        return (self.train_sampler, self.valid_sampler)

    #EXECUTOR CODE BEGIN#
    def get_train_sampler(self, train_data, valid_size):

        train, valid = self.get_exe_result('gen_subset_random_sampler')
        return self.train_sampler

    def get_valid_sampler(self, train_data, valid_size):
        train, valid = self.get_exe_result('gen_subset_random_sampler')
        return self.valid_sampler

    #EXECUTOR CODE END#


    '''
    1. Replace self.get_exe_result('xxxx') with code get by:
        self.get_code(self, 'xxxx', result_prefix='', indent='')
        
    2. Add code_uuid to the function above
    
    3. Interprete if code_uuid is new - return function code else - return variable name
    
    4. Change variable names to output name instead of input names
        4.1 intermediate step - output in = out
        
    1.1 Replace "self." with node.get_name()
    
    '''
