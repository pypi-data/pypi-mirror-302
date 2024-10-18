from .i_port import IPort
import threading
from abc import ABC, abstractmethod
from enum import Enum
import time
import json
from ..templates.utilities.constants import *

class INode(ABC):
    class UpdateMode(Enum):
        Synchronized = 1 #update when all input ports delivered data
        Asynchron = 2    #update when any input ports delivered data

    def __init__(self, inputPort : list[dict]):
        self.InputPorts : list[IPort] = []
        if inputPort is not None and len(inputPort) > 0:
            for p in inputPort:
                if any(p[PortInfo.NAME.value] in ip.__dict__()[PortInfo.NAME.value] for ip in self.InputPorts):
                    raise ValueError(f'Duplicate output port found {str(p)}. Every port must feature a unique name')
                p[PortInfo.ID.value] = len(self.InputPorts)
                port = IPort(p)
                port._set_data_available_eventhandler(self.__on_data_available)
                self.InputPorts.append(port)
            self.NodeUpdateMode = self.UpdateMode.Synchronized

            self.__event : threading.Event = threading.Event()
            self.__updateThreadRunning = False
            self.__updateThread = None
            self._updateCnt = 0
            self._totalTimeMs = 0
            self._updateTimeMs = 0
            self.__start()

    def __del__(self):
        if self.InputPorts is not None and len(self.InputPorts) > 0:
            self.__stop()

    def __dict__(self):   
        ip = []
        for p in self.InputPorts:
            ip.append(p.__dict__())
        return {NodeInfo.INPUTS.value:ip}

    def __repr__(self):
        return json.dumps(self.__dict__(), indent=4)

    def __start(self):
        if not self.__updateThreadRunning:
            self.__updateThreadRunning = True
            self.__updateThread = threading.Thread(target=self.__updateThread_DoWork, daemon=True)
            self.__updateThread.start()
           
    def __stop(self):
        if self.__updateThreadRunning:
            self.__updateThreadRunning = False
            self.__event.set()
            self.__updateThread.join()
            self.__updateThread = None

    def __on_data_available(self):
        if self.NodeUpdateMode is self.UpdateMode.Asynchron:
            self.__event.set()
        else:
            allPortsAcquired = True
            for port in self.InputPorts:
                if port.DataCount <= 0:
                    allPortsAcquired = False
                    break
            if allPortsAcquired:
                self.__event.set()

    def __updateThread_DoWork(self):
        try:
            self.__event.wait()
            self.__event.clear()
            while self.__updateThreadRunning:
                if self.__updateThreadRunning:
                    updateCnt = -1
                    for port in self.InputPorts:
                        if updateCnt == -1 or port.DataCount <= updateCnt:
                            updateCnt = port.DataCount
                    for i in range(updateCnt):
                        start = time.time()
                        self.__step()
                        end = time.time()
                        self._updateCnt += 1
                        self._totalTimeMs += (end - start)*1000
                        self._updateTimeMs = self._totalTimeMs / self._updateCnt

                self.__event.wait()
                self.__event.clear()    
        except:
            self.__stop()
    
    def __step(self):
        if self.InputPorts is None or len(self.InputPorts) <= 0:
            raise TypeError('No input ports defined. Update is only available if input ports are defined.')

        data = []
        for i in range(0,len(self.InputPorts)):
            if(self.InputPorts[i].DataCount > 0):
                data.append(self.InputPorts[i]._read())
            else:
                data.append(None)
        
        if self._updateCnt <= 0:
            metadata = []
            for ip in self.InputPorts:
                metadata.append(ip._get_metadata())
            self._init(data, metadata)
        self._step(data)
    
    def _get_port_index_by_name(self, inputPortName):
        port = None
        for p in self.InputPorts:
            if p.__dict__()[PortInfo.NAME.value] == inputPortName:
                port = p
                break
            
        if port is None:
            raise ValueError(f'Could not find output port named\'{inputPortName}\'.')
        
        return self.InputPorts.index(port)

    @abstractmethod
    def _init(self, data, metadata):
        pass

    @abstractmethod
    def _step(self, data):
        pass