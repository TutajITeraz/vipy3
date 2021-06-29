## Change style

with dpg.theme() as theme:
    dpg.add_theme_color(dpg.mvThemeCol_Button, _hsv_to_rgb(i/7.0, 0.6, 0.6))
    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, _hsv_to_rgb(i/7.0, 0.8, 0.8))
    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hsv_to_rgb(i/7.0, 0.7, 0.7))
    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, i*5)
    dpg.add_theme_style(dpg.mvStyleVar_FramePadding, i*3, i*3)

dpg.add_button(label="Click", callback=_log)
dpg.set_item_theme(dpg.last_item(), theme)


## Node editor

        with dpg.collapsing_header(label="Node Editor"):

            dpg.add_text("Ctrl+Click to remove a link.", bullet=True)

            with dpg.node_editor(callback=lambda sender, app_data: dpg.add_node_link(app_data[0], app_data[1], parent=sender), 
                             delink_callback=lambda sender, app_data: dpg.delete_item(app_data)):

                with dpg.node(label="Node 1", pos=[10, 10]):

                    with dpg.node_attribute():
                        dpg.add_input_float(label="F1", width=150)

                    with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
                        dpg.add_input_float(label="F2", width=150)

                with dpg.node(label="Node 2", pos=[300, 10]):

                    with dpg.node_attribute() as na2:
                        dpg.add_input_float(label="F3", width=200)

                    with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
                        dpg.add_input_float(label="F4", width=200)

                with dpg.node(label="Node 3", pos=[25, 150]):                                  
                    with dpg.node_attribute():
                        dpg.add_input_text(label="T5", width=200)
                    with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static): 
                        dpg.add_simple_plot(label="Node Plot", default_value=(0.3, 0.9, 2.5, 8.9), width=200, height=80, histogram=True)


## Modal and file

            with dpg.tree_node(label="Modals"):
                dpg.add_text("Modal windows are like popups but the user cannot close them by clicking outside.")
                dpg.add_button(label="Delete..")
                with dpg.popup(dpg.last_item(), modal=True, mousebutton=dpg.mvMouseButton_Left) as modal_id:
                    dpg.add_text("All those beautiful files will be deleted.\nThis operation cannot be undone!")
                    dpg.add_separator()
                    dpg.add_checkbox(label="Don't ask me next time")
                    dpg.add_button(label="OK", width=75, callback=lambda: dpg.configure_item(modal_id, show=False))
                    dpg.add_same_line()
                    dpg.add_button(label="Cancel", width=75, callback=lambda: dpg.configure_item(modal_id, show=False))

            with dpg.tree_node(label="File/Directory Selector"):

                with dpg.file_dialog(label="Demo File Dialog", show=False, callback=lambda s, a, u : print(s, a, u)):
                    dpg.add_file_extension(".*", color=(255, 255, 255, 255))
                    dpg.add_file_extension(".cpp", color=(255, 255, 0, 255))
                    dpg.add_file_extension(".h", color=(255, 0, 255, 255))
                    dpg.add_file_extension(".py", color=(0, 255, 0, 255))
                    #dpg.add_button(label="Button on file dialog")

                dpg.add_button(label="Show File Selector", user_data=dpg.last_container(), callback=lambda s, a, u: dpg.configure_item(u, show=True))


## Dynamic textures:


def _create_dynamic_textures():
    
    ## create dynamic textures
    texture_data1 = []
    for i in range(0, 100*100):
        texture_data1.append(255/255)
        texture_data1.append(0)
        texture_data1.append(255/255)
        texture_data1.append(255/255)

    texture_data2 = []
    for i in range(0, 50*50):
        texture_data2.append(255/255)
        texture_data2.append(255/255)
        texture_data2.append(0)
        texture_data2.append(255/255)

    dpg.add_dynamic_texture(100, 100, texture_data1, parent=demo_texture_container, id=demo_dynamic_texture_1)
    dpg.add_dynamic_texture(50, 50, texture_data2, parent=demo_texture_container, id=demo_dynamic_texture_2)

def _update_dynamic_textures(sender, app_data, user_data):

    new_color = dpg.get_value(sender)
    new_color[0] = new_color[0]/255
    new_color[1] = new_color[1]/255
    new_color[2] = new_color[2]/255
    new_color[3] = new_color[3]/255

    if user_data == 1:
        texture_data = []
        for i in range(0, 100*100):
            texture_data.append(new_color[0])
            texture_data.append(new_color[1])
            texture_data.append(new_color[2])
            texture_data.append(new_color[3])
        dpg.set_value(demo_dynamic_texture_1, texture_data)

    elif user_data == 2:
        texture_data = []
        for i in range(0, 50*50):
            texture_data.append(new_color[0])
            texture_data.append(new_color[1])
            texture_data.append(new_color[2])
            texture_data.append(new_color[3])
        dpg.set_value(demo_dynamic_texture_2, texture_data)

#Window:


#Right click menu:

            with dpg.tree_node(label="Popups"):

                dpg.add_text("When a popup is active, it inhibits interacting with windows that are behind the popup. Clicking outside the popup closes it.")
                b = dpg.add_button(label="Select..")
                dpg.add_same_line()
                t = dpg.add_text("<None>")
                with dpg.popup(b):
                    dpg.add_text("Aquariam")
                    dpg.add_separator()
                    dpg.add_selectable(label="Bream", user_data=[t, "Bream"], callback=lambda s, a, u: dpg.set_value(u[0], u[1]))
                    dpg.add_selectable(label="Haddock", user_data=[t, "Haddock"], callback=lambda s, a, u: dpg.set_value(u[0], u[1]))
                    dpg.add_selectable(label="Mackerel", user_data=[t, "Mackerel"], callback=lambda s, a, u: dpg.set_value(u[0], u[1]))
                    dpg.add_selectable(label="Pollock", user_data=[t, "Pollock"], callback=lambda s, a, u: dpg.set_value(u[0], u[1]))
                    dpg.add_selectable(label="Tilefish", user_data=[t, "Tilefish"], callback=lambda s, a, u: dpg.set_value(u[0], u[1]))

#Menu:

        with dpg.menu_bar():

            with dpg.menu(label="File"):

                dpg.add_menu_item(label="New")
                dpg.add_menu_item(label="Open")

                with dpg.menu(label="Open Recent"):

                    dpg.add_menu_item(label="harrel.c")
                    dpg.add_menu_item(label="patty.h")
                    dpg.add_menu_item(label="nick.py")

                dpg.add_menu_item(label="Save")
                dpg.add_menu_item(label="Save As...")

                with dpg.menu(label="Settings"):

                    dpg.add_menu_item(label="Option 1", callback=_log, user_data=logger)
                    dpg.add_menu_item(label="Option 2", check=True, callback=_log, user_data=logger)
                    dpg.add_menu_item(label="Option 3", check=True, default_value=True, callback=_log, user_data=logger)

                    with dpg.child(height=60, autosize_x=True, delay_search=True):
                        for i in range(0, 10):
                            dpg.add_text(f"Scolling Text{i}")

                    dpg.add_slider_float(label="Slider Float")
                    dpg.add_input_int(label="Input Int")
                    dpg.add_combo(("Yes", "No", "Maybe"), label="Combo")


#Loading indicator:

            with dpg.tree_node(label="Loading Indicators"):

                dpg.add_loading_indicator()
                dpg.add_same_line()
                dpg.add_loading_indicator(style=1)