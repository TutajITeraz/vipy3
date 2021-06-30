import dearpygui.dearpygui as dpg
from helpers import *

class Node:
    def __init__(self):
        self.uuid = gen_uuid()

    def render_node(self,parent_node_editor):
        pass

    def get_class_name(self):
        return type(self).__name__

class MetaNode(Node):
    def __init__(self, workspace):
        super().__init__()
        self.parent_workspace = workspace

        self.dpg_render_editor()


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



class Workspace:
    def __init__(self):
        self.uuid = uuid.uuid1()
        self.nodes_available = {'math': {'add': None, 'sub': None, 'advanced': {'sqrt': None}}, 'AI':{'pytorch': None} }

        self.meta_nodes = []

    def create_new_meta_node(self):
        module = MetaNode(self)

        self.meta_nodes.append(module)

    def get_available_nodes(self):
        return self.nodes_available

    def dpg_render_available_nodes_to(self,parent,nodes=None):
        if not nodes:
            nodes = self.get_available_nodes()

        for n in nodes:
            print(n,type(nodes[n]))
            if type(nodes[n]) is dict:
                menu_item_id = dpg.add_menu(label=n, parent=parent)
                self.dpg_render_available_nodes_to(menu_item_id,nodes=nodes[n])
            else:
                menu_item_id = dpg.add_menu_item(label=n, parent=parent)

    def get_element_by_uuid(self,uuid):#TODO get element by uuid
        pass



WORKSPACE = Workspace()
DPG_PRIMARY_WINDOW_ID = dpg.add_window(label="vipy3", width=800, height=800, pos=(100, 100) )
dpg_menu_bar_id = dpg.add_menu_bar(label='Workspace menu bar', parent=DPG_PRIMARY_WINDOW_ID)
dpg_workspace_menu_id = dpg.add_menu(label='Workspace', parent=dpg_menu_bar_id)

dpg.add_menu_item(label='New Workspace', parent=dpg_workspace_menu_id)#TODO new workspace
dpg.add_menu_item(label='Load Workspace...', parent=dpg_workspace_menu_id)#TODO load workspace
dpg.add_menu_item(label='Save Workspace', parent=dpg_workspace_menu_id)#TODO save workspace
dpg.add_menu_item(label='Save Workspace As...', parent=dpg_workspace_menu_id)#TODO save as workspace
dpg.add_menu_item(label='New MetaNode', parent=dpg_workspace_menu_id, callback=WORKSPACE.create_new_meta_node)#TODO new MetaNode
dpg.add_menu_item(label='Load MetaNode', parent=dpg_workspace_menu_id)#TODO load MetaNode

dpg.set_primary_window(DPG_PRIMARY_WINDOW_ID, True)

dpg.start_dearpygui()

