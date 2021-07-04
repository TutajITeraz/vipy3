import dearpygui.dearpygui as dpg
from helpers import *


class Node:
    def __init__(self, meta_node_uuid=None, serialized_state=None):
        self.meta_node_uuid = meta_node_uuid
        self.uuid = gen_uuid()
        self.name = self.get_class_name()

        self.inputs = []
        self.outputs = {}
        self.stage = 0

        self.fresh = False

        if serialized_state:
            self.deserialize(serialized_state)
        else:
            self.initialize_values()

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

    def get_workspace(self):
        return self.workspace

    def serialize(self):
        pass

    def deserialize(self):
        pass

    def render_node(self):
        pass

    def get_class_name(self):
        return type(self).__name__

class InConn():
    def __init__(self,parent_node,name,default_value):
        self.parent_node = parent_node
        self.name = name
        self.value = default_value
        self.uuid = gen_uuid()

        self.connected_node_uuid = ''
        self.connected_node_out_uuid = ''

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

    def get_type(self):
        return self.type

    def get_uuid(self):
        return self.uuid

    def dpg_render(self):
        pass

class InConnInt():
    def __init__(self,parent_node,name,default_value,min=0,max=100):
        super().__init__(self,parent_node,name,default_value)
        self.max = max
        self.min = min

    def dpg_render(self):
        pass


class ViAdd(Node):
    def __init__(self, workspace, uuid='', serialized_state=''):
        super().__init__(self, workspace, uuid, serialized_state, )

    def initialize_values(self):
        self.inputs = [InConnInt(self,'number_a',1,0,100),InConnInt(self,'number_b',1,0,100) ]
        self.outputs = {}



class MetaNode(Node):
    def __init__(self,  meta_node_uuid='', serialized_state='', parent_workspace=None):
        super().__init__(meta_node_uuid, serialized_state)

        self.nodes = {}
        LOG.log("parent_workspace:"+str(parent_workspace))
        self.parent_workspace = parent_workspace

    def initialize_values(self):    #TODO: Separate initialize_values from render
        self.dpg_render_editor()

    def render_node(self):
        pass

    def add_node(self,node_class):
        pass

    def add_node_callback(self,callback_data):
        LOG.log(callback_data)

    def dpg_render_editor(self):
        self.dpg_window_id = dpg.add_window(label=self.get_name(), width=800, height=600, pos=(50, 50))

        self.dpg_menu_bar_id = dpg.add_menu_bar(label='Workspace menu bar', parent=self.dpg_window_id)
        self.dpg_meta_node_menu_id = dpg.add_menu(label='MetaNode', parent=self.dpg_menu_bar_id)
        dpg.add_menu_item(label='Load MetaNode', parent=self.dpg_meta_node_menu_id)#TODO load meta_node
        dpg.add_menu_item(label='Save MetaNode', parent=self.dpg_meta_node_menu_id)#TODO save meta_node
        dpg.add_menu_item(label='Save MetaNode As...', parent=self.dpg_meta_node_menu_id)#TODO save as meta_node

        self.dpg_add_node_menu_id = dpg.add_menu(label='Add Node...', parent=self.dpg_menu_bar_id)
        self.parent_workspace.dpg_render_available_nodes_to(self.dpg_add_node_menu_id,self.add_node_callback)

        self.dpg_node_editor_id = dpg.add_node_editor(parent=self.dpg_window_id)

        #self.dpg_popup_id = dpg.popup(self.dpg_node_editor_id)
        #self.dpg_popup_id = dpg.window(label='Rightclick fake window', modal=True)
        #self.dpg_popup_menu_bar_id = dpg.add_menu_bar(label='Rightclick menu bar', parent=self.dpg_popup_id)
        #self.dpg_right_click_menu_id = dpg.add_menu(label='right click menu', parent=self.dpg_popup_menu_bar_id)
        #dpg.add_menu_item(label='Add some node', parent=self.dpg_right_click_menu_id)  # TODO add some node

        self.dpg_is_rendered = True

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

    def dpg_render_available_nodes_to(self,dpg_parent,callback,nodes=None):
        if not nodes:
            nodes = self.get_available_nodes()

        for n in nodes:
            LOG.log(n,type(nodes[n]))
            if type(nodes[n]) is dict:
                menu_item_id = dpg.add_menu(label=n, parent=dpg_parent)
                self.dpg_render_available_nodes_to(menu_item_id,callback,nodes=nodes[n])
            else:
                if nodes[n] is not None:
                    menu_item_id = dpg.add_menu_item(label=n, parent=dpg_parent, callback=callback)
                else:
                    menu_item_id = dpg.add_menu_item(label=n, parent=dpg_parent)

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

