from utilities import *
from template_nodes import *
import unittest
import sys
import os
import numpy as np
import time

class SourcesTests(unittest.TestCase):
    def test_manual_source(self):
        "Tests if data is propagated properly for manual sources, where sending is initiated manually/programmatically by calling send."
        global dataSent
        dataSent = [np.zeros((1, 8)), np.ones((1, 8))]

        global dataReceived
        dataReceived = None

        def event_handler(data):
            global dataReceived
            dataReceived = data

        src = Sender([{'name':'out1','datatype':None},{'name':'out2','datatype':None}])
        filt = Filter()
        sink = Sink(event_handler)

        src.connect_by_id(0, filt, 0)
        src.connect_by_id(1, filt, 1)
        filt.connect_by_id(0, sink, 0)
        filt.connect_by_id(1, sink, 1)

        src.write(dataSent)

        timeOutS = 0.5
        start = time.time()
        t = 0
        while dataReceived is None and t < timeOutS:
            t = time.time() - start
            time.sleep(0.01)

        src.disconnect_by_id(0, filt, 0)
        src.disconnect_by_id(1, filt, 1)
        filt.disconnect_by_id(0, sink, 0)
        filt.disconnect_by_id(1, sink, 1)

        del src
        del filt
        del sink

        if t > timeOutS:
            assert False

        for i in range(0,len(dataSent)):
            assert np.array_equal(dataSent[i], dataReceived[i])

    def test_frequency_source(self):
        "Tests if data is propagated properly for frequency sources, where continous data streams are sent as soon as \'start\' is called until \'stop\'is called"
        global dataReceivedCnt
        dataReceivedCnt = 0

        def event_handler(data):
            if data[0][0,0] == 125:
                src.stop()
            global dataReceivedCnt
            dataReceivedCnt += 1

        samplingRate = 250
        numberOfChannels = 8
        src = Counter([{'name':'out1','datatype':None},{'name':'out2','datatype':None}], samplingRate, numberOfChannels)
        filt = Filter()
        sink = Sink(event_handler)

        src.connect_by_id(0, filt, 0)
        src.connect_by_id(1, filt, 1)
        filt.connect_by_id(0, sink, 0)
        filt.connect_by_id(1, sink, 1)

        src.start()

        timeOutS = 1
        start = time.time()
        t = 0
        while dataReceivedCnt < samplingRate/2 and t < timeOutS:
            t = time.time() - start
            time.sleep(0.01)

        src.disconnect_by_id(0, filt, 0)
        src.disconnect_by_id(1, filt, 1)
        filt.disconnect_by_id(0, sink, 0)
        filt.disconnect_by_id(1, sink, 1)

        del src
        del filt
        del sink

        if t > timeOutS:
            assert False

        assert dataReceivedCnt >= samplingRate/2

    def test_device_source(self):
        "Tests if data is propagated properly for device sources, where continous data streams are sent as soon as \'start\' is called until \'stop\'is called"
        global dataReceivedCnt
        dataReceivedCnt = 0

        def event_handler(data):
            if data[0][0,0] == 125:
                src.stop()
            global dataReceivedCnt
            dataReceivedCnt += 1

        samplingRate = 250
        numberOfChannels = 8
        CounterDevice.start_scanning()
        devices = CounterDevice.get_available_devices()
        CounterDevice.stop_scanning()

        src = CounterDevice(devices[0], samplingRate, numberOfChannels)
        filt = Filter()
        sink = Sink(event_handler)

        src.connect_by_id(0, filt, 0)
        src.connect_by_id(1, filt, 1)
        filt.connect_by_id(0, sink, 0)
        filt.connect_by_id(1, sink, 1)

        src.start()

        timeOutS = 1
        start = time.time()
        t = 0
        while dataReceivedCnt < samplingRate/2 and t < timeOutS:
            t = time.time() - start
            time.sleep(0.01)

        src.disconnect_by_id(0, filt, 0)
        src.disconnect_by_id(1, filt, 1)
        filt.disconnect_by_id(0, sink, 0)
        filt.disconnect_by_id(1, sink, 1)

        del src
        del filt
        del sink

        if t > timeOutS:
            assert False

        assert dataReceivedCnt >= samplingRate/2
        
if __name__ == '__main__':
    try:
        filePath =  os.path.join(dir, os.path.basename(__file__).replace(".py", "") + ".txt") 
        with open(filePath, "w") as f:
            dual_stream = DualStream(f, sys.stdout)
            runner = unittest.TextTestRunner(stream=dual_stream, verbosity=2)
            unittest.main(testRunner=runner, exit=False)
    except SystemExit as e:
        pass