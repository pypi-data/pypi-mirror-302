from ...pattern.io_node import IONode
from abc import abstractmethod
from ...templates.utilities.constants import *

class Node(IONode):
    def __init__(self, inputPorts : list[dict] = None , outputPorts : list[dict] = None, output_metadata : list[dict] = None):
        IONode.__init__(self, inputPorts, outputPorts) 
        
    def connect_by_name(self, outputPortName, node, inputPortName):
        IONode.connect_by_name(self, outputPortName, node, inputPortName)

    def disconnect_by_name(self, outputPortName, node, inputPortName):
        IONode.disconnect_by_name(self, outputPortName, node, inputPortName)

    def connect_by_id(self, outputPortId, node, inputPortId):
        IONode.connect_by_id(self, outputPortId, node,inputPortId)

    def disconnect_by_id(self, outputPortId, node, inputPortId):
        IONode.disconnect_by_id(self, outputPortId, node,inputPortId)

    def send(self, data):
        IONode.send(self, data)

    def init(self, data, metadata):
        IONode.init(self, data, metadata)

    @abstractmethod
    def step(self, data):
        pass