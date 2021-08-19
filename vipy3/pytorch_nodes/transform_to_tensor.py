from vipy3.core import *

#EXECUTOR IMPORTS BEGIN#
import torchvision.transforms as transforms
#EXECUTOR IMPORTS END#

class ViTransformToTensor(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)
        self.default_executor_name = 'get_samplers'

    def initialize_values(self):
        self.inputs = [ InConn(self,'transformsList',None,type='list') ]
        self.outputs = [ OutConn(self,'transformsList', self.default_executor_name, type='list') ]
        #functions used by other functions have to have the same name and executor


    #EXECUTOR CODE BEGIN#
    def default_executor(self, transformsList):
        if transformsList == None:
            transformsList = []

        transformsList.append(transforms.ToTensor())
        return transformsList
    #EXECUTOR CODE END#