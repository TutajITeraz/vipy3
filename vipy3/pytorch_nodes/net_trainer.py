from vipy3 import ViFor
from vipy3.core import *
from vipy3.core.in_conn import InConn


class ViNetTrainer(ViFor):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)


    def for_exe_loop(self, **kwargs):
        print("FOR LOOP ARGS:")
        for key, value in kwargs.items():
            print("    FOR LOOP ARG : "+str(key)+" = "+str(value) )


        how_many = self.get_input_value('how_many')

        result_list = []
        for self.iterator in range(how_many):
            data = self.get_input_value('data')

            self.last_result = self.for_exe(**kwargs)

            result_list.append(self.last_result)
        return result_list

    def initialize_values(self):
        self.inputs = [ InConnInt(self,'how_many',1,None,0,100),
                        InConn(self, 'train_loader'),
                        InConn(self, 'model'),
                        InConn(self, 'oprimizer'),
                        InConn(self, 'loss_function')
                        ]

        self.outputs = [ OutConn(self,'result_list', 'for_exe_loop', type='list'),
                         OutConn(self,'i', 'get_iter', type='number'),
                         OutConn(self, 'get_last_model', 'get_last_model', type='number')
                         ]


    #EXECUTOR CODE BEGIN#
    def for_exe(self, data, train_loader, model, optimizer, loss_function):
        print('Im for! Last data is:'+str(data))
        return data
    #EXECUTOR CODE END#