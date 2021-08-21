import dearpygui.dearpygui as dpg
from vipy3.core import *
import sys
import importlib

class ViShowImg(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

    def initialize_values(self):
        self.inputs = [ InConn(self,'img',1,None) ]
        self.outputs = [ OutConn(self,'bypass', 'default_executor', type='string') ]
        self.visualizers = {'show_img': ViImgVisualizer(self,'value', label='Show Image')}

    #EXECUTOR CODE BEGIN#
    def default_executor(self, img):
        return img
    #EXECUTOR CODE END#