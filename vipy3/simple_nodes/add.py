import dearpygui.dearpygui as dpg
from vipy3.core import *
import sys
import importlib

class ViAdd(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

    def initialize_values(self):
        self.inputs = [ InConnInt(self,'num_a',1,None,0,100,label='Num A'), InConnInt(self,'num_b',1,None,0,100,label='Num B') ]
        self.outputs = [ OutConn(self,'result', 'default_executor', type='number', label='Result Number') ]

    #EXECUTOR CODE BEGIN#
    def default_executor(self, num_a, num_b):
        if num_a is None:
            num_a = 0
        if num_b is None:
            num_b = 0 
        return num_a+num_b
    #EXECUTOR CODE END#