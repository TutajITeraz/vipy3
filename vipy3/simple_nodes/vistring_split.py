import dearpygui.dearpygui as dpg
from vipy3.core import *
import sys
import importlib

class ViStringSplit(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)
        self.default_executor_name = 'get_str_pair'

    def initialize_values(self):
        self.inputs = [ InConnStr(self,'str','Ala ma kota',None), InConnStr(self,'delim',' ',None) ]
        self.outputs = [ OutConn(self,'get_str_pair', 'get_str_pair', type='pair', hidden=True),
                         OutConn(self,'before', 'get_before', type='string'),
                         OutConn(self,'after', 'get_after', type='string')
                         ]

    #EXECUTOR CODE BEGIN#
    def get_str_pair(self, str, delim):
        result = str.split(delim)
        self.splitted_pair = (result[0], result[1])

    def get_before(self):
        self.get_exe_result('get_str_pair')
        return self.splitted_pair[0]

    def get_after(self):
        self.get_exe_result('get_str_pair')
        return self.splitted_pair[1]

    #EXECUTOR CODE END#