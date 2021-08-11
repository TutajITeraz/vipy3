def load_dataset_mnist(self, transforms, root, train, download):

    print('Init end, loading function 1.2')
    import torchvision.transforms as transforms
    print('Init end, loading function 1.3')
    from torchvision import datasets
    print('Init end, loading function 1.1')
    from os.path import expanduser

    print('root:'+str(root))
    print('train:'+str(train))
    print('download:'+str(download))

    from six.moves import urllib
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    #return datasets.MNIST(root=expanduser(root), train=train, download=download,
    #                          transform=transforms.Compose(transforms))

    return 'test mnist'

