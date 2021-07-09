import dearpygui.dearpygui as dpg
from . import *


class MetaNode(Node):
    def __init__(self,  parent_meta_node=None, serialized_state='', parent_workspace=None):
        self.parent_workspace = parent_workspace
        self.nodes = {}

        self.should_render_editor = True
        self.should_render_node = False
        
        super().__init__(parent_meta_node, serialized_state)


    def initialize_values(self):    #TODO: Separate initialize_values from render
        self.dpg_render_editor()

    def render_node(self):
        pass

    def add_node_callback(self, sender, app_data, user_data):
        LOG.log('add_node_callback sender '+ str(sender))
        LOG.log('add_node_callback app_data ' + str(app_data))
        LOG.log('add_node_callback user_data '+ str(user_data))

        self.add_node_to_editor(user_data['node_class'])
    
    def add_node_to_editor(self, node_class):
        LOG.log('add_node_to_editor: '+str(node_class))
        new_node = node_class(parent_meta_node=self)

        self.nodes[new_node.get_uuid()] = new_node

    def get_node_by_uuid(uuid):
        node = None
        if hasattr(self.nodes, uuid):
            node = self.nodes[uuid]

        return node
    
    def dpg_get_node_editor_id(self):
        return self.dpg_node_editor_id

    def dpg_link_callback(self,sender,app_data,user_data):
        LOG.log('dpg_link_callback sender '+ str(sender))
        LOG.log('dpg_link_callback app_data ' + str(app_data))
        LOG.log('dpg_link_callback user_data '+ str(user_data))
        attr_from_dpg_id = app_data[0]
        attr_to_dpg_id = app_data[1]

        attr_from = dpg.get_item_user_data(attr_from_dpg_id)
        attr_to = dpg.get_item_user_data(attr_to_dpg_id)

        LOG.log('dpg_link_callback attr_from ' + str(attr_from))
        LOG.log('dpg_link_callback attr_to ' + str(attr_to))

        can_connect = attr_to.set_connected_node_out(attr_from)

        result = False
        if can_connect:
            result = dpg.add_node_link(attr_from_dpg_id, attr_to_dpg_id, parent=sender, user_data=attr_to)

        LOG.log('new link created: '+str(result))

        return True

    def dpg_delink_callback(self,sender,app_data,user_data):
        LOG.log('dpg_delink_callback sender '+ str(sender))
        LOG.log('dpg_delink_callback app_data ' + str(app_data))
        LOG.log('dpg_delink_callback user_data '+ str(user_data))
        
        link_dpg_id = app_data

        attr_to = dpg.get_item_user_data(link_dpg_id)

        attr_to.set_connected_node_out(None)

        dpg.delete_item(link_dpg_id)

    def dpg_render_editor(self):
        self.dpg_window_id = dpg.add_window(label=self.get_name(), width=800, height=600, pos=(50, 50))

        self.dpg_menu_bar_id = dpg.add_menu_bar(label='Workspace menu bar', parent=self.dpg_window_id)
        self.dpg_meta_node_menu_id = dpg.add_menu(label='MetaNode', parent=self.dpg_menu_bar_id)
        dpg.add_menu_item(label='Load MetaNode', parent=self.dpg_meta_node_menu_id)#TODO load meta_node
        dpg.add_menu_item(label='Save MetaNode', parent=self.dpg_meta_node_menu_id)#TODO save meta_node
        dpg.add_menu_item(label='Save MetaNode As...', parent=self.dpg_meta_node_menu_id)#TODO save as meta_node

        self.dpg_add_node_menu_id = dpg.add_menu(label='Add Node...', parent=self.dpg_menu_bar_id)

        #self.parent_workspace.dpg_render_available_nodes_to(self.dpg_add_node_menu_id, self)
        avaliable_nodes = self.parent_workspace.get_available_nodes()
        self.dpg_render_available_nodes_to(avaliable_nodes,self.dpg_add_node_menu_id)
        #self.parent_workspace.dpg_render_available_nodes_to(self.dpg_add_node_menu_id, (lambda self: lambda arg1, arg2: self.add_node_callback(arg1, arg2))(self))

        self.dpg_node_editor_id = dpg.add_node_editor(parent=self.dpg_window_id, callback=self.dpg_link_callback, delink_callback=self.dpg_delink_callback)

        #self.dpg_popup_id = dpg.popup(self.dpg_node_editor_id)
        #self.dpg_popup_id = dpg.window(label='Rightclick fake window', modal=True)
        #self.dpg_popup_menu_bar_id = dpg.add_menu_bar(label='Rightclick menu bar', parent=self.dpg_popup_id)
        #self.dpg_right_click_menu_id = dpg.add_menu(label='right click menu', parent=self.dpg_popup_menu_bar_id)
        #dpg.add_menu_item(label='Add some node', parent=self.dpg_right_click_menu_id)  # TODO add some node

        self.dpg_is_rendered = True

    def dpg_render_available_nodes_to(self,nodes,dpg_parent):
        for n in nodes:
            LOG.log(n,type(nodes[n]))
            if type(nodes[n]) is dict:
                menu_item_id = dpg.add_menu(label=n, parent=dpg_parent)
                self.dpg_render_available_nodes_to(nodes[n],menu_item_id)
            else:
                if nodes[n] is not None:
                    print('nodes[n]'+ str(nodes[n]))

                    menu_item_id = dpg.add_menu_item(label=n, parent=dpg_parent, callback=self.add_node_callback, user_data={'node_class': nodes[n]})
                else:
                    menu_item_id = dpg.add_menu_item(label=n, parent=dpg_parent)

    def dpg_right_click_menu(self):
        pass

    def saveStatusToFile(self): #TODO save
        pass

    def serialize(self):
        status = {}
        status['dpg_is_rendered'] = self.dpg_is_rendered
        if self.dpg_is_rendered:
            status['dpg_window_width'] = dpg.get_item_width(self.dpg_window_id)
            status['dpg_window_height'] = dpg.get_item_height(self.dpg_window_id)
            status['dpg_window_pos'] = dpg.get_item_pos(self.dpg_window_id)

        status['nodes']={}
        for n in self.nodes:
            status['nodes'][n] = self.nodes[n].serialize()

        #TODO add all links to status:
        
        #dpg_all_items = dpg.get_i
        #for item in dpg_all_items:
        #    print('item '+str(item))
        
        return status

    def deserialize(self, status):
        self.dpg_is_rendered = status['dpg_is_rendered']
        if self.dpg_is_rendered:
            self.dpg_render_editor()
            dpg.set_item_width(self.dpg_window_id,status['dpg_window_width'])
            dpg.set_item_height(self.dpg_window_id,status['dpg_window_height'])
            dpg.set_item_pos(self.dpg_window_id,status['dpg_window_pos'])

        for n in status['nodes']:
            self.nodes[n] = Node(self, status['nodes'][n])
