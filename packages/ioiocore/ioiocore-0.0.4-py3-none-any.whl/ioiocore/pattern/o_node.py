from .o_port import OPort
from .i_port import IPort
import json
from ..templates.utilities.constants import PortInfo, NodeInfo

class ONode:
    def __init__(self, outputPort : list[dict], metadata : list[dict]):
        self.OutputPorts : list[OPort] = []
        if outputPort is not None and len(outputPort) > 0:
            for i in range(0, len(outputPort)):
                if any(outputPort[i][PortInfo.NAME.value] in ip.__dict__()[PortInfo.NAME.value] for ip in self.OutputPorts):
                    raise ValueError(f'Duplicate output port found {str(outputPort[i])}. Every port must feature a unique name')
                outputPort[i][PortInfo.ID.value] = len(self.OutputPorts)
                self.OutputPorts.append(OPort(outputPort[i]))
            self.__writeCnt = 0
        self._set_metadata(metadata)
        self.Metadata = self._get_metadata()
  
    def __del__(self):
        if self.OutputPorts is not None and len(self.OutputPorts) > 0:
            for outputPort in self.OutputPorts:
                outputPort.__del__()
                del(outputPort)

    def __dict__(self):   
        op = []
        for p in self.OutputPorts:
            op.append(p.__dict__())
        return {NodeInfo.OUTPUTS.value: op}

    def __repr__(self):
        return json.dumps(self.__dict__(), indent=4)

    def _set_metadata(self, metadata : list[dict]):
        if metadata is not None and len(metadata) != len(self.OutputPorts):
            raise ValueError(f'Dimensions of metadata and outputs must be identical if set. \'{len(metadata)}\' != \'{len(self.OutputPorts)}\'.')
        if self.OutputPorts is not None and len(self.OutputPorts) > 0:
            for i in range(0, len(self.OutputPorts)):
                if metadata is None:
                    self.OutputPorts[i]._set_metadata(None)
                else:
                    self.OutputPorts[i]._set_metadata(metadata[i])
    
    def _get_metadata(self):
        metadata = []
        if self.OutputPorts is not None and len(self.OutputPorts) > 0:
            for i in range(0, len(self.OutputPorts)):
                metadata.append(self.OutputPorts[i]._get_metadata())
        return metadata

    def _get_port_index_by_name(self, outputPortName : str):
        port = None
        for p in self.OutputPorts:
            if p.__dict__()[PortInfo.NAME.value] == outputPortName:
                port = p
                break
        if port is None:
            raise ValueError(f'Could not find input port named \'{outputPortName}\'.')
        
        return self.OutputPorts.index(port)

    def connect_by_id(self, id : int, inputPort : IPort):
        if self.OutputPorts is None or len(self.OutputPorts) <= 0:
            raise ValueError('Connect is only available if outputs are defined.')
        if len(self.OutputPorts) <= id:
            raise ValueError('Port {outputPortId} is out of bounds')    
        self.OutputPorts[id]._connect(inputPort)
        
    def disconnect_by_id(self, id : int, inputPort : IPort):
        if self.OutputPorts is None or len(self.OutputPorts) <= 0:
            raise ValueError('Disconnect is only available if outputs are defined.')
        if len(self.OutputPorts) <= id:
            raise ValueError('Port {outputPortId} is out of bounds')
        self.OutputPorts[id]._disconnect(inputPort)

    def send(self, data):
        if self.OutputPorts is None or len(self.OutputPorts) <= 0:
            raise TypeError('No output ports defined. Write is only available if output ports are defined.')
        
        if len(data) is not len(self.OutputPorts):
            raise ValueError('Number of OutputPorts do not match received data.')
            
        for i in range(0,len(data)):
            self.__write(i, data[i])

    def __write(self, id : int, data):
        if id < len(self.OutputPorts):
            self.__writeCnt += 1
            self.OutputPorts[id]._write(data)
        else:
            raise IndexError(f"Index {id} out of range.")
