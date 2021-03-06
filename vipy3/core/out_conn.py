import dearpygui.dearpygui as dpg
import sys
from . import *
import weakref
import vipy3.core.helpers

class OutConn():
    def __init__(self,parent_node,name,value_executor, state=None, type='any', label='', hidden=False):
        self.parent_node = weakref.proxy(parent_node)
        self.name = name
        self.uuid = gen_uuid()
        self.value_executor = value_executor
        self.type = type
        self.label = label
        self.last_code_uuid = ''
        self.hidden = hidden

        if state is not None:
            self.deserialize(state)
            
    def __del__(self):
        print('Destructor of '+self.get_name())

    def get_dpg_attribute_id(self):
        return self.dpg_attribute_id

    def deserialize(self,state):
        self.name = state['name']
        self.uuid = state['uuid']
        self.value_executor = state['value_executor']
        self.type = state['type']
        self.label = state['label']

    def get_parent_node(self):
        return self.parent_node

    def get_type(self):
        return self.type

    def get_label(self):
        if self.label != '':
            return self.label
        else:
            return self.get_name()

    def serialize(self):
        state = {}
        state['name'] = self.name
        state['uuid'] = self.uuid
        state['value_executor'] = self.value_executor
        state['type'] = self.type
        state['label'] = self.label

        return state

    def is_fresh(self):
        return self.parent_node.is_fresh()

    def connect_to(self):
        pass

    def get_value(self):
        return self.parent_node.get_exe_result(self.value_executor)

    def get_code(self, result_prefix='',indent='', code_uuid=''):
        result_variable_name = self.get_parent_node().get_name()+'_'+self.get_name()

        if code_uuid == self.last_code_uuid:
            print('FUNCTION CALLED TWICE '+self.get_name()+' uuid: '+code_uuid)
            code = '\n'
            if result_prefix != '':
                code = indent + result_prefix + result_variable_name + '\n'

            return {'imports_code': '', 'functions_code': '', 'code': code }
        self.last_code_uuid = code_uuid

        node_code = self.parent_node.get_code(self.value_executor, (result_variable_name+' = '), indent=indent, code_uuid=code_uuid)
        #renaming
        if result_prefix != '':
            node_code['code'] += indent + result_prefix + result_variable_name+'\n'
        return node_code

    def get_name(self):
        return self.name

    def get_uuid(self):
        return self.uuid

    def dpg_render(self):
        if self.hidden:
            return

        parent_node_id = self.parent_node.get_dpg_node_id()
        self.dpg_attribute_id = dpg.add_node_attribute(parent=parent_node_id,attribute_type=dpg.mvNode_Attr_Output, user_data=weakref.proxy(self))
        self.gpg_text_id = dpg.add_text(self.get_label(), parent=self.dpg_attribute_id)

    def dpg_get_attribute_id(self):
        return self.dpg_attribute_id