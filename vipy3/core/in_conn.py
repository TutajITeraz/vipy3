import dearpygui.dearpygui as dpg
import sys
from . import *

class InConn():
    def __init__(self,parent_node,name='',default_value=None, serialized_state=None):
        self.parent_node = parent_node
        self.name = name
        self.value = default_value
        self.uuid = gen_uuid()

        #self.connected_node_uuid = ''
        #self.connected_node_out_uuid = ''

        self.connected_node_out = None

        if serialized_state is not None:
            self.deserialize(serialized_state)

        self.fresh = False

        #self.dpg_render()

    def get_dpg_attribute_id(self):
        return self.dpg_attribute_id

    def get_class_name(self):
        return type(self).__name__

    def get_connected_node_out(self):
        return self.connected_node_out;

    def get_parent_node(self):
        return self.parent_node

    def set_connected_node_out(self,node_out_attr):
        self.connected_node_out = node_out_attr

        return True# TODO Allow connection (check type)
    
    def is_fresh(self):
        if self.is_connected():
            return self.connected_node_out.is_fresh()

        return self.fresh

    def is_connected(self):
        if self.connected_node_out is not None:
            return True
        return False

    def connect_to(self):
        pass

    def get_value(self):

        if self.is_connected():
            self.value = self.get_connected_node_out().get_value()
        elif hasattr(self,'dpg_input_id') and self.dpg_input_id:
            self.value = dpg.get_value(self.dpg_input_id)
        return self.value

    def get_code(self):
        if self.is_connected():
            return self.get_connected_node_out().get_code()
        elif hasattr(self,'dpg_input_id') and self.dpg_input_id:
            return dpg.get_value(self.dpg_input_id)
        return ''

    def set_value(self):
        return self.value

    def get_name(self):
        return self.name

    def get_uuid(self):
        return self.uuid

    def dpg_get_attribute_id(self):
        return self.dpg_attribute_id

    def dpg_render(self):
        parent_node_id = self.parent_node.get_dpg_node_id()
        self.dpg_attribute_id = dpg.add_node_attribute(parent=parent_node_id, user_data=self)
        self.gpg_text_id = dpg.add_text(self.get_name(), parent=self.dpg_attribute_id)

        print(' dpg_attribute_id = '+str(self.dpg_attribute_id))

class InConnInt(InConn):
    def __init__(self,parent_node,name='',default_value=None,serialized_state=None,min=0,max=100):
        super().__init__(parent_node,name,default_value,serialized_state)
        
        self.max = max
        self.min = min

        if serialized_state is not None:
            self.deserialize(serialized_state)
    
    def serialize(self):
        state = {}
        state['name']=self.get_name()
        state['class_name'] = self.get_class_name()
        state['value'] = self.get_value()
        state['max'] = self.max
        state['min'] = self.min
        state['uuid'] = self.get_uuid()
        return state

    def deserialize(self, state):
        self.name = state['name']
        self.value = state['value']
        self.max = state['max']
        self.min = state['min']
        self.uuid = state['uuid']

        self.fresh = False

    def dpg_render(self):
        print('dpg_render in conn int')
        parent_node_id = self.parent_node.get_dpg_node_id()
        self.dpg_attribute_id = dpg.add_node_attribute(parent=parent_node_id, user_data=self)
        self.dpg_input_id = dpg.add_input_int(label=self.get_name(), default_value=self.get_value(), width=75, parent=self.dpg_attribute_id, max_value=self.max, min_value=self.min)
