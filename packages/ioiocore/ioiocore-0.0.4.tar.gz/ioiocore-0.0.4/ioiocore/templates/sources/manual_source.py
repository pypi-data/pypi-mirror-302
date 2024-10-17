from ..common.node import Node
from ..utilities.frequency_generator import FrequencyGenerator
from abc import abstractmethod
from ..utilities.constants import *

class ManualSource(Node):
    def __init__(self, outputPorts):
        Node.__init__(self, inputPorts=None, outputPorts=outputPorts)

    def __del__(self):
        Node.__del__(self)   

    def send(self, data):
        Node.send(self, data)