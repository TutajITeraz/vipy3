import dearpygui.dearpygui as dpg
from vipy3.core import *
import sys

class ViMetaIn(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)
        self.default_executor = 'bypass'

    def initialize_values(self):
        self.outputs = [OutConn(self,'input', 'bypass', type='any')]

    def bypass(self):
        return 1



class ViMetaOut(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)
        self.default_executor = 'bypass'

    def initialize_values(self):
        self.inputs = [ InConn(self,'out') ]

    def bypass(self):
        return 1
