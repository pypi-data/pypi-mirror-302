from ..common.node import Node
from abc import abstractmethod
from ..utilities.constants import *
from ..utilities.frequency_generator import FrequencyGenerator

class DeviceSource(Node):
    def __init__(self, outputPorts):
        metadata = []
        for p in outputPorts:
            metadata.append({Metadata.SAMPLING_RATE.value : -1})
        Node.__init__(self, inputPorts=None, outputPorts=outputPorts, output_metadata=metadata)

    def __del__(self):
        Node.__del__(self)

    def init(self, data, metadata):
        return metadata

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