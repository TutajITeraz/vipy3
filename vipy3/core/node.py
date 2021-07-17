import dearpygui.dearpygui as dpg
import sys
import inspect
from . import *
import os

class Node:
    def __init__(self, parent_meta_node=None, serialized_state=None):
        self.parent_meta_node = parent_meta_node
        self.uuid = gen_uuid()
        self.name = self.get_class_name()

        self.inputs = []
        self.outputs = []
        self.actions = {'exe_print':'Exe', 'dpg_get_code_callback': 'Gen code'} #TODO implement actions
        self.visualizers = {'value':'value_widget'} #TODO implement visualizers
        self.default_executor = ''
        
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

    def dpg_get_code_callback(self):
        print(self.get_code(self.default_executor))
    
    def get_code(self, value_executor, result_prefix=''):
        #TODO code generator
        code = ''

        func_to_call = getattr(self,value_executor)
        params = inspect.signature(func_to_call).parameters

        for param in params:
            input_code = self._get_input_code(param, self.get_name()+'_'+str(param) + ' = ')
            code += input_code + '\n'

        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path = "../simple_nodes/"
        abs_file_path = os.path.join(script_dir, rel_path)

        f = open(abs_file_path+"/_"+value_executor+".py", "r")
        #code_file = f.read()
        for line in f:
            if not 'def' in line:
                print('line ======> '+line)
                if line[0]==' ':
                    line = line.lstrip()

                if not 'return' in line:
                    for param in params:
                        line = line.replace(param, self.get_name()+'_'+param)
                    code+=line 
                elif result_prefix != '':
                    print('line ======> (1) '+line)
                    result_line = line.replace("return ", result_prefix)
                    print('line ======> (1 result) '+result_line)
                    code+=result_line
                else:
                    print('line ======> (2) '+line)
                    result_line = line.replace("return ", "print( ") + " )"
                    print('line ======> (2 result) '+result_line)
                    code+=result_line

        f.close()

        return code

    def _get_input_code(self, input_name, result_prefix=''):
        input = self.get_input_by_name(input_name)
        return input.get_code(result_prefix)

    def exe_print(self):
        print(str(self.get_exe_result(self.default_executor)))

    def get_exe_result(self,exe_func_name):
        if self.is_fresh() and exe_func_name in self.exe_cache:
            return self.exe_cache[exe_func_name]

        func_to_call = getattr(self,exe_func_name)
        params=inspect.signature(func_to_call).parameters

        print('try to gather function params:'+str(params))

        args = []
        for param in params:
            print('get '+str(param))
            value = self.get_input_value(param)
            args.append(value)
        
        print('args '+str(args))

        self.exe_cache[exe_func_name] = func_to_call(*args)

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
            print('checking freshness of node '+str(input))
            if input.is_fresh() == False:
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

    def get_dpg_node_id(self):
        return self.dpg_node_id

    def dpg_action_callback(self,sender,app_data,user_data):
        getattr(self,user_data)()

    def set_name(self,name):
        self.name = name
        dpg.set_item_label(self.dpg_node_id,self.name)

    def dpg_delete_callback(self,sender,app_data,user_data):
        dpg_node_attr_id = dpg.get_item_parent(sender)
        dpg_node_id = dpg.get_item_parent(dpg_node_attr_id)


        #TODO delete input links

        #TODO delete output links


        dpg.delete_item(dpg_node_id)

    def dpg_render_node(self):
        print('dpg_render_node')

        self.dpg_node_id = dpg.add_node(label = self.get_name(), pos=self.get_position(), parent=self.parent_meta_node.dpg_get_node_editor_id(), user_data={'node_uuid': self.get_uuid()})

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
        self.dpg_edit_button_id = dpg.add_button(label='edit', parent=self.fake_action_attribute_id)

        #Edit modal:
        with dpg.popup(self.dpg_edit_button_id, modal=True, mousebutton=dpg.mvMouseButton_Left) as modal_id:
            dpg.add_text("Node names should be unique if you want to generate code")
            self.dpg_new_name_input_id = dpg.add_input_text(parent=modal_id, label='name', default_value=self.get_name())
            dpg.add_separator()
            dpg.add_button(label="OK", width=75, callback=lambda: [self.set_name(dpg.get_value(self.dpg_new_name_input_id)), dpg.configure_item(modal_id, show=False)])
            dpg.add_same_line()
            dpg.add_button(label="Cancel", width=75, callback=lambda: dpg.configure_item(modal_id, show=False))



        for action in self.actions:
            dpg.add_same_line(parent=self.fake_action_attribute_id)
            dpg.add_button(label=self.actions[action], callback=self.dpg_action_callback, user_data=action, parent=self.fake_action_attribute_id)

    def get_class_name(self):
        return type(self).__name__
