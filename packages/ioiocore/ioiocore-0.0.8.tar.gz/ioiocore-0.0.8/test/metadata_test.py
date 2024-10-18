from utilities import *
from template_nodes import *
import unittest
import numpy as np
import time

class MetadataTests(unittest.TestCase):
    def test_single_sample_basic_functionality(self):
        "Checks if metadata is propagated properly. TODO NOT FINISHED YET/UNTESTED FEATURE"
        global dataSent
        dataSent = [np.zeros((1, 8)), np.ones((1, 8))]

        global dataReceived
        dataReceived = None

        def event_handler(data):
            global dataReceived
            dataReceived = data

        src = Source()
        filt = Filter()
        sink = Sink(event_handler)

        src.connect_by_id(0, filt, 0)
        src.connect_by_id(1, filt, 1)
        filt.connect_by_id(0, sink, 0)
        filt.connect_by_id(1, sink, 1)

        srcmd = src.Metadata

        src.send(dataSent)

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

        sinkmd = sink.Metadata

        del src
        del filt
        del sink

        if t > timeOutS:
            assert False

        for i in range(0,len(dataSent)):
            assert np.array_equal(dataSent[i], dataReceived[i])

        if srcmd == sinkmd:
            assert True

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
        filt1 = Filter()
        filt2 = Filter()
        sink = Sink(event_handler)

        src.connect_by_id(0, filt1, 0)
        src.connect_by_id(1, filt1, 1)
        filt1.connect_by_id(0, filt2, 0)
        filt1.connect_by_id(1, filt2, 1)
        filt2.connect_by_id(0, sink, 0)
        filt2.connect_by_id(1, sink, 1)

        srcmd = src.Metadata

        src.start()

        timeOutS = 1
        start = time.time()
        t = 0
        while dataReceivedCnt < samplingRate/2 and t < timeOutS:
            t = time.time() - start
            time.sleep(0.01)

        sinkmd = sink.Metadata

        src.disconnect_by_id(0, filt1, 0)
        src.disconnect_by_id(1, filt1, 1)
        filt1.disconnect_by_id(0, filt2, 0)
        filt1.disconnect_by_id(1, filt2, 1)
        filt2.disconnect_by_id(0, sink, 0)
        filt2.disconnect_by_id(1, sink, 1)

        del src
        del filt1
        del filt2
        del sink

        if srcmd == sinkmd:
            assert True

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