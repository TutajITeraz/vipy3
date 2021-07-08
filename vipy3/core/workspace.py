import dearpygui.dearpygui as dpg
from . import *

class Workspace:
    def __init__(self):
        self.uuid = gen_uuid()
        self.nodes_classes = {} 
        self.nodes_available = {}
        #self.nodes_available = {'math': {'add': ViAdd, 'sub': None, 'advanced': {'sqrt': None}}, 'AI':{'pytorch': None} }
        self.filepath = DEFAULT_WORKSPACE_SAVE_PATH

        self.meta_nodes = {}    #maps uuid to objects

    def create_new_meta_node(self, status=''):
        node = None

        LOG.log('creating new meta_node. parent =', str(self))

        if status != '':
            node = MetaNode(None, status, parent_workspace=self)
        else:
            node = MetaNode(parent_workspace=self)

        meta_node_uuid = node.get_uuid()

        self.meta_nodes[meta_node_uuid]=node

    def add_nodes_available(self,nodes):
        for n in nodes:
            self.nodes_available[n] = nodes[n]

    def get_available_nodes(self):
        return self.nodes_available

    def get_element_by_uuid(self,uuid):#TODO get element by uuid
        pass

    def dpg_save_status_to_file_callback(self, param):
        self.save_status_to_file(self.filepath)
        
    def dpg_load_status_from_file_callback(self, param):
        self.load_status_from_file()

    def load_status_from_file(self, filepath=''):
        if filepath == '':
            filepath = self.filepath
        self.filepath = filepath

        status = load_data(filepath)

        print(str(status))

        if status != None:
            self.deserialize(status)
            LOG.log('loaded file:' + filepath + 'and get status:' + str(status))

    def save_status_to_file(self, filepath=''):
        if filepath == '':
            filepath = self.filepath

        serializedStatus = self.serialize()

        print(str(serializedStatus))

        save_data(serializedStatus,filepath)


    def serialize(self):
        status = {}
        status['nodes_available'] = self.nodes_available
        meta_nodes_status={}
        for mn in self.meta_nodes:
            meta_nodes_status[mn] = self.meta_nodes[mn].serialize()

        status['meta_nodes_status']=meta_nodes_status

        LOG.log(str(status))

        return status

    def deserialize(self,status):
        #TODO should delete all existing meta nodes first
        LOG.log(status)
        self.nodes_available = status['nodes_available']
        meta_nodes_status = status['meta_nodes_status']
        for mns in meta_nodes_status:
            self.create_new_meta_node(meta_nodes_status[mns])


    def new_meta_node_callback(self,cbdata):
        self.create_new_meta_node()

