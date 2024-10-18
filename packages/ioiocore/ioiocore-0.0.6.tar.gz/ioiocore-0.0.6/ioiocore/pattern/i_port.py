import queue
import json
from ..templates.utilities.constants import *

class IPort:
    def __init__(self, portInfo : dict):   
        if PortInfo.NAME.value not in portInfo:
            raise ValueError(f'Could not find key \'{PortInfo.NAME.value}\'.')
        if PortInfo.TYPE.value not in portInfo:
            raise ValueError(f'Could not find key \'{PortInfo.TYPE.value}\'.')
        self.__portinfo = portInfo
        self.DataCount : int = 0
        self.IsConnected = False
        self.__queue : queue.Queue = queue.Queue()
        self.__eventHandler : function
        self.__readCnt = 0
        self.__metadata = None
    
    def __dict__(self):
        return self.__portinfo
    
    def __repr__(self):
        return json.dumps(self.__dict__(), indent=4)

    def _set_metadata(self, metadata):
        self.__metadata = metadata
    
    def _get_metadata(self):
        return self.__metadata

    def _write(self, data):
        self.__queue.put(data, block=True, timeout=None)
        self.DataCount = self.__queue.qsize()
        if self.__eventHandler is not None:
            self.__eventHandler()

    def _read(self):
        if self.DataCount > 0:
            try:
                self.__readCnt += 1
                return self.__queue.get(block=True, timeout=None)
            except:
                return None
        else:
            return None 

    def _set_data_available_eventhandler(self, handler):
        self.__eventHandler = handler

    def _remove_data_available_eventhandler(self, handler):
        self.__eventHandler = None