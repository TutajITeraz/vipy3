from dearpygui.core import *
from dearpygui.simple import *
from vinode import *
from torchvision import datasets
import torchvision.transforms as transforms

import torch
import numpy as np

import torch.nn as nn
import torch.nn.functional as F

from os.path import expanduser

import collections
try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict


class ViDatasetsMNIST(ViNode):
    className = 'ViDatasetsMNIST'

    def __init__(self, name):
        super().__init__(name)
        self.addConnection('transforms', None, None)
        self.params = {'root': '~/pydata', 'train': True, 'download': True}

    def execFunction(self):
        return datasets.MNIST(root=expanduser(self.params['root']), train=self.params['train'], download=self.params['download'],
                              transform=transforms.Compose(self.inputCache['transforms']))

    def initFunction(self):
        self.setStage(1)
        # The MNIST datasets are hosted on yann.lecun.com that has moved under CloudFlare protection
        # Run this script to enable the datasets download
        # Reference: https://github.com/pytorch/vision/issues/1938
        from six.moves import urllib
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)

class ViDataset(ViNode):
    className = 'ViDataset'

    def __init__(self, name):
        super().__init__(name)
        self.addConnection('transforms', None, None)
        self.params = {'root': '~/pydata', 'train': True, 'download': True,
                       'dataset': {'selected': 'MNIST', 'list': ['MNIST','CIFAR10']}}

    def execFunction(self):
        if self.getParamValue('dataset') == 'MNIST':
            return datasets.MNIST(root=expanduser(self.params['root']), train=self.params['train'], download=self.params['download'],
                              transform=transforms.Compose(self.inputCache['transforms']))
        if self.getParamValue('dataset') == 'CIFAR10':
            return datasets.CIFAR10(root=expanduser(self.params['root']), train=self.params['train'], download=self.params['download'],
                              transform=transforms.Compose(self.inputCache['transforms']))

    def initFunction(self):
        self.setStage(1)
        # The MNIST datasets are hosted on yann.lecun.com that has moved under CloudFlare protection
        # Run this script to enable the datasets download
        # Reference: https://github.com/pytorch/vision/issues/1938
        from six.moves import urllib
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)


class ViDataLoader(ViNode):
    className = 'ViDataLoader'

    def __init__(self, name):
        super().__init__(name)
        self.addConnection('data', None, None)
        self.params = {'batch_size': 20, 'num_workers': 0}

    def execFunction(self):
        return torch.utils.data.DataLoader(self.inputCache['data'], batch_size=self.params['batch_size'],
                                           num_workers=self.params['num_workers'])


class ViDataIter(ViNode):
    className = 'ViDataIter'

    def __init__(self, name):
        super().__init__(name)
        self.addConnection('dataloader', None, None)
        self.outputFunctions = {'image': self.execFunction, 'label': self.getLabel}
        self.playDefaultOut = 'image'
        self.params = {'select': 1}

    def execFunction(self):
        self.getInputValuesIfNeeded()
        dataiter = iter(self.inputCache['dataloader'])
        self.images, self.labels = dataiter.next()

        return self.images[self.params['select']]

    def getLabel(self):
        self.getInputValuesIfNeeded()
        
        return self.labels[self.params['select']]



unloader = transforms.ToPILImage()


def tensor_to_np(tensor):
    img = tensor.mul(255).byte()
    # img = img.cpu().numpy().squeeze(0).transpose((1, 2, 0))
    img = img.cpu().numpy()
    return img


def grayscale_to_rgb(img):
    newimg = []
    for x in img:
        for y in x:
            for z in y:
                newimg.append(z)
                newimg.append(z)
                newimg.append(z)
    return newimg


class ViDataFigure(ViNode):
    className = 'ViDataFigure'

    def __init__(self, name):
        super().__init__(name)
        self.addConnection('imgdata', None, None)
        self.imgPreview = {'prev': self.name + "#texture"}

        self.textureSize[0] = 128
        self.textureSize[1] = 128

        self.texture = []
        for i in range(0, self.textureSize[0] * self.textureSize[1]):
            self.texture.append(255)
            self.texture.append(0)
            self.texture.append(255)
        add_texture(self.name + "#texture", self.texture, self.textureSize[0], self.textureSize[1],
                    format=mvTEX_RGB_INT)

    def execFunction(self):
        # draw_image()
        imgdata = tensor_to_np(self.inputCache['imgdata'])
        imgdata = np.stack((imgdata,) * 3, axis=-1)  # for grayscale

        # imgdata = grayscale_to_rgb(imgdata[0])
        # print("IMG DATA"+ str(imgdata))

        self.texture = imgdata

        self.textureSize[0] = 28
        self.textureSize[1] = 28

        # add_texture("#cooltexture", self.texture, 10, 10, format=mvTEX_RGBA_INT)
        add_texture(self.name + "#texture", self.texture, self.textureSize[0], self.textureSize[1],
                    format=mvTEX_RGB_INT)

        return self.inputCache['imgdata']


class ViSize2D(ViNode):
    className = 'ViSize2D'

    def __init__(self, name):
        super().__init__(name)
        self.params = {'x': 28 * 28, 'y': 1}

    def execFunction(self):
        return [self.params['x'], self.params['y']]


# TODO zrobić ViView2d
class ViView(ViNode):
    className = 'ViView'

    def __init__(self, name):
        super().__init__(name)
        self.addConnection('data', None, None)
        self.addConnection('size', None, None)

    def execFunction(self):
        return self.inputCache['data'].view(self.inputCache['size'])


class ViRelu(ViNode):
    className = 'ViRelu'

    def __init__(self, name):
        super().__init__(name)
        self.addConnection('data', None, None)

    def execFunction(self):
        return F.relu(self.inputCache['data'])


# TODO zrobić ViLinear2d
class ViLinear(ViNode):
    className = 'ViLinear'

    def __init__(self, name):
        super().__init__(name)
        self.outputFunctions = {'parameters': self.getParameters, 'out': self.execFunction}
        self.params = {'x': 28 * 28, 'y': 1}
        self.addConnection('data', None, None)

        self.m = None
        self.lastoutsizex = 0
        self.lastoutsizey = 0

    def execFunction(self):
        # init only when param change
        if not hasattr(self, 'm') or self.params['x'] != self.lastoutsizex or self.params['y'] != self.lastoutsizey :
            self.m = nn.Linear(self.params['x'], self.params['y'])

        self.lastoutsizex = self.params['x']
        self.lastoutsizey = self.params['y']

        return self.m(self.inputCache['data'])

    def getParameters(self):
        if not hasattr(self, 'm') or self.params['x'] != self.lastoutsizex or self.params['y'] != self.lastoutsizey :
            self.m = nn.Linear(self.params['x'], self.params['y'])

        self.lastoutsizex = self.params['x']
        self.lastoutsizey = self.params['y']

        return self.m.parameters()


class Net(nn.Module):
    def __init__(self, viForwardFunction):
        super(Net, self).__init__()
        # self.fc1 = nn.Linear(28 * 28, 1)
        self.viForwardFunction = viForwardFunction

        print("Net init")

    def forward(self, x):
        print("Net forward")
        # flatten image input
        # x = x.view(-1, 28 * 28)
        # add hidden layer, with relu activation function
        # x = F.relu(self.fc1(x))
        return self.viForwardFunction(x)


class ViNet(ViNode):
    className = 'ViNet'

    def __init__(self, name):
        super().__init__(name)
        self.outputFunctions = {'model': self.getModel}
        self.addConnection('forward', None, None)
        self.model = Net(self.execFunction)

    def execFunction(self, data):
        return self.inputCache['data']

    def getModel(self):
        return self.model


class ViCrossEntropyLoss(ViNode):
    className = 'ViCrossEntropyLoss'

    def __init__(self, name):
        super().__init__(name)

    def initFunction(self):
        self.criterion = nn.CrossEntropyLoss()

    def execFunction(self):
        return self.criterion


class ViOptimizer(ViNode):
    className = 'ViOptimizer'

    def __init__(self, name):
        super().__init__(name)
        self.addConnection('parameters', None, None)
        self.params = {'lr': 0.01}

        self.optimizer = None

    def execFunction(self):
        # TODO cache do not create everytime!

        print("self.inputCache[ parameters ]",str(self.inputCache['parameters']))
        print("self.params['lr']", str(self.params['lr']))

        self.optimizer = torch.optim.SGD(self.inputCache['parameters'], self.params['lr'])
        return self.optimizer


# TODO zrobić jak for
class ViTrainer(ViNode):
    className = 'ViTrainer'

    def __init__(self, name):
        super().__init__(name)
        self.addConnection('model', None, None)
        self.addConnection('train_loader', None, None)
        self.addConnection('optimizer', None, None)
        self.addConnection('lossFunction', None, None)
        self.params = {'n_epochs': 30}

        self.optimizer = None

    def execFunction(self):

        for epoch in range(self.params['n_epochs']):
            train_loss = 0.0
            for data, target in self.inputCache['train_loader']:
                # clear the gradients of all optimized variables
                self.inputCache['optimizer'].zero_grad()
                # forward pass: compute predicted outputs by passing inputs to the model
                output = self.inputCache['model'](data)
                # calculate the loss
                loss = self.inputCache['lossFunction'](output, target)
                # backward pass: compute gradient of the loss with respect to model parameters
                loss.backward()
                # perform a single optimization step (parameter update)
                self.inputCache['optimizer'].step()
                # update running training loss
                train_loss += loss.item() * data.size(0)

            train_loss = train_loss / len(self.inputCache['train_loader'].dataset)

            print('Epoch: {} \tTraining Loss: {:.6f}'.format(
                epoch + 1,
                train_loss
            ))

        return None


class ViNetTrainer(ViNode):
    className = 'ViNetTrainer'
    def __init__(self, name):
        super().__init__(name)
        self.results = []
        self.params = {'n_epochs': 30}
        self.outputFunctions = {'runFor': self.forFunction, 'getModel': self.getModel, 'rawData': self.getData}
        self.playDefaultOut = 'runFor'
        self.addConnection('train_loader', None, None)
        self.addConnection('optimizer', None, None)
        self.addConnection('lossFunction', None, None)
        self.addConnection('processedData', None, None)

        self.train_loss = 0.0

        self.initFunction()

    def initFunction(self):
        self.model = Net(self.forwardFunction)
        self.data = None

    def forwardFunction(self, data):
        return self.inputCache['processedData']

    def getModel(self):
        return self.model

    def getData(self):
        return self.data

    def forFunction(self):

        self.execCounter.append([0])
        self.iterator = 0

        for epoch in range(self.params['n_epochs']):
            self.train_loss = 0.0
            for self.data, target in self.inputCache['train_loader']:
                self.iterator+=1
                self.execCounter.pop()
                self.execCounter.append(self.iterator)
                self.getInputValues()
                # clear the gradients of all optimized variables
                self.inputCache['optimizer'].zero_grad()
                # forward pass: compute predicted outputs by passing inputs to the model
                #output = self.model(self.data)
                # calculate the loss
                loss = self.inputCache['lossFunction'](self.inputCache['processedData'], target)
                # backward pass: compute gradient of the loss with respect to model parameters
                loss.backward()
                # perform a single optimization step (parameter update)
                self.inputCache['optimizer'].step()
                # update running training loss
                self.train_loss += loss.item() * self.data.size(0)

            self.train_loss = self.train_loss / len(self.inputCache['train_loader'].dataset)

            print('Epoch: {} \tTraining Loss: {:.6f}'.format(
                epoch + 1,
                self.train_loss
            ))

        return self.train_loss


class ViAddLists(ViNode):
    className = 'ViAddLists'

    def __init__(self, name):
        super().__init__(name)

        self.addConnection('listA', None, None)
        self.addConnection('listB', None, None)

    def execFunction(self):
        return list(self.inputCache['listA'] + self.inputCache['listB'])


class ViSeqNet(ViNode):
    className = 'ViSeqNet'

    def __init__(self, name):
        super().__init__(name)
        self.outputFunctions = {'model': self.getModel, 'parameters': self.getParams}
        self.playDefaultOut = 'model'
        self.addConnection('netDict', None, None)

    def getModel(self):
        if not hasattr(self,'model'):
            self.preFunction()
            self.getInputValues()
            self.model = nn.Sequential(self.inputCache['netDict'])

        return self.model

    def getParams(self):
        return self.getModel().parameters()

class ViSeqLinear(ViNode):
    className = 'ViSeqLinear'

    def __init__(self, name):
        super().__init__(name)
        self.params = {'x': 28 * 28, 'y': 1}
        self.addConnection('seq', None, None)

        self.f = None

    def execFunction(self):
        self.f = nn.Linear(self.params['x'], self.params['y'])
        seq = self.inputCache['seq']
        if seq == None:
            seq = OrderedDict([])

        seq.update({self.name: self.f})
        return seq

class ViSeqReLU(ViNode):
    className = 'ViSeqReLU'

    def __init__(self, name):
        super().__init__(name)
        self.addConnection('seq', None, None)

        self.f = None

    def execFunction(self):
        self.f = nn.ReLU()
        seq = self.inputCache['seq']
        if seq == None:
            seq = OrderedDict([])

        seq.update({self.name: self.f})
        return seq

class ViSeqLogSoftmax(ViNode):
    className = 'ViSeqLogSoftmax'

    def __init__(self, name):
        super().__init__(name)
        self.addConnection('seq', None, None)

        self.f = None

    def execFunction(self):
        self.f = nn.LogSoftmax(dim=1)
        seq = self.inputCache['seq']
        if seq == None:
            seq = OrderedDict([])

        seq.update({self.name: self.f})
        return seq



class ViNetTrainer(ViNode):
    className = 'ViNetTrainer'
    def __init__(self, name):
        super().__init__(name)
        self.results = []
        self.params = {'n_epochs': 30}
        self.outputFunctions = {'getModel': self.forFunction}
        self.playDefaultOut = 'getModel'
        self.addConnection('train_loader', None, None)
        self.addConnection('model', None, None)
        self.addConnection('optimizer', None, None)
        self.addConnection('lossFunction', None, None)

        self.initFunction()

    def initFunction(self):
        self.train_loss = 0.0
        self.data = None
        self.iterator = 0

    def forFunction(self):

        self.execCounter.append([0])
        self.iterator = 0

        self.getInputValues()

        for epoch in range(self.params['n_epochs']):
            self.train_loss = 0.0
            for self.data, target in self.inputCache['train_loader']:
                self.iterator += 1
                self.execCounter.pop()
                self.execCounter.append(self.iterator)

                # Flatten MNIST images into a 784 long vector
                images = self.data.view(self.data.shape[0], -1)
                # clear the gradients of all optimized variables
                self.inputCache['optimizer'].zero_grad()
                # forward pass: compute predicted outputs by passing inputs to the model
                output = self.inputCache['model'](images)
                # calculate the loss
                loss = self.inputCache['lossFunction'](output, target)
                # backward pass: compute gradient of the loss with respect to model parameters
                loss.backward()
                # perform a single optimization step (parameter update)
                self.inputCache['optimizer'].step()
                # update running training loss
                self.train_loss += loss.item() * images.size(0)

            self.train_loss = self.train_loss / len(self.inputCache['train_loader'].dataset)

            print('Epoch: {} \tTraining Loss: {:.6f}'.format(
                epoch + 1,
                self.train_loss
            ))

        return self.inputCache['model']

class ViUseModelOnData(ViNode):
    className = 'ViUseModelOnData'

    def __init__(self, name):
        super().__init__(name)
        self.outputFunctions = {'out': self.execFunction}
        self.playDefaultOut = 'out'
        self.addConnection('data', None, None)
        self.addConnection('model', None, None)


    def execFunction(self):
        with torch.no_grad():
            # Flatten MNIST images into a 784 long vector
            flattenedData = self.inputCache['data'].view(self.inputCache['data'].shape[0], -1)
            results = self.inputCache['model'](flattenedData)

            return results

#TODO Automatycznie dopasować do wielkości danych
class ViLogChart(ViNode):
    className = 'ViLogChart'

    def __init__(self, name):
        super().__init__(name)
        self.addConnection('logData', None, None)

    def initFunction(self):
        self.plotExists = False
        pass

    def execFunction(self):
        values = torch.exp(self.inputCache['logData']).tolist()[0]

        if not self.plotExists:
            add_plot(self.name+"##plot", x_axis_name="x", y_axis_name="y", height=200, width=200, parent=self.name)
            set_plot_xlimits(self.name+"##plot", 0, 11)
            set_plot_ylimits(self.name+"##plot", 0, 1.1)
            labels = [["0", 1], ["1", 2], ["2", 3],["3", 4],["4", 5],["5", 6],["6", 7],["7", 8],["8", 9],["9", 10]]
            set_xticks(self.name+"##plot", labels)
            self.plotExists = True

        print('values:'+str(values))

        xticks = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

        add_bar_series(self.name+"##plot", "data", xticks, values, weight=1)

class ViSaveModel(ViNode):
    className = 'ViSaveModel'

    def __init__(self, name):
        super().__init__(name)
        self.outputFunctions = {'getAndSaveModel': self.execFunction}
        self.playDefaultOut = 'getAndSaveModel'
        self.addConnection('model', None, None)
        self.params={'path': '~/pydata/Model.pytorch'}

    def initFunction(self):
        pass

    def execFunction(self):
        torch.save(self.inputCache['model'], expanduser(self.params['path']))

        return self.inputCache['model']


class ViLoadModel(ViNode):
    className = 'ViLoadModel'

    def __init__(self, name):
        super().__init__(name)
        self.outputFunctions = {'loadModel': self.execFunction}
        self.playDefaultOut = 'loadModel'
        self.params = {'path': '~/pydata/Model.pytorch'}

    def initFunction(self):
        pass

    def execFunction(self):
        self.model = torch.load(expanduser(self.params['path']))

        return self.model

class ViTransformToTensor(ViNode):
    className = 'ViTransformToTensor'

    def __init__(self, name):
        super().__init__(name)
        self.addConnection('transformsList', None, None)

        self.f = None

    def execFunction(self):
        self.f = transforms.ToTensor()
        seq = self.inputCache['transformsList']
        if seq == None:
            seq = []

        seq.append(self.f)
        return seq

class ViNormalize(ViNode):
    className = 'ViNormalize'

    def __init__(self, name):
        super().__init__(name)
        self.params = {'mean0': 0.5, 'mean1': 0.5, 'mean2': 0.5, 'std0': 0.5, 'std1': 0.5, 'std2': 0.5}
        self.addConnection('transformsList', None, None)

        self.f = None

    def execFunction(self):
        self.f = transforms.Normalize((self.getParamValue('mean0'), self.getParamValue('mean1'), self.getParamValue('mean2')), (self.getParamValue('std0'), self.getParamValue('std1'), self.getParamValue('std2')))
        seq = self.inputCache['transformsList']
        if seq == None:
            seq = []

        seq.append(self.f)
        return seq

#TODO Usunąć niepotrzebne
#TODO wyświetlanie grafu dla nauczonego :)
#TODO convolution

###############################################################
# TRAIN.
# INPUT:
#	n_epochs = 30
#	model
#	train_loader
#	optimizer
#	criterion(lossFunction)

# INNER PARAMS:
#	train_loss = 0.0

VINODES.append(ViTransformToTensor)
VINODES.append(ViNormalize)
VINODES.append(ViDatasetsMNIST)
VINODES.append(ViDataLoader)
VINODES.append(ViDataIter)
VINODES.append(ViDataFigure)

VINODES.append(ViSize2D)
VINODES.append(ViView)
#VINODES.append(ViRelu)
#VINODES.append(ViLinear)

#VINODES.append(ViNet)
VINODES.append(ViCrossEntropyLoss)
VINODES.append(ViOptimizer)
VINODES.append(ViTrainer)

VINODES.append(ViNetTrainer)
VINODES.append(ViAddLists)

VINODES.append(ViSeqNet)
VINODES.append(ViSeqLinear)
VINODES.append(ViSeqReLU)
VINODES.append(ViSeqLogSoftmax)

VINODES.append(ViUseModelOnData)
VINODES.append(ViLogChart)


VINODES.append(ViSaveModel)
VINODES.append(ViLoadModel)

VINODES.append(ViDataset)
# ViCriterion
# ViOptimizer