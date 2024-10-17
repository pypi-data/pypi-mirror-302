from .i_node import INode
from .o_node import ONode
from abc import abstractmethod
import json
from ..templates.utilities.constants import *

class IONode(INode, ONode):
    def __init__(self, inputPorts : list[dict] = None , outputPorts : list[dict] = None, output_metadata : list[dict] = None):
        INode.__init__(self, inputPort=inputPorts)
        ONode.__init__(self, outputPort=outputPorts, metadata = output_metadata)
        self.Metadata = ONode._get_metadata(self)

    def __del__(self):
        pass
        
    def __dict__(self):
        ip = []
        for p in self.InputPorts:
            ip.append(p.__dict__())
        op = []
        for p in self.OutputPorts:
            op.append(p.__dict__())
        return {NodeInfo.NODE.value : self.__class__.__name__, NodeInfo.INPUTS.value : ip, NodeInfo.OUTPUTS.value : op}

    def __repr__(self):
        return json.dumps(self.__dict__(), indent=4)

    def _init(self, data, metadata):
        self.Metadata = metadata
        self.init(data, metadata)

    def _step(self, data):
        dataOut = self.step(data)

        if dataOut is not None and self.OutputPorts is not None and len(self.OutputPorts) > 0:
            if len(self.OutputPorts) != len(dataOut):
                raise ValueError(f'Could not write data. Dimensions do not match. Data: {len(dataOut)} Port: {len(self.OutputPorts)}.')
            self.send(dataOut)
    
    def connect_by_name(self, outputPortName, node, inputPortName):
        if self.OutputPorts is None or len(self.OutputPorts) <= 0:
            raise ValueError('Connect is only available if outputs are defined.')
        io = ONode._get_port_index_by_name(self, outputPortName)
        ii = INode._get_port_index_by_name(node, inputPortName)
        self.connect_by_id(io, node, ii)

    def disconnect_by_name(self, outputPortName, node, inputPortName):
        if self.OutputPorts is None or len(self.OutputPorts) <= 0:
            raise ValueError('Connect is only available if outputs are defined.')
        io = ONode._get_port_index_by_name(self, outputPortName)
        ii = INode._get_port_index_by_name(node, inputPortName)
        self.disconnect_by_id(io, node, ii)

    def connect_by_id(self, outputPortId, node, inputPortId):
        ONode.connect_by_id(self, outputPortId, node.InputPorts[inputPortId])

    def disconnect_by_id(self, outputPortId, node, inputPortId):
        ONode.disconnect_by_id(self, outputPortId, node.InputPorts[inputPortId])

    def send(self, data):
        ONode.send(self, data)

    def init(self, data, metadata):
        if self.OutputPorts is not None and len(self.OutputPorts) > 0:
            self._set_metadata(metadata)

    @abstractmethod
    def step(self, data):
        pass