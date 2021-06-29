import dearpygui.dearpygui as dpg
from dearpygui.demo import show_demo
show_demo()
dpg.start_dearpygui()

with dpg.window(label="vipy3", width=800, height=800, pos=(100, 100), ) as demo_id:
    with dpg.menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="New")
            dpg.add_menu_item(label="Open")