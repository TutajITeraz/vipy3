from vipy3.core import *

#EXECUTOR IMPORTS BEGIN#
import torch
#EXECUTOR IMPORTS END#
from vipy3.core.in_conn import InConn


class ViDataIter(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)
        self.default_executor_name = 'get_next'

    def initialize_values(self):
        self.inputs = [ InConnInt(self,'select',default_value=0,min=0, max=20),
                        InConn(self,'dataloader',None,type='tensor')
                        ]
        self.outputs = [ OutConn(self,'get_image', 'get_image', type='tensor'),
                         OutConn(self,'get_label', 'get_label', type='string'),
                         OutConn(self,'get_next', 'get_next', type='pair', hidden=True)]
        #functions used by other functions have to have the same name and executor


    #EXECUTOR CODE BEGIN#
    def get_next(self, select, dataloader):
        dataiter = iter(dataloader)
        images, labels = dataiter.next()

        self.image = images[select]
        self.label = labels[select]


    def get_image(self, train_data, valid_size):
        self.get_exe_result('get_next')
        return self.image


    def get_label(self, train_data, valid_size):
        self.get_exe_result('get_next')
        return self.label


    #EXECUTOR CODE END#