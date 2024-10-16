from .o_port import OPort
from .i_port import IPort
import json
from ..constants import PortInfo, NodeInfo

class ONode:
    def __init__(self, outputPort : list[dict]):
        self.OutputPorts : list[OPort] = []
        if outputPort is not None and len(outputPort) > 0:
            for p in outputPort:
                if any(p[PortInfo.NAME.value] in ip.__dict__()[PortInfo.NAME.value] for ip in self.OutputPorts):
                    raise ValueError(f'Duplicate output port found {str(p)}. Every port must feature a unique name')
                p[PortInfo.ID.value] = len(self.OutputPorts)
                self.OutputPorts.append(OPort(p))
            self.__writeCnt = 0
        
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

    def connect(self, id : int, inputPort : IPort):
        if id < len(self.OutputPorts):
            self.OutputPorts[id].connect(inputPort)
        else:
            raise IndexError(f"Index {id} out of range.")
        
    def disconnect(self, id : int, inputPort : IPort):
        if id < len(self.OutputPorts):
            self.OutputPorts[id].disconnect(inputPort)
        else:
            raise IndexError(f"Index {id} out of range.")

    def _write(self, id : int, data):
        if id < len(self.OutputPorts):
            self.__writeCnt += 1
            self.OutputPorts[id].write(data)
        else:
            raise IndexError(f"Index {id} out of range.")
