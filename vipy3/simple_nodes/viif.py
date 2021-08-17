from vipy3.core import *


class ViIf(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)
        self.default_executor_name = 'if_exe_body'

        from ._if_exe import if_exe
        setattr(self, 'if_exe', if_exe.__get__(self))

        self.iterator=0
        self.last_result=None

    def if_exe_body(self):
        condition = self.get_input_value('condition')

        if condition:
            data = self.get_input_value('data_if_true')
        else:
            data = self.get_input_value('data_if_false')

        return data

    def get_iter(self):
        return self.iterator

    #def get_last_result(self):
    #    return self.last_result

    def initialize_values(self):
        self.inputs = [ InConnBool(self,'condition'), InConn(self,'data_if_true'), InConn(self,'data_if_false') ]
    
        self.outputs = [ OutConn(self,'result', 'if_exe_body') ]

    def get_code(self, value_executor, result_prefix='', indent=''):
        if(value_executor=='get_iter'):
            return {'imports_code': '', 'functions_code': '', 'code': result_prefix +' '+self.get_name()+'_'+'iter'}

        code = ''
        imports_code = ''
        functions_code = ''
        
        param = 'condition'
        input_code = self._get_input_code(param, self.get_name()+'_'+param + ' = ')
        code += input_code['code'] + '\n'
        imports_code += input_code['imports_code']
        functions_code += input_code['functions_code']

        code+='if '+self.get_name()+'_'+param+':'+'\n'

        param = 'data_if_true'
        input_code = self._get_input_code(param, self.get_name()+'_'+'results' + ' = ','    ')
        code += input_code['code'] + '\n'
        imports_code += input_code['imports_code']
        functions_code += input_code['functions_code']

        code+='else:'+'\n'

        param = 'data_if_false'
        input_code = self._get_input_code(param, self.get_name()+'_'+'results' + ' = ','    ')
        code += input_code['code'] + '\n'
        imports_code += input_code['imports_code']
        functions_code += input_code['functions_code']

        if result_prefix != '':
            code+=result_prefix+' '+self.get_name()+'_'+'results\n'
        else:
            code+='print(str('+self.get_name()+'_'+'results))'

        #Add indentation:
        indent_code = ''
        for line in code.splitlines():
            indent_code += indent+line+'\n'

        return {'imports_code': imports_code, 'functions_code': functions_code, 'code': indent_code}
    

    #EXECUTOR CODE BEGIN#
    def if_exe(self, data):
        print('Im for! Last data is:'+str(data))
        return data
    #EXECUTOR CODE END#