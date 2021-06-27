from dearpygui.core import *
from dearpygui.simple import *
from vinode import *
from vinodes import *
from vitorch import *
from datetime import datetime
import time
import threading
import json
import pickle
from os.path import expanduser

DEFAULT_FOLDER = expanduser('~/pydata/')


# virtualenv /usr/bin/python3 use global

# add_additional_font("data/fonts/chaney/chaney_wide_italic.ttf", size= 12)

# print(str(forek.play()))

# exit()


def demo_main_callback(sender, data):
    set_value("Mouse Position##demo", str(get_mouse_pos()))


def on_demo_close(sender, data):
    delete_item("Dear PyGui Demo")
    if does_item_exist("Logging Widget On Window##demo"):
        delete_item("Logging Widget On Window##demo")


def show_demo():
    def get_link_info(sender, data):
        print("Selected Nodes: ", get_selected_nodes("Node Editor 1##demo"))
        print("Selected Links: ", get_selected_links("Node Editor 1##demo"))
        print("Links: ", get_links("Node Editor 1##demo"))

    def clear_stuff(sender, data):
        clear_selected_nodes("Node Editor 1##demo")
        clear_selected_links("Node Editor 1##demo")

    def link_callback(sender, data):
        print("Sender: " + str(sender))
        print("Data: " + str(data))

        nodeFromPair = getViNodeConnectionFromStr(data[0])
        nodeToPair = getViNodeConnectionFromStr(data[1])
        nodeFrom = getViNodeByName(nodeFromPair['node'])
        nodeTo = getViNodeByName(nodeToPair['node'])
        nodeTo.linkCallback(nodeFrom, nodeFromPair['atr'], nodeToPair['atr'])
        # log_debug

    def delink_callback(sender, data):
        print("delink_callback")
        print("Sender: " + str(sender))
        print("Data: " + str(data))
        nodeFromPair = getViNodeConnectionFromStr(data[0])
        nodeToPair = getViNodeConnectionFromStr(data[1])
        nodeFrom = getViNodeByName(nodeFromPair['node'])
        nodeTo = getViNodeByName(nodeToPair['node'])

        print("Looking for:" + str(nodeFromPair['node']+ " : "+ nodeFromPair['atr'] + ' to: '+nodeToPair['atr']))

        for connectionName in list(nodeTo.inputConnections):
            connection = nodeTo.inputConnections[connectionName]
            nodeRef = connection['connection']
            atrFrom = connection['outname']
            print("examine conn: "+ connectionName+ " " + str(nodeRef.name)+ ' atrFrom:'+atrFrom+ ' nodeFromPair[atr]: ???'+nodeFromPair['atr'])
            if nodeRef.name == nodeFromPair['node'] and atrFrom == nodeFromPair['atr'] and connectionName ==  nodeToPair['atr']:
                print("delete! connection:" + connectionName)
                del nodeTo.inputConnections[connectionName]

    def save_all(sender, data):
        #TODO zapis pozycji całego node editora

        allViNodes = NAME_NODE_MAPPING

        print("SAVE NODES:" + str(allViNodes))

        for n in allViNodes:
            allViNodes[n].getItemConfig()

        links = get_links("Node Editor 1##demo")

        savePackage = {'viNodes': allViNodes, 'links': links}

        outfile = open(DEFAULT_FOLDER + 'test.visave', 'wb+')
        pickle.dump(savePackage, outfile)
        outfile.close()

        print(str(len(NAME_NODE_MAPPING)) + " items saved")

    def load_all(sender, data):
        # TODO zapis pozycji całego node editora

        infile = open(DEFAULT_FOLDER + 'test.visave', 'rb')
        loadedPackage = pickle.load(infile)
        infile.close()

        NAME_NODE_MAPPING = loadedPackage['viNodes']
        print(str(len(NAME_NODE_MAPPING)) + " items loaded")

        links = loadedPackage['links']

        for l in links:
            print(str(l))
            add_node_link("Node Editor 1##demo", l[0], l[1])

    with window("Main", width=500, height=300):

        with tab_bar("Main Tabbar##demo"):
            with tab("Model##demo"):
                with child("prodMenu2##demo", autosize_y=True, width=200):
                    with group("decorated child group##demo", width=-20):
                        for v in VINODES:
                            add_button(f"{v.className}##childbutton##demo", callback=createViNodeAndAddToNodeEditor,
                                       callback_data={'node': v, 'editor': "Node Editor 1##demo"})

                add_same_line()
                with child("prodMain##demo", border=False, autosize_x=True, autosize_y=True):
                    with managed_columns("Node Editor Columns##demo", 4):
                        add_button("Save All", callback=save_all)
                        add_button("Load All", callback=load_all)
                        add_button("Get Info##demo", callback=get_link_info)
                        add_button("Clear Selections##demo", callback=clear_stuff)

                    add_node_editor("Node Editor 1##demo", link_callback=link_callback, delink_callback=delink_callback)

                    end()  # node_editor
                    # end()  # window

            with tab("Training##demo"):
                add_text("This is the Training tab!")

                #texture = []
                #for i in range(0, 10000):
                #    texture.append(255)
                #    texture.append(0)
                #    texture.append(255)
                #    texture.append(255)
                #add_texture("#cooltexture", texture, 100, 100, format=mvTEX_RGBA_INT)

                #add_image("img test on train", value="#cooltexture2")

            with tab("Verification##demo"):
                add_text("This is the Training tab!")

    set_primary_window("Main", True)


set_main_window_size(1600, 800)
set_main_window_title("ViPy3")

#show_style_editor()

set_render_callback(demo_main_callback)
show_demo()
# show_debug()
# show_logger()
start_dearpygui()
