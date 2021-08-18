import dearpygui.dearpygui as dpg
from vipy3.core import *
import sys
import importlib

class ViShowText(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

    def initialize_values(self):
        self.inputs = [ InConn(self,'str_or_val',1,None) ]
        self.outputs = [ OutConn(self,'bypass', 'default_executor', type='string') ]
        self.visualizers = {'show_text': ViTextVisualizer(self,'value', label='Show Text')}

    #EXECUTOR CODE BEGIN#
    def default_executor(self, str_or_val):
        return str_or_val
    #EXECUTOR CODE END#