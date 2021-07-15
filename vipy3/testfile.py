import dearpygui.dearpygui as dpg

with dpg.window(label="Tutorial1", width=400, height=400) as mainwindow:

    node_editor_id = dpg.add_node_editor(callback=lambda sender, app_data: dpg.add_node_link(app_data[0], app_data[1], parent=sender), 
                             delink_callback=lambda sender, app_data: dpg.delete_item(app_data), parent= mainwindow)

    node_id = dpg.add_node(label="Node 1", pos=[10, 10], parent= node_editor_id)

    dpg.add_button(label='edit', parent=mainwindow)

dpg.start_dearpygui()
