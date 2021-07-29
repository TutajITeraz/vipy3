import dearpygui.dearpygui as dpg
from vipy3.core import *
import sys
import importlib

class ViFor(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)
        self.default_executor = 'for_exe'

        self.iterator=0

    def for_exe(self):
        how_many = self.get_input_value('how_many')

        result_list = []
        for self.iterator in range(how_many):
            data = self.get_input_value('data')
            result_list.append(data)
        return result_list

    def get_iter(self):
        return self.iterator

    def initialize_values(self):
        self.inputs = [ InConnInt(self,'how_many',1,None,0,100), InConn(self,'data') ]
        self.outputs = [ OutConn(self,'result_list', 'for_exe', type='list'), OutConn(self,'i', 'get_iter', type='number') ]

    def get_code(self, value_executor, result_prefix='', indent=''):
        if(value_executor=='get_iter'):
            return {'imports_code': '', 'functions_code': '', 'code': result_prefix +' '+self.get_name()+'_'+'iter'}

        code = ''
        imports_code = ''
        functions_code = ''
        
        param = 'how_many'
        input_code = self._get_input_code(param, self.get_name()+'_'+param + ' = ')
        code += input_code['code'] + '\n'
        imports_code += input_code['imports_code']
        functions_code += input_code['functions_code']

        code += self.get_name()+'_'+'results = []\n'
        code+='for '+self.get_name()+'_'+'iter in range('+self.get_name()+'_'+param+'):'+'\n'

        param = 'data'
        input_code = self._get_input_code(param, self.get_name()+'_'+'data' + ' = ',indent='    ')
        code += input_code['code'] + '\n'
        imports_code += input_code['imports_code']
        functions_code += input_code['functions_code']

        code+='    '+self.get_name()+'_'+'results.append('+self.get_name()+'_'+'data'+')\n'

        if result_prefix != '':
            code+=result_prefix+' '+self.get_name()+'_'+'results\n'
        else:
            code+='print(str('+self.get_name()+'_'+'results))'

        #Add indentation:
        indent_code = ''
        for line in code.splitlines():
            indent_code += indent+line+'\n'

        return {'imports_code': imports_code, 'functions_code': functions_code, 'code': indent_code}