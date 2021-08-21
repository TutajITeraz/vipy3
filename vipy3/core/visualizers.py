import dearpygui.dearpygui as dpg
import sys
from . import *
import weakref
import vipy3.core.helpers

class ViVisualizer():
    def __init__(self, parent_node, name, serialized_state=None, label=''):
        self.parent_node = weakref.proxy(parent_node)
        self.name = name
        self.uuid = gen_uuid()
        self.label = label


        if serialized_state is not None:
            self.deserialize(serialized_state)

        self.value = None

    def __del__(self):
        print('Destructor of '+self.get_name())

    def get_label(self):
        if self.label != '':
            return self.label
        else:
            return self.get_name()

    def set_value(self,value):
        self.value = value
        pass

    def update(self):
        return self.dpg_attribute_id

    def get_class_name(self):
        return type(self).__name__

    def get_parent_node(self):
        return self.parent_node

    def get_name(self):
        return self.name

    def get_uuid(self):
        return self.uuid

    def get_type(self):
        return self.type

    def dpg_render(self):
        parent_node_id = self.parent_node.get_dpg_node_id()
        self.dpg_attribute_id = dpg.add_node_attribute(label=self.get_label(), parent=parent_node_id, user_data=weakref.proxy(self), attribute_type=dpg.mvNode_Attr_Static)
        pass


    def serialize(self):
        state = {}
        state['name']=self.get_name()
        state['class_name'] = self.get_class_name()
        state['uuid'] = self.get_uuid()
        state['value'] = self.value
        state['label'] = self.label
        return state

    def deserialize(self, state):
        self.name = state['name']
        self.value = state['value']
        self.uuid = state['uuid']
        self.label = state['label']


class ViTextVisualizer(ViVisualizer):
    def __init__(self,parent_node, name='', serialized_state=None, label=''):
        super().__init__(parent_node, name, serialized_state, label)

    def dpg_render(self):
        print('render visualizer: '+self.get_name())

        parent_node_id = self.parent_node.get_dpg_node_id()
        self.dpg_attribute_id = dpg.add_node_attribute(label=self.get_label(), parent=parent_node_id, user_data=weakref.proxy(self), attribute_type=dpg.mvNode_Attr_Static)
        self.dpg_text_id = dpg.add_text(self.get_label(), parent=self.dpg_attribute_id)

    def update(self, str_or_val):
        print('update visualizer val:'+str(str_or_val))
        self.value = str_or_val
        dpg.set_value(self.dpg_text_id, str(str_or_val))


class ViImgVisualizer(ViVisualizer):
    def __init__(self,parent_node, name='', serialized_state=None, label=''):
        super().__init__(parent_node, name, serialized_state, label)

    def dpg_render(self):
        print('render visualizer: '+self.get_name())

        parent_node_id = self.parent_node.get_dpg_node_id()
        self.dpg_attribute_id = dpg.add_node_attribute(label=self.get_label(), parent=parent_node_id, user_data=weakref.proxy(self), attribute_type=dpg.mvNode_Attr_Static)
        self.dpg_img_id = dpg.add_text(self.get_label(), parent=self.dpg_attribute_id)

    def update(self, str_or_val):
        print('update visualizer val:'+str(str_or_val))
        self.value = str_or_val
        dpg.set_value(self.dpg_text_id, str(str_or_val))

def _create_dynamic_textures():
    ## create dynamic textures
    texture_data1 = []
    for i in range(0, 100*100):
        texture_data1.append(255/255)
        texture_data1.append(0)
        texture_data1.append(255/255)
        texture_data1.append(255/255)

    dpg.add_dynamic_texture(100, 100, texture_data1, parent=demo_texture_container, id=demo_dynamic_texture_1)

def _update_dynamic_textures(sender, app_data, user_data):
    new_color[0] = 0.1
    new_color[1] = 0.2
    new_color[2] = 0.3
    new_color[3] = 0.4

    texture_data = []
    for i in range(0, 100*100):
        texture_data.append(new_color[0])
        texture_data.append(new_color[1])
        texture_data.append(new_color[2])
        texture_data.append(new_color[3])

    dpg.set_value(demo_dynamic_texture_1, texture_data)
