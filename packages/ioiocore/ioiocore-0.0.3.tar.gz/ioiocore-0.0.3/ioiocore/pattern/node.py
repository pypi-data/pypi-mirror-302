from .src.i_node import INode
from .src.o_node import ONode
from abc import abstractmethod
import json
from .constants import *

class Node(INode, ONode):
    def __init__(self, inputPorts : list[dict] = None , outputPorts : list[dict] = None):
        INode.__init__(self, inputPort=inputPorts)
        ONode.__init__(self, outputPort=outputPorts)
    
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

    def __get_output_port_index_by_name(self, node, outputPortName):
        port = None
        for p in node.OutputPorts:
            if p.__dict__()[PortInfo.NAME.value] == outputPortName:
                port = p
                break
        if port is None:
            raise ValueError(f'Could not find input port named \'{outputPortName}\'.')
        
        return node.OutputPorts.index(port)

    def __get_input_port_index_by_name(self, node, inputPortName):
        port = None
        for p in node.InputPorts:
            if p.__dict__()[PortInfo.NAME.value] == inputPortName:
                port = p
                break
            
        if port is None:
            raise ValueError(f'Could not find output port named\'{inputPortName}\'.')
        
        return node.InputPorts.index(port)

    def _update(self):
        if self.InputPorts is None or len(self.InputPorts) <= 0:
            raise TypeError('No input ports defined. Update is only available if input ports are defined.')

        data = []
        for i in range(0,len(self.InputPorts)):
            if(self.InputPorts[i].DataCount > 0):
                data.append(self.InputPorts[i].read())
            else:
                data.append(None)
        
        dataOut = self.update(data)

        if dataOut is not None and self.OutputPorts is not None and len(self.OutputPorts) > 0:
            self.write(dataOut)

    def write(self, data):
        if self.OutputPorts is None or len(self.OutputPorts) <= 0:
            raise TypeError('No output ports defined. Write is only available if output ports are defined.')
        
        if len(data) is not len(self.OutputPorts):
            raise ValueError('Number of OutputPorts do not match received data.')
            
        for i in range(0,len(data)):
            self._write(i, data[i])
    
    def connect_by_name(self, outputPortName, node, inputPortName):
        if self.OutputPorts is None or len(self.OutputPorts) <= 0:
            raise ValueError('Connect is only available if outputs are defined.')
        io = self.__get_output_port_index_by_name(self, outputPortName)
        ii = self.__get_input_port_index_by_name(node, inputPortName)
        self.connect_by_id(io, node, ii)

    def disconnect_by_name(self, outputPortName, node, inputPortName):
        if self.OutputPorts is None or len(self.OutputPorts) <= 0:
            raise ValueError('Connect is only available if outputs are defined.')
        io = self.__get_output_port_index_by_name(self, outputPortName)
        ii = self.__get_input_port_index_by_name(node, inputPortName)
        self.disconnect_by_id(io, node, ii)

    def connect_by_id(self, outputPortId, node, inputPortId):
        if self.OutputPorts is None or len(self.OutputPorts) <= 0:
            raise ValueError('Connect is only available if outputs are defined.')
        if len(self.OutputPorts) <= outputPortId:
            raise ValueError('Port {outputPortId} is out of bounds')
        self.connect(outputPortId, node.InputPorts[inputPortId])

    def disconnect_by_id(self, outputPortId, node, inputPortId):
        if self.OutputPorts is None or len(self.OutputPorts) <= 0:
            raise ValueError('Disconnect is only available if outputs are defined.')
        if len(self.OutputPorts) <= outputPortId:
            raise ValueError('Port {outputPortId} is out of bounds')
        self.disconnect(outputPortId, node.InputPorts[inputPortId])

    @abstractmethod
    def update(self, data):
        pass