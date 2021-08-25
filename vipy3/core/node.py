import dearpygui.dearpygui as dpg
import sys
import inspect
from . import *
import os
import weakref
import gc
from importlib import import_module


class Node:
    def __init__(self, parent_meta_node=None, serialized_state=None):
        if parent_meta_node:
            self.parent_meta_node = weakref.proxy(parent_meta_node)
        self.uuid = gen_uuid()
        self.name = self.get_class_name()
        self.default_executor_name = 'default_executor'

        self.inputs = []
        self.outputs = []
        self.actions = {'exe_print':'Exe', 'dpg_get_code_callback': 'Gen code'}
        self.visualizers = {}
        
        self.exe_cache = {}
        self.stage = 0
        self.position = [10,10]
        self.fresh = False
        self.should_render_node = True

        if serialized_state:
            self.deserialize(serialized_state)
        else:
            self.initialize_values()

        print('class: '+str(self.get_class_name())+' should_render_node:'+str(self.should_render_node))
        if hasattr(self,'parent_meta_node') and self.parent_meta_node and self.should_render_node:
            self.dpg_render_node()

    def _get_self_filepath(self):
        return os.path.abspath(sys.modules[self.__class__.__module__].__file__)

    def _get_executor_function_text(self, value_executor):
        code = ''
        imports_code = ''
        functions_code = ''

        imports_started = False

        code_started = False
        executor_code_started = False

        f = open(self._get_self_filepath(), "r")
        for line in f:

            if '#EXECUTOR IMPORTS BEGIN#' in line:
                imports_started = True
                continue

            if '#EXECUTOR CODE BEGIN#' in line:
                code_started = True
                continue

            if '#EXECUTOR IMPORTS END#' in line:
                imports_started = False
                continue

            if '#EXECUTOR CODE END#' in line:
                code_started = False
                break

            if code_started:

                if executor_code_started:
                    if 'def' in line:
                        break
                    else:
                         code += line[4:]

                #executor_code_started = False and:
                elif ('def '+value_executor) in line:
                    executor_code_started = True

            if imports_started:
                imports_code += line

        f.close()

        return {'imports_code': imports_code, 'functions_code': functions_code, 'code': code}


    def unbind_methods(self):
        pass
        #if hasattr(self,'executor_module_name') and self.executor_module_name != '':
        #    del getattr(self,self.executor_module_name)
    
    def __del__(self):
        print('Destructor of '+self.get_name())

    #TODO set fresh to false when changing any input value

    def dpg_get_code_callback(self):
        code_uuid = gen_uuid()
        code = self.get_code(self.default_executor_name, code_uuid=code_uuid)

        full_code = code['imports_code'] + '\n' + code['functions_code']+ '\n' + code['code']
        cw = CodeWindow(full_code)
    
    def get_code(self, value_executor, result_prefix='', indent='', code_uuid=''):
        print(self.get_name()+' uuid '+code_uuid)

        code = ''
        imports_code = ''
        functions_code = ''

        print('value_executor: ', str(value_executor))

        func_to_call = getattr(self,value_executor)
        params = inspect.signature(func_to_call).parameters

        for param in params:
            input_code = self._get_input_code(param, self.get_name()+'_'+str(param) + ' = ', code_uuid=code_uuid)
            if(len(input_code)<2):
                continue

            code += input_code['code'] + '\n'
            imports_code += input_code['imports_code']
            functions_code += input_code['functions_code']

        #
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path = "../simple_nodes/"
        abs_file_path = os.path.join(script_dir, rel_path)

        executor_code = self._get_executor_function_text(value_executor)
        imports_code = executor_code['imports_code']

        if value_executor != 'bypass':
            for line in executor_code['code'].splitlines():
                line = line+'\n'
                if not 'def' in line:
                    #print('line ======> '+line)
                    if line[0]==' ':
                        #line = line.lstrip()
                        line = line[4:]

                    if 'self.get_exe_result(' in line:
                        code += "#code from inner call start\n"
                        result_line = line.split("self.get_exe_result(")[1]
                        result_line = result_line.split(")")[0]

                        result_line = result_line.replace("'", "")
                        result_line = result_line.replace('"', '')

                        #TODO because output caches ;) But do we really have to had an output to perform this?
                        #TODO Maybe hidden output will do?
                        output = self.get_output_by_name(result_line)
                        result_code = output.get_code(result_prefix='', indent='', code_uuid=code_uuid)


                        code += result_code['code']+'\n'

                        code += "#code from inner call end\n"

                        continue

                    line = line.replace('self.',self.get_name()+'_')

                    for param in params:
                        line = line.replace(param, self.get_name()+'_'+param)

                    if not 'return' in line:
                        code+=line 
                    elif result_prefix != '':
                        #print('line ======> (1) '+line)
                        result_line = line.replace("return ", result_prefix)
                        #print('line ======> (1 result) '+result_line)
                        code+=result_line
                    else:
                        #print('line ======> (2) '+line)
                        result_line = line.replace("return ", "print( ") + " )"
                        #print('line ======> (2 result) '+result_line)
                        code+=result_line

        else:
            for param in params:
                code += result_prefix+self.get_name()+'_'+param

        #Add indentation:
        indent_code = ''
        for line in code.splitlines():
            indent_code += indent+line+'\n'

        return {'imports_code': imports_code, 'functions_code': functions_code, 'code': indent_code}

    def _get_input_code(self, input_name, result_prefix='', indent='', code_uuid=''):
        print('getting input: '+input_name)
        input = self.get_input_by_name(input_name)
        if input is None:
            LOG.log('error', 'cannot find input: '+input_name)
            return {'imports_code': '', 'functions_code': '', 'code': ''}

        return input.get_code(result_prefix, indent=indent, code_uuid=code_uuid)

    def exe_print(self):
        print('default_executor_name: ', self.default_executor_name)
        print(str(self.get_exe_result(self.default_executor_name)))

    def get_exe_result(self,exe_func_name=''):
        if exe_func_name == '':
            exe_func_name=self.default_executor_name

        if self.is_fresh() and exe_func_name in self.exe_cache:
            #print(self.get_name()+' node is fresh and returning cached value:'+str(self.exe_cache[exe_func_name]))
            self.set_stage(3)
            return self.exe_cache[exe_func_name]

        func_to_call = getattr(self,exe_func_name)
        params=inspect.signature(func_to_call).parameters

        print('try to gather function params:'+str(params)+' of func name: '+exe_func_name)
        self.set_stage(1)

        args = {}
        for param in params:
            #print('get '+str(param))
            value = self.get_input_value(param)
            args[param] = value
        
        #print('args '+str(args))

        #Visualizers:
        print(self.get_name()+' node visualizers: '+str(self.visualizers))
        for v in self.visualizers:
            print('VISUALIZE:'+ v)

            visualizer = self.visualizers[v]
            visualizer.update(**args)

        self.set_stage(2)
        self.exe_cache[exe_func_name] = func_to_call(**args)
        self.set_stage(3)

        #print(self.get_name() + ' node is not fresh, so calculated value is:' + str(self.exe_cache[exe_func_name]))


        self.set_fresh(True)
        return self.exe_cache[exe_func_name]

    def initialize_values(self):
        pass

    def get_all_inputs(self):
        return self.inputs

    def get_name(self):
        return self.name
        
    def set_name(self,name):
        self.name=name
        return self.name

    def get_uuid(self):
        return self.uuid

    def set_fresh(self,is_fresh):
        self.fresh = is_fresh

    def get_input_value(self, input_name):
        input = self.get_input_by_name(input_name)
        if input is None:
            LOG.log('error','Could not get input named:'+input_name)
            return None
        return input.get_value()

    def is_fresh(self):
        #if self.stage == 1 or self.stage == 2 : #during calculation (used by loop)
        #    return True

        if not self.fresh:
            return False
        
        for input in self.inputs:
            print(self.get_name()+' is checking freshness of node input '+str(input.get_name()))
            if input.is_fresh() == False:
                print('    is NOT fresh')
                return False
            print('    is fresh')

        return True

    # 0 = init
    # 1 = waiting for data
    # 2 = calculating
    # 3 = done (fresh)
    # 4 = not fresh
    def set_stage(self, stage):
        self.stage = stage

        if self.dpg_node_id and stage == 1:
            dpg.set_item_theme(self.dpg_node_id, WAITING_NODE_THEME)

        elif self.dpg_node_id and stage == 2:
            dpg.set_item_theme(self.dpg_node_id, CALCULATING_NODE_THEME)

        elif self.dpg_node_id and stage == 3:
            dpg.set_item_theme(self.dpg_node_id, DONE_NODE_THEME)

        LOG.log(self.get_name() + "\t changed stage to: " + str(stage))

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
        state['uuid']=self.get_uuid()
        state['name']=self.get_name()
        state['position']=self.get_position()
        state['class_name']=self.get_class_name()


        state['inputs']=[]
        for input in self.inputs:
            state['inputs'].append(input.serialize())

        state['outputs']=[]
        for output in self.outputs:
            state['outputs'].append(output.serialize())

        state['visualizers'] = {}
        for v in self.visualizers:
            state['visualizers'][v] = self.visualizers[v].serialize()

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

        for v in state['visualizers']:
            visualizer = state['visualizers'][v]
            visualizer_class_name = visualizer['class_name']
            visualizer_class = getattr(sys.modules[__name__], visualizer_class_name)
            self.visualizers[v] = visualizer_class(self,visualizer['name'], serialized_state=visualizer )

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

    def unbind_methods(self):
        pass

    def dpg_delete_callback(self,sender,app_data,user_data):
        print('node dpg delete callback')
        dpg_node_attr_id = dpg.get_item_parent(sender)
        dpg_node_id = dpg.get_item_parent(dpg_node_attr_id)

        node_conf = dpg.get_item_configuration(dpg_node_id)
        print(str(node_conf))

        #dpg_attrs = dpg.get_item_children(dpg_node_id)
        #print(str(dpg_attrs))
        #for dpg_attr_id in dpg_attrs:
        #    dpg_attr = dpg_attrs[dpg_attr_id]
        #    for real_attr in dpg_attr:
        #        dpg_conf = dpg.get_item_configuration(real_attr)
        #        print(str(dpg_conf))

        #TODO delete input links
        #TODO delete output links
        del self.inputs[:]
        del self.outputs[:]
        #del self.actions[:]
        #del self.visualizers[:]

        self.unbind_methods()

        print('Delete node callback : '+self.get_name())

        self.parent_meta_node.delete_node(self.get_uuid())

        dpg.delete_item(dpg_node_id)

    def dpg_render_node(self):
        print('dpg_render_node')

        print('pre render node has ' + str(sys.getrefcount(self)) + ' references')
        refs = gc.get_referrers(self)
        for r in refs:
            print('ref: ' + str(r))

        self.dpg_node_id = dpg.add_node(label = self.get_name(), pos=self.get_position(), parent=self.parent_meta_node.dpg_get_node_editor_id(), user_data={'node_uuid': self.get_uuid()})

        print(' dpg_node_id = '+str(self.dpg_node_id))
        print('user data of node = '+str(dpg.get_item_user_data(self.dpg_node_id)))

        for input in self.inputs:
            input.dpg_render()

        for visualizer in self.visualizers: #TODO render visualizers
            self.visualizers[visualizer].dpg_render()

        for output in self.outputs:
            output.dpg_render()

        self.fake_action_attribute_id = dpg.add_node_attribute(parent=self.dpg_node_id, attribute_type=dpg.mvNode_Attr_Static)

        #weak_dpg_delete_callback = weakref.WeakMethod(self.dpg_delete_callback)

        dpg.add_button(label='x', callback=(lambda a,b,c: self.dpg_delete_callback(a,b,c)), parent=self.fake_action_attribute_id)
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
            dpg.add_button(label=self.actions[action], callback=(lambda a,b,c: self.dpg_action_callback(a,b,c)), user_data=action, parent=self.fake_action_attribute_id)


        print('post render node has ' + str(sys.getrefcount(self)) + ' references')
        refs = gc.get_referrers(self)
        for r in refs:
            print('ref: ' + str(r))


    def get_class_name(self):
        return type(self).__name__
