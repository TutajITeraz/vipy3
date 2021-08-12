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

    #EXECUTOR FUNCTIONS BEGIN#
    def gen_subset_random_sampler(self, train_data, valid_size):
        num_train = len(train_data)
        indices = list(range(num_train))

        np.random.shuffle(indices)
        split = int(np.floor(valid_size * num_train))
        train_idx, valid_idx = indices[split:], indices[:split]

        # define samplers for obtaining training and validation batches
        gen_subset_random_sampler.train_sampler = SubsetRandomSampler(train_idx)
        gen_subset_random_sampler.valid_sampler = SubsetRandomSampler(valid_idx)

        return (self.gen_subset_random_sampler.train_sampler, self.gen_subset_random_sampler.valid_sampler)
    #static:
    gen_subset_random_sampler.train_sampler = None
    gen_subset_random_sampler.valid_sampler = None
    #EXECUTOR FUNCTIONS END#

    #EXECUTOR CODE BEGIN#
    def get_train_sampler(self, train_data, valid_size):
        train, valid = self.gen_subset_random_sampler()
        return train

    def get_valid_sampler(self, train_data, valid_size):
        train, valid = self.gen_subset_random_sampler()
        return valid
    #EXECUTOR CODE END#

