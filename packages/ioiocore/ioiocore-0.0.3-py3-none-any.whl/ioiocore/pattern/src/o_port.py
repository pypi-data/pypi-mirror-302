from .i_port import IPort
import json
from ..constants import *

class OPort:
    def __init__(self, portInfo : dict):
        if PortInfo.NAME.value not in portInfo:
            raise ValueError(f'Could not find key \'{PortInfo.NAME.value}\'.')
        if PortInfo.TYPE.value not in portInfo:
            raise ValueError(f'Could not find key \'{PortInfo.TYPE.value}\'.')
        self.__portinfo = portInfo
        self.__inputPorts : list [IPort] = []
        self.IsConnected = False
    
    def __del__(self):
        for port in self.__inputPorts:
            if port is not None:
                port.IsConnected = False
                self.__inputPorts.remove(port)
                self.IsConnected = False

    def __dict__(self):
        return self.__portinfo
    
    def __repr__(self):
        return json.dumps(self.__dict__(), indent=4)

    def connect(self, inputPort : IPort):
        if inputPort.IsConnected:
            raise ValueError('Port is already connected')
        intype = inputPort.__dict__()[PortInfo.TYPE.value]
        outtype = self.__dict__()[PortInfo.TYPE.value]
        if intype is not outtype:
            raise ValueError(f'Can\'t connect \'{outtype}\' to \'{intype}\'')
        if isinstance(inputPort, IPort):
            inputPort.IsConnected = True
            self.__inputPorts.append(inputPort)
            self.IsConnected = True
        else:
            raise TypeError("'inputPort' must be type of 'InputPort'")
        
    def disconnect(self, inputPort : IPort):
        if len(self.__inputPorts) > 0:
            inputPort.IsConnected = False
            self.__inputPorts.remove(inputPort)
            self.IsConnected = False

    def write(self, data):
        if len(self.__inputPorts) > 0:
            for inputPort in self.__inputPorts:
                inputPort.write(data)