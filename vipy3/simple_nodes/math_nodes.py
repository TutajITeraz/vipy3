import dearpygui.dearpygui as dpg
from vipy3.core import *
import sys
import importlib

class ViAdd(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

        from ._add_exe import add_exe
        setattr(self, 'add_exe', add_exe.__get__(self))
        self.default_executor = 'add_exe'
        
        #add_executor_func = importlib.import_module('._math_nodes_impl','vipy3.simple_nodes').add_exe
        #setattr(self, 'add_exe', add_exe_func.__get__(self))


    def initialize_values(self):
        self.inputs = [ InConnInt(self,'num_a',1,None,0,100), InConnInt(self,'num_b',1,None,0,100) ]
        self.outputs = [ OutConn(self,'result', 'add_exe') ]

#add_executor_func = importlib.import_module('._math_nodes_impl','vipy3.simple_nodes').add_executor
#setattr(ViAdd, 'add_executor', classmethod( add_executor_func ) )
