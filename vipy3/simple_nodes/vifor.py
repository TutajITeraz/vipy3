from vipy3.core import *

class ViFor(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)
        self.default_executor_name = 'for_exe_loop'

        self.iterator=0
        self.last_result=None

    def for_exe_loop(self):
        how_many = self.get_input_value('how_many')

        result_list = []
        for self.iterator in range(how_many):
            data = self.get_input_value('data')

            self.last_result = self.for_exe(data)

            result_list.append(self.last_result)
        return result_list

    def get_iter(self):
        return self.iterator

    #def get_last_result(self):
    #    return self.last_result

    def initialize_values(self):
        self.inputs = [ InConnInt(self,'how_many',1,None,0,100), InConn(self,'data') ]
        #self.outputs = [ OutConn(self,'result_list', 'for_exe_loop', type='list'), OutConn(self,'last_result', 'get_last_result', type='any'), OutConn(self,'i', 'get_iter', type='number') ]
    
        self.outputs = [ OutConn(self,'result_list', 'for_exe_loop', type='list'), OutConn(self,'i', 'get_iter', type='number') ]

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

        inner_loop_code = super().get_code('for_exe',self.get_name()+'_last_result = ','    ')
        code += inner_loop_code['code'] + '\n'
        imports_code += inner_loop_code['imports_code']
        functions_code += inner_loop_code['functions_code']

        code+='    '+self.get_name()+'_'+'results.append('+self.get_name()+'_'+'last_result'+')\n'

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
    def for_exe(self, data):
        print('Im for! Last data is:'+str(data))
        return data
    #EXECUTOR CODE END#