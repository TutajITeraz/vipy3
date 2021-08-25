from vipy3.core import *
import inspect

class ViFor2(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)
        self.default_executor_name = 'for_exe_loop'

        self.iterator=0
        self.last_result=None

    def _get_func_params(self,func_to_call):
        print('vi for 2 get func params of func '+str(func_to_call))
        if func_to_call == self.for_exe_loop:
            print('vi for 2 get func params it is foooor')
            params_exe = self._get_func_params(self.for_exe)
            params = []
            for p in params_exe:
                if p != 'kwargs':
                    params.append(p)

            params_for = inspect.signature(func_to_call).parameters
            for p in params_for:
                if p != 'kwargs':
                    params.append(p)

            return params
        print('vi for 2 get func params it is nooooooooooooot foooor')
        return inspect.signature(func_to_call).parameters

    def is_fresh(self):
        if self.stage == 1:   #if gattering params - pretend that it is fresh - it will allow recursion
            return False

        if self.stage == 2:
            return False    #for will be executed every time - even if it is fresh

        if self.stage == 3:
            return False

        print('FOR STAGE IS => '+str(self.stage))
        return super().is_fresh()

    def for_exe_loop(self, how_many, **kwargs):
        print("FOR LOOP ARGS:")
        for key, value in kwargs.items():
            print("    FOR LOOP ARG : "+str(key)+" = "+str(value) )

        #how_many = self.get_input_value('how_many')

        result_list = []
        for self.iterator in range(how_many):
            data = self.get_input_value('data')

            kwargs['data'] = data

            self.last_result = self.for_exe(**kwargs)

            result_list.append(self.last_result)
        return result_list


    def initialize_values(self):
        self.inputs = [ InConnInt(self,'how_many',1,None,0,100), InConn(self,'data'), InConn(self,'test_param_1')]
        #self.outputs = [ OutConn(self,'result_list', 'for_exe_loop', type='list'), OutConn(self,'last_result', 'get_last_result', type='any'), OutConn(self,'i', 'get_iter', type='number') ]
    
        self.outputs = [ OutConn(self,'result_list', 'for_exe_loop', type='list'),
                         OutConn(self,'i', 'get_iter', type='number'),
                         OutConn(self,'get_last_data', 'get_last_data')]

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
    def for_exe(self, data, test_param1, **kwargs): #additional kwargs is due to unhandled params
        print('Im for! Last data is:'+str(data))
        print('Im for! Test param is:'+str(test_param1))
        return data

    def get_last_data(self):
        return self.last_result

    def get_iter(self):
        return self.iterator
    #EXECUTOR CODE END#