import dearpygui.dearpygui as dpg

with dpg.window(label="Tutorial", width=400, height=400) as mainwindow:
    class TestClass:
        def __init__(self):
            print('this should never be called')


    def some_callback(sender, app_data, user_data):
        print('any callback ')


    DPG_PRIMARY_WINDOW_ID = dpg.add_window(label='test', width=800, height=600, pos=[50, 50])
    with dpg.menu_bar(parent=DPG_PRIMARY_WINDOW_ID):
        with dpg.menu(label="File"):
            menu_item_id = dpg.add_menu_item(label='xxx', callback=some_callback, user_data=lambda: TestClass)

dpg.set_primary_window(mainwindow, True)
dpg.start_dearpygui()