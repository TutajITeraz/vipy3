import dearpygui.dearpygui as dpg
import sys
from . import *

class Node:
    def __init__(self, parent_meta_node=None, serialized_state=None):
        self.parent_meta_node = parent_meta_node
        self.uuid = gen_uuid()
        self.name = self.get_class_name()

        self.inputs = []
        self.outputs = []
        self.actions = {'exePrint':'Execute and print'} #TODO implement actions
        self.visualizers = {'value':'value_widget'} #TODO implement visualizers
        
        self.exe_cache = {}

        self.stage = 0
        self.position = [10,10]

        self.fresh = False
        self.should_render_node = True

        if serialized_state:
            self.deserialize(serialized_state)
        else:
            self.initialize_values()

        print(self.parent_meta_node)

        print('class: '+str(self.get_class_name())+' parent_meta_node:'+str(self.parent_meta_node)+' should_render_node:'+str(self.should_render_node))
        if self.parent_meta_node and self.should_render_node:
            self.dpg_render_node()

    #TODO set fresh to false when changing any input value
    
    
    def exePrint(self):
        exe_func_name = 'default_executor'
        print(str(self.get_exe_result(exe_func_name)))

    def get_exe_result(self,exe_func_name):
        if self.is_fresh() and exe_func_name in self.exe_cache:
            return self.exe_cache[exe_func_name]

        self.exe_cache[exe_func_name] = getattr(self,exe_func_name)()

        self.set_fresh(True)
        return self.exe_cache[exe_func_name]

    def initialize_values(self):
        pass

    def get_all_inputs(self):
        return self.inputs

    def get_name(self):
        return self.name

    def get_uuid(self):
        return self.uuid

    def set_fresh(self,is_fresh):
        self.fresh = is_fresh

    def get_input_value(self, input_name):
        input = self.get_input_by_name(input_name)
        return input.get_value()

    def is_fresh(self):
        if not self.fresh:
            return False
        
        for input in self.inputs:
            if not input.is_fresh():
                return False

        return True

    def set_stage(self, stage):
        self.stage = stage
        LOG.log(self.get_name() + "\t changed stage to: " + self.get_stage_name(stage))

    def get_input_by_name(self,name):
        for input in self.inputs:
            if input.get_name() == name:
                return input

        return None

    def get_output_by_name(self,name):
        for output in self.outputs:
            if output.get_name() == name:
                return output

        return None

    def get_position():
        self.position = dpg.get_item_pos(self.dpg_node_id);
        return self.position

    def serialize(self):
        self.position = self.get_position()

        state = {}
        state['uuid']=self.get_uuid();
        state['name']=self.get_name();
        state['position']=self.get_position();
        state['inputs']={}#TODO zmienić na []
        state['outputs']={}#TODO zmienić na []

        state['inputs']=[]
        for input in self.inputs:
            state['inputs'].append(input.serialize())

        state['outputs']=[]
        for output in self.outputs:
            state['outputs'].append(output.serialize())

        return state


    def deserialize(self,state):

        self.uuid = state['uuid']
        self.name = state['name']

        for inputState in state['inputs']:
            input_class_name = inputState['class_name']
            input_class = getattr(sys.modules[__name__], input_class_name)
            self.inputs.append( input_class(self,serialized_state=inputState) )

        for outputState in state['outputs']:
            self.outputs.append( OutConn(self,outputState['name'],None,outputState) )

        self.set_position(state['position'])
        self.fresh = False


    def get_position(self):
        if hasattr(self, 'dpg_node_id') and self.dpg_node_id is not None:
            self.position = dpg.get_item_pos(self.dpg_node_id)
        return self.position

    def set_position(self, position):
        self.position = position
        if hasattr(self,'dpg_node_id') and self.dpg_node_id is not None:
            dpg.set_item_pos(self.dpg_node_id,position)

    def default_executor(self):
        return None

    def get_dpg_node_id(self):
        return self.dpg_node_id

    def dpg_action_callback(self,sender,app_data,user_data):
        getattr(self,user_data)()

    def dpg_edit_callback(self,sender,app_data,user_data):
        #TODO edit node callback
        pass

    def dpg_delete_callback(self,sender,app_data,user_data):
        #TODO delete node callback
        pass

    def dpg_render_node(self):
        print('dpg_render_node')

        self.dpg_node_id = dpg.add_node(label = self.get_name()+' '+self.get_uuid(), pos=self.get_position(), parent=self.parent_meta_node.dpg_get_node_editor_id(), user_data={'node_uuid': self.get_uuid()})

        print(' dpg_node_id = '+str(self.dpg_node_id))
        print('user data of node = '+str(dpg.get_item_user_data(self.dpg_node_id)))

        for input in self.inputs:
            input.dpg_render()

        for visualizer in self.visualizers: #TODO render visualizers
            pass

        for output in self.outputs:
            output.dpg_render()

        self.fake_action_attribute_id = dpg.add_node_attribute(parent=self.dpg_node_id, attribute_type=dpg.mvNode_Attr_Static)
        dpg.add_button(label='x', callback=self.dpg_delete_callback, parent=self.fake_action_attribute_id)
        dpg.add_same_line(parent=self.fake_action_attribute_id)
        dpg.add_button(label='edit', callback=self.dpg_edit_callback, parent=self.fake_action_attribute_id)

        for action in self.actions:
            dpg.add_same_line(parent=self.fake_action_attribute_id)
            dpg.add_button(label=self.actions[action], callback=self.dpg_action_callback, user_data=action, parent=self.fake_action_attribute_id)

    def get_class_name(self):
        return type(self).__name__
