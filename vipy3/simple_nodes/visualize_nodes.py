import dearpygui.dearpygui as dpg
from vipy3.core import *
import sys
import importlib

class ViShowText(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

        from ._show_text import show_text
        setattr(self, 'show_text', show_text.__get__(self))
        self.default_executor = 'show_text'

    def initialize_values(self):
        self.inputs = [ InConn(self,'str_or_val',1,None) ]
        self.visualizers = {'show_text': ViTextVisualizer(self,'value')}

