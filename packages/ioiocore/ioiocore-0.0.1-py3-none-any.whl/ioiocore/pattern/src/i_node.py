from .i_port import IPort
import threading
from abc import ABC, abstractmethod
from enum import Enum
import time

class INode(ABC):
    class UpdateMode(Enum):
        Synchronized = 1 #update when all input ports delivered data
        Asynchron = 2    #update when any input ports delivered data

    def __init__(self, inputPort : list[str]):
        self.InputPorts : list[IPort] = []
        for p in inputPort:
            port = IPort(p)
            port.set_data_available_eventhandler(self.__on_data_available)
            self.InputPorts.append(port)
        self.NodeUpdateMode = self.UpdateMode.Synchronized

        self.__event : threading.Event = threading.Event()
        self.__updateThreadRunning = False
        self.__updateThread = None
        self.__updateCnt = 0
        self.__totalTimeMs = 0
        self.__updateTimeMs = 0
        self.__start()

    def __del__(self):
        self.__stop()

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
                        self.update()
                        end = time.time()
                        self.__updateCnt += 1
                        self.__totalTimeMs += (end - start)*1000
                        self.__updateTimeMs = self.__totalTimeMs / self.__updateCnt

                self.__event.wait()
                self.__event.clear()
                    
        except Exception as e:
            self.__stop()

    @abstractmethod
    def update(self):
        pass