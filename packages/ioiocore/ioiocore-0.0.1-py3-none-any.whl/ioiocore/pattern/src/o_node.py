from .o_port import OPort
from .i_port import IPort

class ONode:
    def __init__(self, outputPort : list[str]):
        self.OutputPorts : list[OPort] = []
        for s in outputPort:
            self.OutputPorts.append(OPort(s))
        self.__writeCnt = 0
        
    def __del__(self):
        for outputPort in self.OutputPorts:
            del(outputPort)
        
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

    def write(self, id : int, data):
        if id < len(self.OutputPorts):
            self.__writeCnt += 1
            self.OutputPorts[id].write(data)
        else:
            raise IndexError(f"Index {id} out of range.")
