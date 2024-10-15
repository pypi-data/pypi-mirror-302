from .i_port import IPort

class OPort:
    def __init__(self, portName : str):
        self.__inputPorts : list [IPort] = []
        self.PortName = portName
        self.IsConnected = False
    
    def __del__(self):
        for port in self.__inputPorts:
            if port is not None:
                port.IsConnected = False
                self.__inputPorts.remove(port)
                self.IsConnected = False

    def connect(self, inputPort : IPort):
        if inputPort.IsConnected:
            raise ValueError('Port is already connected')
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