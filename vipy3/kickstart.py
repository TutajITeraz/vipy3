import dearpygui.dearpygui as dpg
from .core import *
from .simple_nodes import *

#RUN: /usr/bin/python3 -m vipy3.kickstart

dpg.setup_viewport()
dpg.set_viewport_title(title='ViPy3')
dpg.set_viewport_width(1400)
dpg.set_viewport_height(600)
dpg.set_viewport_pos([1,1])

WORKSPACE = Workspace()
nodes_available = {'math': {'add': ViAdd, 'sub': None, 'advanced': {'sqrt': None}}, 'AI':{'pytorch': None} }
WORKSPACE.add_nodes_available(nodes_available)

DPG_PRIMARY_WINDOW_ID = dpg.add_window(label="vipy3", width=800, height=800, pos=(100, 100) )
dpg_menu_bar_id = dpg.add_menu_bar(label='Workspace menu bar', parent=DPG_PRIMARY_WINDOW_ID)
dpg_workspace_menu_id = dpg.add_menu(label='Workspace', parent=dpg_menu_bar_id)

#dpg.add_menu_item(label='New Workspace', parent=dpg_workspace_menu_id)#TODO new workspace
dpg.add_menu_item(label='Load Last Workspace', parent=dpg_workspace_menu_id,callback=WORKSPACE.dpg_load_status_from_file_callback)
#dpg.add_menu_item(label='Load Workspace...', parent=dpg_workspace_menu_id)#TODO load workspace
dpg.add_menu_item(label='Save Workspace', parent=dpg_workspace_menu_id, callback=WORKSPACE.dpg_save_status_to_file_callback)
#dpg.add_menu_item(label='Save Workspace As...', parent=dpg_workspace_menu_id)#TODO save as workspace
dpg.add_menu_item(label='New MetaNode', parent=dpg_workspace_menu_id, callback=WORKSPACE.new_meta_node_callback)#TODO new MetaNode
#dpg.add_menu_item(label='Load MetaNode', parent=dpg_workspace_menu_id)#TODO load MetaNode


dpg_debug_menu = dpg.add_menu(label='Debug', parent=dpg_menu_bar_id)
dpg.add_menu_item(label="Show Documentation", callback=lambda: dpg.show_tool(dpg.mvTool_Doc), parent=dpg_debug_menu)
dpg.add_menu_item(label="Show Debug", callback=lambda: dpg.show_tool(dpg.mvTool_Debug), parent=dpg_debug_menu)
dpg.add_menu_item(label="Show Style Editor", callback=lambda: dpg.show_tool(dpg.mvTool_Style), parent=dpg_debug_menu)
dpg.add_menu_item(label="Show Font Manager", callback=lambda: dpg.show_tool(dpg.mvTool_Font), parent=dpg_debug_menu)
dpg.add_menu_item(label="Show Item Registry", callback=lambda: dpg.show_tool(dpg.mvTool_ItemRegistry), parent=dpg_debug_menu)
dpg.add_menu_item(label="Show ImGui Demo", callback=lambda: dpg.show_imgui_demo(), parent=dpg_debug_menu)

dpg.set_primary_window(DPG_PRIMARY_WINDOW_ID, True)

#viewport_conf = dpg.get_viewport_configuration()
#dpg.set_viewport_title("viiiiipy")

#Default to speed up the work:
WORKSPACE.load_status_from_file()

dpg.start_dearpygui()

