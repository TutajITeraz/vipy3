import dearpygui.dearpygui as dpg
import uuid

class Node:
    def __init__(self):
        self.uuid = uuid.uuid1()

    def render_node(self,parent_node_editor):
        pass

class MetaNode(Node):
    def __init__(self):
        super().__init__()
        self.render_editor()
        pass

    def render_node(self):
        pass

    def render_editor(self):
        self.dpg_window_id = dpg.add_window(label=self.uuid, width=800, height=800, pos=(100, 100))

        pass

class Workspace:
    def __init__(self):
        self.uuid = uuid.uuid1()
        self.modules = []

    def create_new_meta_node(self):
        module = MetaNode()

        self.modules.append(module)

WORKSPACE = Workspace()
DPG_PRIMARY_WINDOW_ID = dpg.add_window(label="vipy3", width=800, height=800, pos=(100, 100) )
dpg_menu_bar_id = dpg.add_menu_bar(label='Workspace menu bar', parent=DPG_PRIMARY_WINDOW_ID)
dpg_menu_id = dpg.add_menu(label='File', parent=dpg_menu_bar_id)

dpg_file_menu_id = dpg.add_menu_item(label='New MetaNode', parent=dpg_menu_id, callback=WORKSPACE.create_new_meta_node)
dpg.add_menu_item(label='Load MetaNode', parent=dpg_menu_id)
dpg.add_menu_item(label='Save MetaNode', parent=dpg_menu_id)
dpg.add_menu_item(label='Load Workspace', parent=dpg_menu_id)
dpg.add_menu_item(label='Save Workspace', parent=dpg_menu_id)

dpg.set_primary_window(DPG_PRIMARY_WINDOW_ID, True)

dpg.start_dearpygui()

