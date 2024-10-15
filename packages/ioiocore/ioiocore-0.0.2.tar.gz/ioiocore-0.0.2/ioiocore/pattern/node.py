from .src.i_node import INode
from .src.o_node import ONode
from abc import abstractmethod
import json

class Node(INode, ONode):
    def __init__(self, inputPorts : list[str] = None , outputPorts : list[str] = None):
        if inputPorts is not None and len(inputPorts) == 0:
            inputPorts = None
        if outputPorts is not None and len(outputPorts) == 0:
            outputPorts = None
        if inputPorts is None and outputPorts is None:
            raise ValueError('Node without inputs and outputs is not allowed. \'inputPorts\' and/or \'outputPorts\' must be defined.')
        if inputPorts is not None:
            duplicates = self.__checkForDuplicates(inputPorts)
            if duplicates:
                raise ValueError(f'Duplicate input port names found {duplicates}. Every port must feature a unique name')
        if outputPorts is not None:
            duplicates = self.__checkForDuplicates(outputPorts)
            if duplicates:
                raise ValueError(f'Duplicate input port names found {duplicates}. Every port must feature a unique name')
        if inputPorts is not None and outputPorts is not None:
            duplicates = self.__checkForDuplicates(outputPorts + inputPorts)
            if len(duplicates) > 0:
                raise ValueError(f'Duplicate port names found {duplicates}. Every port must feature a unique name')
        
        INode.__init__(self, inputPort=inputPorts)
        ONode.__init__(self, outputPort=outputPorts)

    def __checkForDuplicates(self, l):
        seen = set()
        duplicates = set()
        for item in l:
            if item in seen:
                duplicates.add(item)
            else:
                seen.add(item)
        return duplicates
    
    def __del__(self):
        pass

    def __dict__(self):
        oPorts = {}
        iPorts = {}
        if self.OutputPorts is not None and len(self.OutputPorts) >= 0:
            cnt = 0
            for op in self.OutputPorts:
                oPorts[cnt] = op.PortName
                cnt+=1
        if self.InputPorts is not None and len(self.InputPorts) >= 0:
            cnt = 0
            for ip in self.InputPorts:
                iPorts[cnt] = ip.PortName
                cnt+=1

        return {
            "name" : self.__class__.__name__,
            "outputs" : oPorts,
            "inputs" : iPorts
        }

    def __repr__(self):
        return json.dumps(self.__dict__(), indent=4)

    def __get_output_port_index_by_name(self, node, outputPortName):
        port = None
        for p in node.OutputPorts:
            if p.PortName == outputPortName:
                port = p
                break
        if port is None:
            raise ValueError(f'Could not find input port named \'{outputPortName}\'.')
        
        return node.OutputPorts.index(port)

    def __get_input_port_index_by_name(self, node, inputPortName):
        port = None
        for p in node.InputPorts:
            if p.PortName == inputPortName:
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