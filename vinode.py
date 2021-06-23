from dearpygui.core import *
from dearpygui.simple import *
import copy


NAME_NODE_MAPPING = {}
VINODES = []

#TODO zmienić WSZYSTKIE wywołania parametrów na te IfNeeded

def getViNodeByName(nodeName):
    node = None
    try:
        node = NAME_NODE_MAPPING[nodeName]
    except:
        pass
    return node


def getViNodeConnectionFromStr(strName):
    splitted = strName.split("##")
    return {'node': splitted[1], 'atr': splitted[0]}


def createViNodeAndAddToNodeEditor(sender, data):
    name = data['node'].className;
    nameWithNumber = ''
    for i in range(9999):
        nameWithNumber = name + str(i)
        if getViNodeByName(nameWithNumber) == None:
            break

    newViNode = data['node'](nameWithNumber)
    newViNode.addToNodeEditor(data['editor'])
    # newViNode.dpgNode = get_data(nameWithNumber)


# TODO parametry int nadpisywalne wejściem
# TODO node sekwencji operacji
# TODO gen code
# TODO oznaczenie zmian :) Check przy pobieraniu :)
# TODO 'connection' zmienić na nodeRef  a nazwę na connectionName
# TODO przejść na nowe dearpygui

class ViNode:
    className = 'ViNode'

    def __init__(self, name):
        self.name = name
        self.inputConnections = {}
        self.params = {}
        self.inputCache = {}
        self.execCounter = []
        self.outputFunctions = {'out': self.execFunction}
        self.stage = 0
        self.dpgNode = None
        self.imgPreview = {}
        self.playDefaultOut = 'out'
        self.texture = []
        self.textureSize = [128,128]
        self.needsUpdate = True

        self.initFunction()

    def __setstate__(self, state):
        # self.__init__(state['name'])
        self.name = state['name']
        print("new name is ----->" + state['name'])
        self.inputConnections = state['inputConnections']
        self.params = state['params']
        self.inputCache = state['inputCache']
        self.execCounter = state['execCounter']
        self.outputFunctions = state['outputFunctions']
        self.stage = 0
        self.dpgNode = state['dpgNode']
        self.imgPreview = state['imgPreview']
        self.playDefaultOut = state['playDefaultOut']
        self.texture = state['texture']
        self.textureSize = state['textureSize']
        self.needsUpdate = True

        if len(self.texture) > 0:
            self.textureSize[0] = 128
            self.textureSize[1] = 128

            self.texture=[]

            for i in range(0, self.textureSize[0]*self.textureSize[1]):
                self.texture.append(255)
                self.texture.append(0)
                self.texture.append(255)

        self.initFunction()

        print(str(self.dpgNode))
        self.addToNodeEditor("Node Editor 1##demo", self.dpgNode)
        print(state)

    # def __del__(self):
    #    for ic in self.inputConnections:

    def setUpdated(self):
        set_item_color(self.name,1,[0.5,0.5,0.5])

        self.needsUpdate = False

    def setOutofdate(self):
        self.needsUpdate = True

    def doesNeedUpdate(self):
        if self.needsUpdate:
            return True
        if hasattr(self,'inputConnections'):
            for connectionName in list(self.inputConnections):
                connection = self.inputConnections[connectionName]
                print("connection: " + str(connection))
                nodeRef = connection['connection']

                if hasattr(nodeRef, 'doesNeedUpdate'):
                    if nodeRef.doesNeedUpdate():
                        return True
        return False

    def setStage(self, stage):
        self.stage = stage
        print(self.name + "(" + self.className + ")\t" + str(
            self.execCounter) + "\t changed stage to: " + self.getStageName(stage))

    def getStageName(self, stage):
        stageNames = ['noInit', 'init', 'pre', 'getInputVals', 'exec', 'post', 'done']
        return stageNames[stage]

    def initFunction(self):
        self.setStage(1)
        pass

    def preFunction(self):
        self.setStage(2)
        pass

    def execFunction(self):
        self.setStage(4)
        pass

    def postFunction(self):
        self.setStage(5)
        pass

    def getInputValuesIfNeeded(self):
        if self.doesNeedUpdate():
            self.inputCache = {}
            self.setStage(3)
            for paramName in self.inputConnections:
                if hasattr(self.inputConnections[paramName]['connection'], 'exec'):
                    self.inputCache[paramName] = self.inputConnections[paramName]['connection'].exec(self.execCounter[:], self.inputConnections[paramName]['outname'])
                else:
                    self.inputCache[paramName] = None

        self.setUpdated()

    def getInputValues(self):
        self.inputCache = {}
        self.setStage(3)
        for paramName in self.inputConnections:
            if hasattr(self.inputConnections[paramName]['connection'], 'exec'):
                self.inputCache[paramName] = self.inputConnections[paramName]['connection'].exec(self.execCounter[:], self.inputConnections[paramName]['outname'])
            else:
                self.inputCache[paramName] = None

    def exec(self, execCounter, outName):
        if outName == self.playDefaultOut:
            self.execCounter = execCounter
            execCounter.append(0)

            self.preFunction()
            self.getInputValues()

        # retVal = self.execFunction()
        retVal = self.outputFunctions[outName]()

        if outName == self.playDefaultOut:
            self.postFunction()
            self.setStage(6)

        self.setUpdated()

        return retVal

    def play(self):
        retVal = self.exec([0], self.playDefaultOut)
        print(retVal)
        return retVal

    def editViNode(self, sender, data):
        add_window("Edit Node", width=250, height=100)
        add_text("Please enter unique name:")
        add_input_text("NodeName##Editor", on_enter=True, callback=self.editViNode2, callback_data=data)
        add_button("Change", callback=self.editViNode2, callback_data=data)
        end()
        # focus_item("NodeName##addToNodeEditor") #https://github.com/hoffstadt/DearPyGui/issues/159

    def editViNode2(self, sender, data, node):
        newName = get_value("NodeName##Editor")
        oldName = self.name

        print("OLD NAME:" + oldName + " NEW NAME:" + newName)

        itemConf = get_item_configuration(oldName)

        # recreate new node!!
        allLinks = get_links("Node Editor 1##demo")[:]

        # delete old node
        delete_item(self.name)

        self.name = newName
        itemConf['name'] = newName
        self.dpgNode = itemConf

        print("self.name:" + self.name)

        newObject = copy.copy(self)

        del NAME_NODE_MAPPING[oldName]
        NAME_NODE_MAPPING[newName] = newObject

        for l in allLinks:
            print("Analyzing link:" + str(l))
            if oldName in l[0]:
                print("added")
                add_node_link("Node Editor 1##demo", l[0].replace(oldName, newName), l[1])
            elif oldName in l[1]:
                print("added")
                add_node_link("Node Editor 1##demo", l[0], l[1].replace(oldName, newName))

        delete_item("Edit Node")

    def deleteViNode(self, sender, data):
        oldName = self.name

        allLinks = get_links("Node Editor 1##demo")[:]

        for nodename in NAME_NODE_MAPPING:
            node = NAME_NODE_MAPPING[nodename]
            for connectionName in list(node.inputConnections):
                connection = node.inputConnections[connectionName]
                print("connection: " + str(connection))
                nodeRef = connection['connection']
                if nodeRef == None:
                    continue
                if nodeRef.name == oldName:
                    print("delete! connection:" + connectionName)
                    del node.inputConnections[connectionName]

        delete_item(self.name)
        del NAME_NODE_MAPPING[oldName]

    def addConnection(self, inputName, nodeRef, nodeFromAtrName):
        print("addConnection inputName: "+ str(inputName))
        print("addConnection nodeRef: "+ str(nodeRef))

        self.inputConnections[inputName] = {'connection': nodeRef, 'outname': nodeFromAtrName}

    def updateParam(self, sender, data):
        # print("updateParam data:"+ data)
        # print("updateParam sender:"+ sender)
        value = get_value(sender)
        # print("updateParam value:"+ str(value))
        self.params[data] = value

    def addToNodeEditor(self, nodeEditor, nodeParams=None):
        print(str(nodeEditor))

        NAME_NODE_MAPPING[self.name] = self

        x_pos = 5
        y_pos = 5
        if (nodeParams):
            x_pos = nodeParams['x_pos']
            y_pos = nodeParams['y_pos']

        print("ADD NODE NAME: " + self.name + " x: " + str(x_pos))
        add_node(self.name, x_pos=x_pos, y_pos=y_pos, parent=nodeEditor)

        for p in self.params:
            add_node_attribute(p + "##" + self.name, static=True)

            if type(self.params[p]) is int:
                add_input_int(p + "##" + self.name + "#input", width=60, default_value=self.params[p],
                              callback=self.updateParam, callback_data=p)
            elif type(self.params[p]) is float:
                add_input_float(p + "##" + self.name + "#input", width=60, default_value=self.params[p],
                                callback=self.updateParam, callback_data=p)
            elif type(self.params[p]) is str:
                add_input_text(p + "##" + self.name + "#input", width=160, default_value=self.params[p],
                               callback=self.updateParam, callback_data=p)
            elif type(self.params[p]) is bool:
                add_checkbox(p + "##" + self.name + "#input", default_value=self.params[p], callback=self.updateParam,
                             callback_data=p)

            end()  # node_attribute

        for p in self.imgPreview:
            add_node_attribute(p + "##" + self.name, static=True)
            print("texture:" + self.imgPreview[p])

            #add_image("img " + p + "##" + self.name, value=self.imgPreview[p])
            add_texture(self.name+"#texture", self.texture, self.textureSize[0], self.textureSize[1], format=mvTEX_RGB_INT)
            add_image("img " + p + "##" + self.name, value=self.name+"#texture")
            # add_image_button("img "+p+"##"+self.name, source=self.imgPreview[p])
            end()  # node_attribute

        i = 0
        for ic in self.inputConnections:
            add_node_attribute(ic + "##" + self.name)
            # add_input_float(self.name+" attr "+ic+"##demo", width=150, callback=link_callback)
            add_text(ic)
            end()  # node_attribute

        for of in self.outputFunctions:
            print("Adding attribute: "+of + "##" + self.name)
            add_node_attribute(of + "##" + self.name, output=True)
            add_indent(offset=100)
            add_text(of)
            unindent()
            end()  # node_attribute

        # add_input_float("F2##demo", width=150,callback=lambda sender, data: print("Sender: %s Data: %s" % (sender, data)))

        # parentConf = get_item_configuration(self.name)
        # print(parentConf)

        add_node_attribute("Play attr" + "##" + self.name, static=True)
        add_button("Play" + "##" + self.name, callback=self.play)
        add_same_line()
        add_button("Edit" + "##" + self.name, callback=self.editViNode)
        add_same_line()
        add_button("Del" + "##" + self.name, callback=self.deleteViNode)
        end()  # node_attribute

        end()  # node

    def getItemConfig(self):
        self.dpgNode = get_item_configuration(self.name)
        print(str(self.dpgNode))

    def linkCallback(self, nodeFrom, nodeFromAtrName, attrName):
        print(self.name + " has new connection from atr:" + nodeFromAtrName + " to attr: " + attrName)
        self.addConnection(attrName, nodeFrom, nodeFromAtrName)
