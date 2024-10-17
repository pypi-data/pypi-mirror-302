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

        print(src.Metadata)
        print(filt.Metadata)
        print(sink.Metadata)

        src.send(dataSent)

        timeOutS = 0.5
        start = time.time()
        t = 0
        while dataReceived is None and t < timeOutS:
            t = time.time() - start
            time.sleep(0.01)

        print(src.Metadata)
        print(filt.Metadata)
        print(sink.Metadata)

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

if __name__ == '__main__':
    try:
        filePath =  os.path.join(dir, os.path.basename(__file__).replace(".py", "") + ".txt") 
        with open(filePath, "w") as f:
            dual_stream = DualStream(f, sys.stdout)
            runner = unittest.TextTestRunner(stream=dual_stream, verbosity=2)
            unittest.main(testRunner=runner, exit=False)
    except SystemExit as e:
        pass