import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()
dpg.show_viewport()


def dpg_delete_node_callback(sender, app_data, user_data):
    print('node dpg delete callback')
    dpg_node_attr_id = dpg.get_item_parent(sender)
    dpg_node_id = dpg.get_item_parent(dpg_node_attr_id)
    dpg.delete_item(dpg_node_id)


with dpg.window(label="Test1", width=800, height=600) as mainwindow:

    node_editor_id = dpg.add_node_editor(callback=lambda sender, app_data: dpg.add_node_link(app_data[0], app_data[1], parent=sender),
                                         delink_callback=lambda sender, app_data: [print('delink callback fired'), dpg.delete_item(app_data)], parent=mainwindow)

    node_id1 = dpg.add_node(label="Node 1", pos=[
                            10, 10], parent=node_editor_id)
    node_id2 = dpg.add_node(label="Node 2", pos=[
                            120, 10], parent=node_editor_id)

    dpg_attribute_id1 = dpg.add_node_attribute(
        parent=node_id1, user_data='one', attribute_type=dpg.mvNode_Attr_Output)
    dpg_text_id1 = dpg.add_text('out', parent=dpg_attribute_id1)

    dpg_attribute_id2 = dpg.add_node_attribute(
        parent=node_id2, user_data='two')
    dpg_text_id2 = dpg.add_text('in', parent=dpg_attribute_id2)

    dpg.add_button(label='delete', callback=(lambda a, b, c: dpg_delete_node_callback(a, b, c)),
                   parent=dpg_attribute_id1)

    dpg_edit_button_id = dpg.add_button(label='edit', parent=dpg_attribute_id1)

    # Edit modal:
    with dpg.popup(dpg_edit_button_id, modal=True, mousebutton=dpg.mvMouseButton_Left) as modal_id:
        dpg.add_text(
            "Node names should be unique if you want to generate code")
        dpg_new_name_input_id = dpg.add_input_text(
            parent=modal_id, label='name', default_value='some name')
        dpg.add_separator()
        dpg.add_button(label="OK", width=75, callback=lambda: [print(dpg.get_value(
            dpg_new_name_input_id)), dpg.configure_item(modal_id, show=False)])
        dpg.add_same_line()
        dpg.add_button(label="Cancel", width=75,
                       callback=lambda: dpg.configure_item(modal_id, show=False))

dpg.start_dearpygui()
