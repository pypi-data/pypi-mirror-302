from ...pattern.io_node import IONode
from abc import abstractmethod
from ..utilities.constants import *

class TimeseriesNode(IONode):
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
        metadata = self.ts_init(data, metadata)
        if metadata is None:
            if self.OutputPorts is not None and len(self.OutputPorts) > 0:
                self._set_metadata(metadata)
        if Metadata.SAMPLING_RATE.value not in metadata:
            raise ValueError(f'\'{self.__class__.__name__}\' requires a node featuring \'{Metadata.SAMPLING_RATE.value}\' as an input.')
        IONode.init(self, data, metadata)

    @abstractmethod
    def ts_init(self, data, metadata):
        pass

    @abstractmethod
    def step(self, data):
        pass