import dearpygui.dearpygui as dpg
from vipy3.core import *
import sys

class ViMetaIn(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

    def initialize_values(self):
        self.outputs = {'input': OutConn(self,'input', 'default_executor')}

    def default_executor(self):
        return 1



class ViMetaOut(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

    def initialize_values(self):
        self.inputs = {'out': InConnInt(self,'out',1,None,0,100)}

    def default_executor(self):
        a = self.inputs['a'].get_value()
        b = self.inputs['b'].get_value()
        result = a+b
        return result

    def dpg_render_node(self):
        super().dpg_render_node()

        self.dpg_value_text = dpg.add_text(default_value='(value)',parent=self.dpg_node_id)