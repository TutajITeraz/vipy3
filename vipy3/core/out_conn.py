import dearpygui.dearpygui as dpg
import sys
from . import *

class OutConn():
    def __init__(self,parent_node,name,value_executor, state=None):
        self.parent_node = parent_node
        self.name = name
        self.uuid = gen_uuid()
        self.value_executor = value_executor

        if state is not None:
            self.deserialize(state)

    def deserialize(self,state):
        self.name = state['name']
        self.uuid = state['uuid']
        self.value_executor = state['value_executor']

    def serialize(self):
        state = {}
        state['name'] = self.name
        state['uuid'] = self.uuid
        state['value_executor'] = self.value_executor
        return state

    def is_fresh(self):
        pass

    def connect_to(self):
        pass

    def get_value(self):
        return self.value_executor()

    def get_name(self):
        return self.name

    def get_uuid(self):
        return self.uuid

    def dpg_render(self):
        parent_node_id = self.parent_node.get_dpg_node_id()
        self.dpg_attribute_id = dpg.add_node_attribute(parent=parent_node_id,attribute_type=dpg.mvNode_Attr_Output)
        self.gpg_text_id = dpg.add_text(self.get_name(), parent=self.dpg_attribute_id)