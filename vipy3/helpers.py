import uuid
import shortuuid
try:
   import cPickle as pickle
except:
   import pickle

from os.path import expanduser
from dearpygui.logger import mvLogger



DEFAULT_FOLDER='~/pydata/'
DEFAULT_WORKSPACE_SAVE_PATH = DEFAULT_FOLDER + 'default.viworkspace'

def gen_uuid():
    return shortuuid.uuid()
    #return uuid.uuid1()

class Logger():#TODO logger with status bar and popup windows on error
    def __init__(self):
        self.logger = mvLogger()
    
    def log(self,level_or_text,text=''):
        level = 'trace'
        if text == '':
            text = level_or_text
        else:
            level = level_or_text

        text = str(text)

        if level == 'trace':
            self.logger.log(text)
        elif level == 'debug':
            self.logger.log_debug(text)
        elif level == 'info':
            self.logger.log_info(text)
        elif level == 'warning':
            self.logger.log_warning(text)
        elif level == 'error':
            self.logger.log_error(text)
        elif level == 'critical':
            self.logger.log_critical(text)

def save_data(data,filepath=DEFAULT_WORKSPACE_SAVE_PATH):
    print('saving data to:'+str(expanduser(filepath)))
    print('data lengts:'+str(len(data)))
    outfile = open(expanduser(filepath), 'wb+')
    pickle.dump(data, outfile, protocol=-1)
    outfile.close()

def load_data(filepath=DEFAULT_WORKSPACE_SAVE_PATH):
    infile = open(expanduser(filepath), 'rb')
    data = pickle.load(infile)
    infile.close()
    return data

LOG = Logger()
LOG.log('test1')
LOG.log('info','test2')