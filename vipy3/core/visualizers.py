import dearpygui.dearpygui as dpg
import sys
from . import *
import weakref
import vipy3.core.helpers
import numpy as np

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

DPG_VISUALIZERS_TEXTURES_CONTAINER = dpg.add_texture_registry(label="Visualizers textures container")


class ViImgVisualizer(ViVisualizer):
    def __init__(self,parent_node, name='', serialized_state=None, label='', width=100, height=100):
        super().__init__(parent_node, name, serialized_state, label)
        self.width = width
        self.height = height

    def dpg_render(self):
        print('render visualizer: '+self.get_name())

        parent_node_id = self.parent_node.get_dpg_node_id()
        self.dpg_attribute_id = dpg.add_node_attribute(label=self.get_label(), parent=parent_node_id, user_data=weakref.proxy(self), attribute_type=dpg.mvNode_Attr_Static)
        self.dpg_texture_id = self._create_dynamic_texture()
        self.dpg_img_id = dpg.add_image(self.dpg_texture_id, width=self.width, height=self.height, parent=self.dpg_attribute_id)

    def update(self, value):
        print('update visualizer val:'+str(value))
        self.value = value

        def tensor_to_np(tensor):
            img = tensor.mul(255).byte()
            # img = img.cpu().numpy().squeeze(0).transpose((1, 2, 0))
            img = img.cpu().numpy()
            return img

        imgdata = tensor_to_np(value)

        channelsNo = len(imgdata)
        imagesHeight = len(imgdata[0])
        imagesWidth = len(imgdata[0][0])

        if self.width != imagesWidth or self.height != imagesHeight:
            self.width = imagesWidth
            self.height = imagesHeight

            dpg.delete_item(self.dpg_texture_id)
            dpg.delete_item(self.dpg_img_id)

            self.dpg_texture_id = dpg.generate_uuid()
            dpg.add_dynamic_texture(self.width, self.height, self.texture_data,
                                    parent=DPG_VISUALIZERS_TEXTURES_CONTAINER, id=self.dpg_texture_id)

            self.dpg_img_id = dpg.add_image(self.dpg_texture_id, width=self.width, height=self.height,
                                            parent=self.dpg_attribute_id)

        print("IMG DATA CHANNELS "+ str(channelsNo))
        print("IMG DATA imagesHeight "+ str(imagesHeight))
        print("IMG DATA imagesWidth "+ str(imagesWidth))

        #update self.dpg_img_id

        dpg.set_item_width(self.dpg_img_id, imagesWidth)
        dpg.set_item_height(self.dpg_img_id, imagesHeight)

        self.width = imagesWidth
        self.height = imagesHeight

        if channelsNo == 1:
            imgdata = np.stack((imgdata,) * 4, axis=-1)  # for grayscale

            for x in range(imagesWidth):
                for y in range(imagesHeight):
                    imgdata[0][x][y][3] = 1.0 #alpha channel

        elif channelsNo==3:
            rgbimg = []
            rdata = imgdata[0]
            gdata = imgdata[1]
            bdata = imgdata[2]
            for x in range(imagesWidth):
                for y in range(imagesHeight):
                    rgbimg.append(rdata[x][y])
                    rgbimg.append(gdata[x][y])
                    rgbimg.append(bdata[x][y])
                    rgbimg.append(0.0)
            imgdata = rgbimg

        print("Result imgdata len "+str(len(imgdata)))

        self.texture_data = imgdata

        dpg.set_value(self.dpg_texture_id, self.texture_data)

    def _create_dynamic_texture(self):
        ## create dynamic textures
        self.texture_data = []
        for i in range(0, 100*100):
            self.texture_data.append(255/255)
            self.texture_data.append(0)
            self.texture_data.append(255/255)
            self.texture_data.append(255/255)

        self.dpg_texture_id = dpg.generate_uuid()
        dpg.add_dynamic_texture(self.width, self.height, self.texture_data, parent=DPG_VISUALIZERS_TEXTURES_CONTAINER, id=self.dpg_texture_id)

        return self.dpg_texture_id
