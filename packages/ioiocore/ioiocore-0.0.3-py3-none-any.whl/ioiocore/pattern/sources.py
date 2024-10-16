from .node import Node
from .frequency_generator import FrequencyGenerator
from abc import abstractmethod

class ManualSource(Node):
    def __init__(self, outputPorts):
        Node.__init__(self, inputPorts=None, outputPorts=outputPorts)

    def __del__(self):
        Node.__del__(self)   

    def write(self, data):
        Node.write(self, data)


class FixedFrequencySource(Node, FrequencyGenerator):
    def __init__(self, outputPorts, samplingRateHz):
        Node.__init__(self, inputPorts=None, outputPorts=outputPorts)
        FrequencyGenerator.__init__(self, samplingRateHz)

    def __del__(self):
        Node.__del__(self)
        FrequencyGenerator.__del__(self)  

    def update(self):
        self.write(self.generate_sample())

    @abstractmethod
    def generate_sample(self):
        pass

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