import dearpygui.dearpygui as dpg
from vipy3.core import *
import sys
import importlib

class ViLoadDatasetMNIST(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

        from ._load_dataset_mnist import load_dataset_mnist
        setattr(self, 'load_dataset_mnist', load_dataset_mnist.__get__(self))
        self.default_executor = 'load_dataset_mnist'

    def unbind_methods(self):
        del self.load_dataset_mnist

    def initialize_values(self):
        self.inputs = [ InConnFile(self,'root','~/pydata',label='root directory'),
                        InConnBool(self,'train',True),
                        InConnBool(self,'download',True),
                        InConn(self,'transforms',None)
                        ]
        self.outputs = [ OutConn(self,'data', self.default_executor, type='tensor') ]

