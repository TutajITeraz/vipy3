from vipy3.core import *

#EXECUTOR IMPORTS BEGIN#
import torchvision.transforms as transforms
from torchvision import datasets
from os.path import expanduser
from six.moves import urllib

from six.moves import urllib
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)
#EXECUTOR IMPORTS END#

class ViLoadDatasetMNIST(Node):
    def __init__(self, parent_meta_node=None, serialized_state=None):
        super().__init__(parent_meta_node, serialized_state)

    def initialize_values(self):
        self.inputs = [ InConnFile(self,'root','~/pydata',label='root directory'),
                        InConnBool(self,'train',True),
                        InConnBool(self,'download',True),
                        InConn(self,'transforms',None)
                        ]
        self.outputs = [ OutConn(self,'data', 'default_executor', type='tensor') ]

    #EXECUTOR CODE BEGIN#
    def default_executor(self, transforms, root, train, download):
        return datasets.MNIST(root=expanduser(root), train=train, download=download,
                              transform=transforms.Compose(transforms))
    #EXECUTOR CODE END#

