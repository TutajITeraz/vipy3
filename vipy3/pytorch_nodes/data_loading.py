import dearpygui.dearpygui as dpg
from vipy3.core import *
#import sys
#import importlib
from importlib import import_module


class ViLoadDatasetMNIST(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state,'load_dataset_mnist',globals()['__package__'])

    def initialize_values(self):
        self.inputs = [ InConnFile(self,'root','~/pydata',label='root directory'),
                        InConnBool(self,'train',True),
                        InConnBool(self,'download',True),
                        InConn(self,'transforms',None)
                        ]
        self.outputs = [ OutConn(self,'data', self.default_executor, type='tensor') ]

