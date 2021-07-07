import dearpygui.dearpygui as dpg
from helpers import *


class Node:
    def __init__(self, parent_meta_node=None, serialized_state=None):
        self.parent_meta_node = parent_meta_node
        self.uuid = gen_uuid()
        self.name = self.get_class_name()

        self.inputs = {}
        self.outputs = {}
        self.stage = 0
        self.position = [10,10]

        self.fresh = False

        if serialized_state:
            self.deserialize(serialized_state)
        else:
            self.initialize_values()

        print(self.parent_meta_node)

        if self.parent_meta_node and self.should_render_node:
            self.dpg_render_node()

    def initialize_values(self):
        pass

    def get_name(self):
        return self.name

    def get_uuid(self):
        return self.uuid

    def set_fresh(self,is_fresh):
        self.fresh = is_fresh

    def is_fresh(self):
        fresh = self.fresh
        #TODO - check if params are fresh too
        return fresh

    def set_stage(self, stage):
        self.stage = stage
        LOG.log(self.get_name() + "\t changed stage to: " + self.get_stage_name(stage))

    def get_input_by_name(self,name):
        for i in self.inputs:
            if self.inputs[i].getName() == name:
                return self.inputs[i]

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
        state['inputs']={}
        state['outputs']={}

        for input in self.inputs:
            state['inputs'][input]=self.inputs[input].serialize()

        for output in self.outputs:
            state['outputs'][output]=self.outputs[output].serialize()


        pass

    def deserialize(self,state):

        for input in state['inputs']:
            input_class_name = state['inputs'][input]['class_name']
            input_class = getattr(sys.modules[__name__], input_class_name)
            self.inputs[input] = input_class(self,serialized_state=state['inputs'][input])

        self.set_position(state['position'])
        self.fresh = False

        pass

    def get_position(self):
        return self.position

    def default_executor(self):
        return None

    def get_dpg_node_id(self):
        return self.dpg_node_id

    def dpg_render_node(self):
        self.dpg_node_id = dpg.add_node(label = self.get_name(), pos=self.get_position(), parent=self.parent_meta_node.dpg_get_node_editor_id())

        for input in self.inputs:
            self.inputs[input].dpg_render()

        for output in self.outputs:
            self.outputs[output].dpg_render()

    def get_class_name(self):
        return type(self).__name__

class InConn():
    def __init__(self,parent_node,name='',default_value=None, serialized_state=None):
        self.parent_node = parent_node
        self.name = name
        self.value = default_value
        self.uuid = gen_uuid()

        self.connected_node_uuid = ''
        self.connected_node_out_uuid = ''

        #self.dpg_render()
    def get_class_name(self):
        return type(self).__name__

    def is_fresh(self):
        pass

    def connect_to(self):
        pass

    def get_value(self):
        return self.value

    def set_value(self):
        return self.value

    def get_name(self):
        return self.name

    def get_uuid(self):
        return self.uuid

    def dpg_render(self):
        parent_node_id = self.parent_node.get_dpg_node_id()
        self.dpg_attribute_id = dpg.add_node_attribute(parent=parent_node_id)
        self.gpg_text_id = dpg.add_text(self.get_name(), parent=self.dpg_attribute_id)

class InConnInt(InConn):
    def __init__(self,parent_node,name='',default_value=None,serialized_state=None,min=0,max=100):
        super().__init__(parent_node,name,default_value,serialized_state)
        
        self.max = max
        self.min = min

        if serialized_state:
            self.deserialize(serialized_state)
    
    def serialize(self):
        state = {}
        state['name']=self.get_name()
        state['class_name'] = self.get_class_name()
        state['value'] = self.value
        state['max']=max
        state['min']=min
        state['uuid']=self.get_uuid()
        return state;

    def deserialize(self):
        state = {}
        self.name = state['name']
        self.value = state['value']
        self.max = state['max']
        self.min = state['min']
        self.uuid = state['uuid']

    def dpg_render(self):
        parent_node_id = self.parent_node.get_dpg_node_id()
        self.dpg_attribute_id = dpg.add_node_attribute(parent=parent_node_id)
        self.gpg_input_id = dpg.add_input_int(label=self.get_name(), default_value=self.get_value(), width=75, parent=self.dpg_attribute_id, max_value=self.max, min_value=self.min )

class OutConn():
    def __init__(self,parent_node,name,value_executor):
        self.parent_node = parent_node
        self.name = name
        self.uuid = gen_uuid()
        self.value_executor = value_executor

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

class ViAdd(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

    def initialize_values(self):
        self.should_render_node = True
        self.inputs = {'a': InConnInt(self,'number a',1,0,100), 'b': InConnInt(self,'number b',1,0,100) }
        self.outputs = {'result': OutConn(self,'result', self.default_executor)}

    def default_executor(self):
        a = self.inputs['a'].get_value()
        b = self.inputs['b'].get_value()
        result = a+b
        return result


class MetaNode(Node):
    def __init__(self,  parent_meta_node=None, serialized_state='', parent_workspace=None):
        self.parent_workspace = parent_workspace
        self.nodes = {}

        self.should_render_editor = True
        self.should_render_node = False
        
        super().__init__(parent_meta_node, serialized_state)


    def initialize_values(self):    #TODO: Separate initialize_values from render
        self.dpg_render_editor()

    def render_node(self):
        pass

    def add_node(self,node_class):
        pass

    def add_node_callback(self, sender, app_data, user_data):
        LOG.log('add_node_callback sender '+ str(sender))
        LOG.log('add_node_callback app_data ' + str(app_data))
        LOG.log('add_node_callback user_data '+ str(user_data))

        self.add_node_to_editor(user_data['node_class'])
    
    def add_node_to_editor(self, node_class):
        LOG.log('add_node_to_editor: '+str(node_class))
        new_node = node_class(parent_meta_node=self)

        self.nodes[new_node.get_uuid()] = new_node
    
    def dpg_get_node_editor_id(self):
        return self.dpg_node_editor_id

    def dpg_render_editor(self):
        self.dpg_window_id = dpg.add_window(label=self.get_name(), width=800, height=600, pos=(50, 50))

        self.dpg_menu_bar_id = dpg.add_menu_bar(label='Workspace menu bar', parent=self.dpg_window_id)
        self.dpg_meta_node_menu_id = dpg.add_menu(label='MetaNode', parent=self.dpg_menu_bar_id)
        dpg.add_menu_item(label='Load MetaNode', parent=self.dpg_meta_node_menu_id)#TODO load meta_node
        dpg.add_menu_item(label='Save MetaNode', parent=self.dpg_meta_node_menu_id)#TODO save meta_node
        dpg.add_menu_item(label='Save MetaNode As...', parent=self.dpg_meta_node_menu_id)#TODO save as meta_node

        self.dpg_add_node_menu_id = dpg.add_menu(label='Add Node...', parent=self.dpg_menu_bar_id)

        #self.parent_workspace.dpg_render_available_nodes_to(self.dpg_add_node_menu_id, self)
        avaliable_nodes = self.parent_workspace.get_available_nodes()
        self.dpg_render_available_nodes_to(avaliable_nodes,self.dpg_add_node_menu_id)
        #self.parent_workspace.dpg_render_available_nodes_to(self.dpg_add_node_menu_id, (lambda self: lambda arg1, arg2: self.add_node_callback(arg1, arg2))(self))

        self.dpg_node_editor_id = dpg.add_node_editor(parent=self.dpg_window_id)

        #self.dpg_popup_id = dpg.popup(self.dpg_node_editor_id)
        #self.dpg_popup_id = dpg.window(label='Rightclick fake window', modal=True)
        #self.dpg_popup_menu_bar_id = dpg.add_menu_bar(label='Rightclick menu bar', parent=self.dpg_popup_id)
        #self.dpg_right_click_menu_id = dpg.add_menu(label='right click menu', parent=self.dpg_popup_menu_bar_id)
        #dpg.add_menu_item(label='Add some node', parent=self.dpg_right_click_menu_id)  # TODO add some node

        self.dpg_is_rendered = True

    def dpg_render_available_nodes_to(self,nodes,dpg_parent):
        for n in nodes:
            LOG.log(n,type(nodes[n]))
            if type(nodes[n]) is dict:
                menu_item_id = dpg.add_menu(label=n, parent=dpg_parent)
                self.dpg_render_available_nodes_to(nodes[n],menu_item_id)
            else:
                if nodes[n] is not None:
                    print('nodes[n]'+ str(nodes[n]))

                    menu_item_id = dpg.add_menu_item(label=n, parent=dpg_parent, callback=self.add_node_callback, user_data={'node_class': nodes[n]})
                else:
                    menu_item_id = dpg.add_menu_item(label=n, parent=dpg_parent)

    def dpg_right_click_menu(self):
        pass

    def saveStatusToFile(self): #TODO save
        pass

    def serialize(self):
        status = {}
        status['dpg_is_rendered'] = self.dpg_is_rendered
        if self.dpg_is_rendered:
            status['dpg_window_width'] = dpg.get_item_width(self.dpg_window_id)
            status['dpg_window_height'] = dpg.get_item_height(self.dpg_window_id)
            status['dpg_window_pos'] = dpg.get_item_pos(self.dpg_window_id)
        
        return status

    def deserialize(self, status):
        self.dpg_is_rendered = status['dpg_is_rendered']
        if self.dpg_is_rendered:
            self.dpg_render_editor()
            dpg.set_item_width(self.dpg_window_id,status['dpg_window_width'])
            dpg.set_item_height(self.dpg_window_id,status['dpg_window_height'])
            dpg.set_item_pos(self.dpg_window_id,status['dpg_window_pos'])



class Workspace:
    def __init__(self):
        self.uuid = uuid.uuid1()
        self.nodes_classes = {} 
        self.nodes_available = {'math': {'add': ViAdd, 'sub': None, 'advanced': {'sqrt': None}}, 'AI':{'pytorch': None} }
        self.filepath = DEFAULT_WORKSPACE_SAVE_PATH

        self.meta_nodes = {}    #maps uuid to objects

    def create_new_meta_node(self, uuid='', status=''):
        node = None

        LOG.log('creating new meta_node. parent =', str(self))

        if uuid != '' and status != '':
            node = MetaNode(uuid, status, parent_workspace=self)
        else:
            node = MetaNode(parent_workspace=self)

        meta_node_uuid = node.get_uuid()

        self.meta_nodes[meta_node_uuid]=node

    def get_available_nodes(self):
        return self.nodes_available

    def get_element_by_uuid(self,uuid):#TODO get element by uuid
        pass

    def dpg_save_status_to_file_callback(self, param):
        self.save_status_to_file(self.filepath)
        
    def dpg_load_status_from_file_callback(self, param):
        self.load_status_from_file()

    def load_status_from_file(self, filepath=''):
        if filepath == '':
            filepath = self.filepath
        self.filepath = filepath

        status = load_data(filepath)

        if status != None:
            self.deserialize(status)
            LOG.log('loaded file:' + filepath + 'and get status:' + str(status))

    def save_status_to_file(self, filepath=''):
        if filepath == '':
            filepath = self.filepath

        serializedStatus = self.serialize()

        save_data(serializedStatus,filepath)

        pass

    def serialize(self):
        status = {}
        status['nodes_available'] = self.nodes_available
        meta_nodes_status={}
        for mn in self.meta_nodes:
            meta_nodes_status[mn] = self.meta_nodes[mn].serialize()

        status['meta_nodes_status']=meta_nodes_status

        LOG.log(str(status))

        return status

    def deserialize(self,status):
        #TODO should delete all existing meta nodes first
        LOG.log(status)
        self.nodes_available = status['nodes_available']
        meta_nodes_status = status['meta_nodes_status']
        for mns in meta_nodes_status:
            self.create_new_meta_node(mns,meta_nodes_status[mns])

    def new_meta_node_callback(self,cbdata):
        self.create_new_meta_node()



WORKSPACE = Workspace()
DPG_PRIMARY_WINDOW_ID = dpg.add_window(label="vipy3", width=800, height=800, pos=(100, 100) )
dpg_menu_bar_id = dpg.add_menu_bar(label='Workspace menu bar', parent=DPG_PRIMARY_WINDOW_ID)
dpg_workspace_menu_id = dpg.add_menu(label='Workspace', parent=dpg_menu_bar_id)

dpg.add_menu_item(label='New Workspace', parent=dpg_workspace_menu_id)#TODO new workspace
dpg.add_menu_item(label='Load Last Workspace', parent=dpg_workspace_menu_id,callback=WORKSPACE.dpg_load_status_from_file_callback)
dpg.add_menu_item(label='Load Workspace...', parent=dpg_workspace_menu_id)#TODO load workspace
dpg.add_menu_item(label='Save Workspace', parent=dpg_workspace_menu_id, callback=WORKSPACE.dpg_save_status_to_file_callback)
dpg.add_menu_item(label='Save Workspace As...', parent=dpg_workspace_menu_id)#TODO save as workspace
dpg.add_menu_item(label='New MetaNode', parent=dpg_workspace_menu_id, callback=WORKSPACE.new_meta_node_callback)#TODO new MetaNode
dpg.add_menu_item(label='Load MetaNode', parent=dpg_workspace_menu_id)#TODO load MetaNode

dpg.set_primary_window(DPG_PRIMARY_WINDOW_ID, True)


#Default to speed up the work:
#WORKSPACE.load_status_from_file()

dpg.start_dearpygui()

