import dearpygui.dearpygui as dpg
from vipy3.core import *
import sys
import importlib

class ViStringConcat(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

    def initialize_values(self):
        self.inputs = [ InConnStr(self,'str1','',None), InConnStr(self,'str2','',None) ]
        self.outputs = [ OutConn(self,'concatenate', self.default_executor_name, type='string') ]

    #EXECUTOR CODE BEGIN#
    def default_executor(self, str1, str2):
        return str1 + str2


    #EXECUTOR CODE END#