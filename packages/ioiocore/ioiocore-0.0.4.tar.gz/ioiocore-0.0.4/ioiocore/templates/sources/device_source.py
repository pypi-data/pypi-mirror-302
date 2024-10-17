from ..common.node import Node
from abc import abstractmethod
from ..utilities.constants import *
from ..utilities.frequency_generator import FrequencyGenerator

class DeviceSource(Node):
    def __init__(self, outputPorts, serial):
        Node.__init__(self, inputPorts=None, outputPorts=outputPorts)

    def __del__(self):
        Node.__del__(self)

    @staticmethod
    @abstractmethod
    def start_scanning():
        pass

    @staticmethod
    @abstractmethod
    def stop_scanning():
        pass

    @staticmethod
    @abstractmethod
    def get_available_devices():
        pass

    @abstractmethod
    def open(self, serial):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass