import dearpygui.dearpygui as dpg
from vipy3.core import *
import sys
import importlib

class ViLoadDatasetMNIST(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

        print('Init end, loading function')

        from ._load_dataset_mnist import load_dataset_mnist
        print('Init end, loading function 2')
        setattr(self, 'load_dataset_mnist', load_dataset_mnist.__get__(self))
        print('Init end, loading function 3')
        self.default_executor = 'load_dataset_mnist'

        print('Function loaded')

    def unbind_methods(self):
        del self.load_dataset_mnist

    def initialize_values(self):
        self.inputs = [ InConnFile(self,'root','~/pydata',label='root directory'),
                        InConnBool(self,'train',True),
                        InConnBool(self,'download',True),
                        InConn(self,'transforms',None)
                        ]
        self.outputs = [ OutConn(self,'data', self.default_executor, type='tensor') ]

