import sys
import os
import numpy as np

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

import ioiocore as ioc

class Source(ioc.Node):
    def __init__(self):
        super().__init__(outputPorts = [{'name' : 'out1', 'datatype' : None}, {'name' : 'out2', 'datatype' : None}])

    def update(self, data):
        pass

    def send(self, data):
        self.write(data)

class Filter(ioc.Node):
    def __init__(self):
        super().__init__(inputPorts = [{'name' : 'in1', 'datatype' : None}, {'name' : 'in2', 'datatype' : None}], outputPorts = [{'name' : 'out1', 'datatype' : None}, {'name' : 'out2', 'datatype' : None}])

    def update(self, data):
        return data

class Sink(ioc.Node):
    def __init__(self, event_handler):
        super().__init__(inputPorts = [{'name' : 'in1', 'datatype' : None}, {'name' : 'in2', 'datatype' : None}])
        self.__event_handler = event_handler

    def update(self, data):
        self.__event_handler(data)

class Sender(ioc.ManualSource):
    def __init__(self, outputPorts):
        super().__init__(outputPorts)
    
    def update(self, data):
        pass

class Counter(ioc.FixedFrequencySource):
    def __init__(self, outputPorts, samplingRateHz=250, numberOfChannels=8):
        super().__init__(outputPorts, samplingRateHz)
        self.__cnt = 0
        self.__numberOfChannels = numberOfChannels

    def generate_sample(self):
        self.__cnt += 1
        return [np.ones((1, self.__numberOfChannels)) * self.__cnt,np.ones((1, self.__numberOfChannels)) * self.__cnt * -1]

class CounterDevice(ioc.DeviceSource):
    __deviceNames = []
    
    class FGCounter(ioc.FrequencyGenerator):
        def __init__(self, frequencyHz, numberOfChannels, handler):
            super().__init__(frequencyHz)
            self.__cnt = 0
            self.__numberOfChannels = numberOfChannels
            self.__handler = handler

        def __del__(self):
            self.__cnt += 1
            self.__handler = None

        def update(self):
            self.__cnt += 1    
            self.__handler([np.ones((1, self.__numberOfChannels)) * self.__cnt,np.ones((1, self.__numberOfChannels)) * self.__cnt * -1])

    def __init__(self, serial, samplingRate =250, numberOfChannels=8):
        self.__outputPorts = [{'name' : 'out1', 'datatype' : None}, {'name' : 'out2', 'datatype' : None}]
        self.__samplingRate = samplingRate
        self.__numberOfChannels = numberOfChannels
        self.__serial = serial
        super().__init__(self.__outputPorts, self.__serial)
        self.open()
    
    def  __del__(self):
        self.close()

    @staticmethod
    def start_scanning():
        if len(CounterDevice.__deviceNames) <= 0:
            CounterDevice.__deviceNames.append('CNT-0000.00.00')
            CounterDevice.__deviceNames.append('CNT-0000.00.01')
            CounterDevice.__deviceNames.append('CNT-0000.00.02')

    @staticmethod
    def stop_scanning():
        pass

    @staticmethod
    def get_available_devices():
        return CounterDevice.__deviceNames
    
    def open(self):
        serials = CounterDevice.get_available_devices()
        if self.__serial not in serials:
            raise ValueError(f"Could not find {self.__serial}.")
        self.__cnt = CounterDevice.FGCounter(self.__samplingRate, self.__numberOfChannels, self.write)

    def close(self):
        pass

    def start(self):
        self.__cnt.start()
    
    def stop(self):
        self.__cnt.stop()
    
    def update(self, data):
        pass
