from ..common.node import Node
from ..utilities.frequency_generator import FrequencyGenerator
from abc import abstractmethod
from ..utilities.constants import *

class TimeseriesSource(Node, FrequencyGenerator):
    def __init__(self, outputPorts, samplingRateHz):
        metadata = []
        for p in outputPorts:
            metadata.append([{Metadata.SAMPLING_RATE.value : samplingRateHz}])
        Node.__init__(self, inputPorts=None, outputPorts=outputPorts, output_metadata=metadata)        
        FrequencyGenerator.__init__(self, samplingRateHz)

    def __del__(self):
        Node.__del__(self)
        FrequencyGenerator.__del__(self)  

    def step(self):
        self.send(self.generate_sample())

    @abstractmethod
    def generate_sample(self):
        pass