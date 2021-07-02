import dearpygui.dearpygui as dpg
from helpers import *

class Node:
    def __init__(self, meta_node=None, serialized_state=None):
        self.uuid = gen_uuid()
        self.meta_node=meta_node

        if serialized_state:
            self.deserialize()

    def getUuid(self):
        return self.uuid

    def serialize(self):
        pass

    def deserialize(self):
        pass

    def render_node(self,parent_node_editor):
        pass

    def get_class_name(self):
        return type(self).__name__

class MetaNode(Node):
    def __init__(self, workspace, uuid='',serialized_state=''):
        super().__init__()
        self.parent_workspace = workspace
        self.name = self.get_class_name()

        if uuid != '':
            self.uuid = uuid

        self.dpg_render_editor()

        if serialized_state != '':
            self.deserialize(serialized_state)

    def get_name():
        return self.name

    def render_node(self):
        pass

    def dpg_render_editor(self):
        self.dpg_window_id = dpg.add_window(label=self.uuid, width=800, height=600, pos=(50, 50))

        self.dpg_menu_bar_id = dpg.add_menu_bar(label='Workspace menu bar', parent=self.dpg_window_id)
        self.dpg_meta_node_menu_id = dpg.add_menu(label='MetaNode', parent=self.dpg_menu_bar_id)
        dpg.add_menu_item(label='Load MetaNode', parent=self.dpg_meta_node_menu_id)#TODO load meta_node
        dpg.add_menu_item(label='Save MetaNode', parent=self.dpg_meta_node_menu_id)#TODO save meta_node
        dpg.add_menu_item(label='Save MetaNode As...', parent=self.dpg_meta_node_menu_id)#TODO save as meta_node

        self.dpg_add_node_menu_id = dpg.add_menu(label='Add Node...', parent=self.dpg_menu_bar_id)

        self.parent_workspace.dpg_render_available_nodes_to(self.dpg_add_node_menu_id)

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
        status['dpg_window_width'] = dpg.get_item_width(self.dpg_window_id)
        status['dpg_window_height'] = dpg.get_item_height(self.dpg_window_id)
        #status['dpg_window_pos'] = dpg.get_item_pos(self.dpg_window_id)
        
        return status

    def deserialize(self, status):
        dpg.set_item_width(self.dpg_window_id,status['dpg_window_width'])
        dpg.set_item_height(self.dpg_window_id,status['dpg_window_height'])




class Workspace:
    def __init__(self):
        self.uuid = uuid.uuid1()
        self.nodes_classes = {} 
        self.nodes_available = {'math': {'add': None, 'sub': None, 'advanced': {'sqrt': None}}, 'AI':{'pytorch': None} }
        self.filepath = DEFAULT_WORKSPACE_SAVE_PATH

        self.meta_nodes = {}    #maps uuid to objects

    def create_new_meta_node(self, uuid='', status=''):
        node = None

        if uuid != '' and status != '':
            node = MetaNode(self, uuid, status)
        else:
            node = MetaNode(self)

        meta_node_uuid = node.getUuid()

        self.meta_nodes[meta_node_uuid]=node

    def get_available_nodes(self):
        return self.nodes_available

    def dpg_render_available_nodes_to(self,parent,nodes=None):
        if not nodes:
            nodes = self.get_available_nodes()

        for n in nodes:
            LOG.log(n,type(nodes[n]))
            if type(nodes[n]) is dict:
                menu_item_id = dpg.add_menu(label=n, parent=parent)
                self.dpg_render_available_nodes_to(menu_item_id,nodes=nodes[n])
            else:
                menu_item_id = dpg.add_menu_item(label=n, parent=parent)

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
        LOG.log('loaded file:'+filepath+'and get status:'+str(status))

        self.deserialize(status)

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
dpg.add_menu_item(label='Load Last Workspace', parent=dpg_workspace_menu_id,callback=WORKSPACE.dpg_load_status_from_file_callback)#TODO load workspace
dpg.add_menu_item(label='Load Workspace...', parent=dpg_workspace_menu_id)#TODO load workspace
dpg.add_menu_item(label='Save Workspace', parent=dpg_workspace_menu_id, callback=WORKSPACE.dpg_save_status_to_file_callback)
dpg.add_menu_item(label='Save Workspace As...', parent=dpg_workspace_menu_id)#TODO save as workspace
dpg.add_menu_item(label='New MetaNode', parent=dpg_workspace_menu_id, callback=WORKSPACE.new_meta_node_callback)#TODO new MetaNode
dpg.add_menu_item(label='Load MetaNode', parent=dpg_workspace_menu_id)#TODO load MetaNode

dpg.set_primary_window(DPG_PRIMARY_WINDOW_ID, True)

dpg.start_dearpygui()

