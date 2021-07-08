import dearpygui.dearpygui as dpg
from vipy3.core import *
import sys

class ViAdd(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

    def initialize_values(self):
        self.inputs = {'a': InConnInt(self,'number a',1,None,0,100), 'b': InConnInt(self,'number b',1,None,0,100) }
        self.outputs = {'result': OutConn(self,'result', 'default_executor')}

    def default_executor(self):
        a = self.inputs['a'].get_value()
        b = self.inputs['b'].get_value()
        result = a+b
        return result