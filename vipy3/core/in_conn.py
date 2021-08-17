import dearpygui.dearpygui as dpg
import sys
from . import *
import weakref
import vipy3.core.helpers

class InConn():
    def __init__(self,parent_node,name='', default_value=None, serialized_state=None, type='any', label=''):
        self.parent_node = weakref.proxy(parent_node)
        self.name = name
        self.value = default_value
        self.uuid = gen_uuid()
        self.type = type
        self.label = label


        #self.connected_node_uuid = ''
        #self.connected_node_out_uuid = ''

        self.connected_node_out = None

        if serialized_state is not None:
            self.deserialize(serialized_state)

        self.fresh = False

        #self.dpg_render()
    def __del__(self):
        print('Destructor of '+self.get_name())

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

        if node_out_attr is None:
            if hasattr(self,'dpg_input_id'):
                dpg.show_item(self.dpg_input_id)
                dpg.hide_item(self.dpg_text_id)
            return True

        if self.get_type() == 'any' or node_out_attr.get_type() == 'any':
            connected = True
        elif self.get_type() == node_out_attr.get_type():
            connected = True
        else:
            self.connected_node_out = None
            connected = False

        if connected and hasattr(self,'dpg_input_id'):
            dpg.hide_item(self.dpg_input_id)
            dpg.show_item(self.dpg_text_id)

        return connected# TODO Allow connection (check type)
    
    def is_fresh(self):
        #print('in connection is checking freshness: ')
        if self.is_connected():
            self.fresh = self.connected_node_out.is_fresh()

        #print('in connection is: '+str(self.fresh))
        return self.fresh

    def is_connected(self):
        if self.connected_node_out is not None:
            return True
        return False

    def connect_to(self):
        pass

    def get_value(self, calculate=True):

        if self.is_connected() and calculate:
            self.value = self.get_connected_node_out().get_value()
        elif hasattr(self,'dpg_input_id') and self.dpg_input_id:
            self.value = dpg.get_value(self.dpg_input_id)

        self.fresh = True

        return self.value

    def get_code(self, result_prefix='', indent=''):
        if self.is_connected():
            connected_out = self.get_connected_node_out()
            print('connected_out = '+str(connected_out))
            return connected_out.get_code(result_prefix, indent=indent)
        elif hasattr(self,'dpg_input_id') and self.dpg_input_id:
            return {'imports_code': '', 'functions_code': '', 'code': indent+result_prefix + str(dpg.get_value(self.dpg_input_id))}
        return ''

    def set_value(self, value):
        self.value = value
        return self.value

    def get_name(self):
        return self.name

    def get_uuid(self):
        return self.uuid

    def get_type(self):
        return self.type

    def dpg_get_attribute_id(self):
        return self.dpg_attribute_id

    def dpg_val_change_callback(self,sender,app_data,user_data):
        self.fresh = False

    def dpg_render(self):
        parent_node_id = self.parent_node.get_dpg_node_id()
        self.dpg_attribute_id = dpg.add_node_attribute(parent=parent_node_id, user_data=weakref.proxy(self))
        self.dpg_text_id = dpg.add_text(self.get_label(), parent=self.dpg_attribute_id)

        print(' dpg_attribute_id = '+str(self.dpg_attribute_id))

    def get_label(self):
        if self.label != '':
            return self.label
        else:
            return self.get_name()

    def serialize(self):
        state = {}
        state['name']=self.get_name()
        state['class_name'] = self.get_class_name()
        state['value'] = self.get_value(False) #False because we do not want to calculate
        state['uuid'] = self.get_uuid()
        state['type'] = self.type
        state['label'] = self.label
        return state

    def deserialize(self, state):
        self.name = state['name']
        self.value = state['value']
        self.uuid = state['uuid']
        self.type = state['type']
        self.label = state['label']

        self.fresh = False


class InConnInt(InConn):
    def __init__(self,parent_node,name='',default_value=None,serialized_state=None,min=0,max=100,label=''):
        type = 'number'
        super().__init__(parent_node,name,default_value,serialized_state,type,label)
        
        self.max = max
        self.min = min

        if serialized_state is not None:
            self.deserialize(serialized_state)
    
    def serialize(self):
        state = {}
        state['name']=self.get_name()
        state['class_name'] = self.get_class_name()
        state['value'] = self.get_value(False)     #should not calculate value when serialization
        state['max'] = self.max
        state['min'] = self.min
        state['uuid'] = self.get_uuid()
        state['type'] = self.type
        return state

    def deserialize(self, state):
        self.name = state['name']
        self.value = state['value']
        self.max = state['max']
        self.min = state['min']
        self.uuid = state['uuid']
        self.type = state['type']

        self.fresh = False

    def dpg_render(self):
        print('dpg_render in conn int value:'+str(self.value))
        parent_node_id = self.parent_node.get_dpg_node_id()
        self.dpg_attribute_id = dpg.add_node_attribute(parent=parent_node_id, user_data=weakref.proxy(self))
        self.dpg_input_id = dpg.add_input_int(label=self.get_label(), default_value=self.value, width=75, parent=self.dpg_attribute_id, max_value=self.max, min_value=self.min, callback=lambda a,b,c: self.dpg_val_change_callback(a,b,c) )
        self.dpg_text_id = dpg.add_text(self.get_label(), parent=self.dpg_attribute_id,show=False)



class InConnBool(InConn):
    def __init__(self,parent_node,name='',default_value=True,serialized_state=None, label=''):
        type = 'number'
        super().__init__(parent_node,name,default_value,serialized_state,type,label)

        if serialized_state is not None:
            self.deserialize(serialized_state)

    def dpg_render(self):
        print('dpg_render in conn int value:'+str(self.value))
        parent_node_id = self.parent_node.get_dpg_node_id()
        self.dpg_attribute_id = dpg.add_node_attribute(parent=parent_node_id, user_data=weakref.proxy(self))
        ###
        self.dpg_input_id = dpg.add_checkbox(label=self.get_label(),  default_value=self.value, parent=self.dpg_attribute_id, callback=lambda a,b,c: self.dpg_val_change_callback(a,b,c))
        self.dpg_text_id = dpg.add_text(self.get_label(), parent=self.dpg_attribute_id,show=False)
