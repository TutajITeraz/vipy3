import dearpygui.dearpygui as dpg
from .core import *
from .simple_nodes import *

#RUN: /usr/bin/python3 -m vipy3.kickstart

WORKSPACE = Workspace()
nodes_available = {'math': {'add': ViAdd, 'sub': None, 'advanced': {'sqrt': None}}, 'AI':{'pytorch': None} }
WORKSPACE.add_nodes_available(nodes_available)

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

