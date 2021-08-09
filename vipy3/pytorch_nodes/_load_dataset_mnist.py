from os.path import expanduser
from torchvision import datasets
import torchvision.transforms as transforms

def load_dataset_mnist(self, transforms, root, train, download):

    from six.moves import urllib
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    return datasets.MNIST(root=expanduser(root), train=train, download=download,
                              transform=transforms.Compose(transforms))