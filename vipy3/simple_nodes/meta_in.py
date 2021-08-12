from vipy3.core import *

class ViMetaIn(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)
        self.default_executor_name = 'bypass'

    def initialize_values(self):
        self.outputs = [OutConn(self,'input', 'bypass', type='any')]

    def bypass(self):
        value = self.parent_meta_node.get_input_value(self.get_name())
        return value

    def get_code(self, value_executor, result_prefix='', indent=''):
        code = indent+result_prefix+self.get_name()
        return {'imports_code': '', 'functions_code': '', 'code': code}

    def is_fresh(self):
        real_input = self.parent_meta_node.get_input_by_name(self.get_name())
        return real_input.is_fresh()