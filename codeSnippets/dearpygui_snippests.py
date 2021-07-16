## Change style

with dpg.theme() as theme:
    dpg.add_theme_color(dpg.mvThemeCol_Button, _hsv_to_rgb(i/7.0, 0.6, 0.6))
    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, _hsv_to_rgb(i/7.0, 0.8, 0.8))
    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, _hsv_to_rgb(i/7.0, 0.7, 0.7))
    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, i*5)
    dpg.add_theme_style(dpg.mvStyleVar_FramePadding, i*3, i*3)

dpg.add_button(label="Click", callback=_log)
dpg.set_item_theme(dpg.last_item(), theme)

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

#Loading indicator:

            with dpg.tree_node(label="Loading Indicators"):

                dpg.add_loading_indicator()
                dpg.add_same_line()
                dpg.add_loading_indicator(style=1)