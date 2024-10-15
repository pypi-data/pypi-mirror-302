from .node import Node
from .frequency_generator import FrequencyGenerator
from abc import abstractmethod

class ManualSource(Node):
    def __init__(self, outputPorts):
        super().__init__(inputPorts=None, outputPorts=outputPorts)

    def __del__(self):
        super().__del__()   

class FixedFrequencySource(Node, FrequencyGenerator):
    def __init__(self, outputPorts, samplingRateHz):
        super().__init__(inputPorts=None, outputPorts=outputPorts)
        super(Node, self).__init__(samplingRateHz)

    def __del__(self):
        super().__del__()
        super(Node, self).__del__()  

    def update(self):
        self.write(self.generate_sample())

    @abstractmethod
    def generate_sample(self):
        pass

class DeviceSource(Node):
    def __init__(self, outputPorts, serial):
        super().__init__(inputPorts=None, outputPorts=outputPorts)

    def __del__(self):
        super().__del__()

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