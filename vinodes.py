from dearpygui.core import *
from dearpygui.simple import *
from vinode import *

class ViValue(ViNode):
    className = 'ViValue'
    def __init__(self, name):
        super().__init__(name)

        self.params = {'value': 10}

    def execFunction(self):
        return self.params['value']


class ViAdd(ViNode):
    className = 'ViAdd'
    def __init__(self, name):
        super().__init__(name)

        self.addConnection('a', None, None)
        self.addConnection('b', None, None)

    def execFunction(self):
        return self.inputCache['a'] + self.inputCache['b']


class ViFor(ViNode):
    className = 'ViFor'
    def __init__(self, name):
        super().__init__(name)
        self.results = []
        self.params = {'howMany': 10}
        self.outputFunctions = {'for': self.forFunction, 'i': self.getIterator}
        self.playDefaultOut = 'for'
        self.addConnection('in', None, None)

    def getIterator(self):
        return self.iterator

    def forFunction(self):
        self.results = []
        self.execCounter.append([0])
        for self.iterator in range(self.params['howMany']):
            self.execCounter.pop()
            self.execCounter.append(self.iterator)
            self.getInputValues()
            self.results.append(self.inputCache['in'])
        return self.results

VINODES.append(ViFor)
VINODES.append(ViAdd)
VINODES.append(ViValue)