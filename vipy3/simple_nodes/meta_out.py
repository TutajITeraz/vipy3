from vipy3.core import *

class ViMetaOut(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)
        self.default_executor_name = 'bypass'

    def initialize_values(self):
        self.inputs = [ InConn(self,'out1') ]

    def bypass(self,out1):
        return out1