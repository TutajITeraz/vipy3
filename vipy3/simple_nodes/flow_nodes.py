import dearpygui.dearpygui as dpg
from vipy3.core import *
import sys
import importlib

class ViFor(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)
        self.default_executor = 'for_exe'

        self.iterator=0

    def for_exe(self):
        how_many = self.get_input_value('how_many')

        result_list = []
        for self.iterator in range(how_many):
            data = self.get_input_value('data')
            result_list.append(data)
        return result_list

    def get_iter(self):
        return self.iterator

    def initialize_values(self):
        self.inputs = [ InConnInt(self,'how_many',1,None,0,100), InConn(self,'data') ]
        self.outputs = [ OutConn(self,'result_list', 'for_exe', type='list'), OutConn(self,'i', 'get_iter', type='number') ]