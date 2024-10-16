from utilities import *
from template_nodes import *
import unittest
import numpy as np
import time

class NodeTests(unittest.TestCase):
    def test_single_sample_basic_functionality(self):
        "Tests if a single sample can be sent from a source, forwarded through a filter and received by a sink node with two channels each."
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

        del src
        del filt
        del sink

        if t > timeOutS:
            assert False

        for i in range(0,len(dataSent)):
            assert np.array_equal(dataSent[i], dataReceived[i])

    def test_single_sample_basic_crossed_connections(self):
        "Tests if a single sample can be sent from a source, forwarded through a filter and received by a sink node with two channels each. Connections are crossed out to test if data is propagated properly between ports."
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

        src.connect_by_id(0, filt, 1)
        src.connect_by_id(1, filt, 0)
        filt.connect_by_id(0, sink, 1)
        filt.connect_by_id(1, sink, 0)

        src.send(dataSent)

        timeOutS = 0.5
        start = time.time()
        t = 0
        while dataReceived is None and t < timeOutS:
            t = time.time() - start
            time.sleep(0.01)

        src.disconnect_by_id(0, filt, 1)
        src.disconnect_by_id(1, filt, 0)
        filt.disconnect_by_id(0, sink, 1)
        filt.disconnect_by_id(1, sink, 0)

        del src
        del filt
        del sink

        if t > timeOutS:
            assert False

        for i in range(0,len(dataSent)):
            assert np.array_equal(dataSent[i], dataReceived[i])

    def test_single_sample_multiple_inputs_on_one_output(self):
        '''Tests if a single sample can be sent from a source, forwarded through a filter and received by a sink node with two channels each. Output port 1 of source is connected to input port 1 and 2 of filter node. Output port 2 of source node is not connected. Output 1 and 2 of filter node are connected to input 1 and 2 of sink node. All node inputs are connected one node output is not connected. Data must be propagated.'''
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
        src.connect_by_id(0, filt, 1)
        filt.connect_by_id(0, sink, 0)
        filt.connect_by_id(1, sink, 1)

        src.send(dataSent)

        timeOutS = 0.5
        start = time.time()
        t = 0
        while dataReceived is None and t < timeOutS:
            t = time.time() - start
            time.sleep(0.01)

        src.disconnect_by_id(0, filt, 0)
        src.disconnect_by_id(0, filt, 1)
        filt.disconnect_by_id(0, sink, 0)
        filt.disconnect_by_id(1, sink, 1)

        del src
        del filt
        del sink

        if t > timeOutS:
            assert False

        expected = [dataSent[0], dataSent[0]]
        for i in range(0,len(dataSent)):
            assert np.array_equal(expected[i], dataReceived[i])

    def test_single_sample_basic_input_not_connected(self):
        '''Tests if a single sample can be sent from a source, forwarded through a filter and received by a sink node with two channels each. Output port 1 of source is connected to input port 1 of filter node. Output port 2 of source node and input 2 of filter are not connected. Data must not be propagated. A timeout must be reached.'''
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
        filt.connect_by_id(0, sink, 0)

        src.send(dataSent)

        timeOutS = 0.5
        start = time.time()
        t = 0
        while dataReceived is None and t < timeOutS:
            t = time.time() - start
            time.sleep(0.01)

        src.disconnect_by_id(0, filt, 0)
        filt.disconnect_by_id(0, sink, 0)

        del src
        del filt
        del sink

        if t > timeOutS:
            assert True
        else:
            assert False
    
    def test_single_sample_1000_nodes(self):
        "Tests if a single sample can be sent from a source node, forwarded through 1000 filter nodes and received by a sink node with two channels each."
        global dataSent
        dataSent = [np.zeros((1, 8)), np.ones((1, 8))]

        global dataReceived
        dataReceived = None

        def event_handler(data):
            global dataReceived
            dataReceived = data

        numberOfFiltNodes = 1000
        src = Source()
        filt = []
        for i in range(0, numberOfFiltNodes):
            filt.append(Filter())
        sink = Sink(event_handler)

        src.connect_by_id(0, filt[0], 0)
        src.connect_by_id(1, filt[0], 1)
        for i in range(0, numberOfFiltNodes-1):
            filt[i].connect_by_id(0, filt[i+1], 0)
            filt[i].connect_by_id(1, filt[i+1], 1) 
        filt[numberOfFiltNodes-1].connect_by_id(0, sink, 0)
        filt[numberOfFiltNodes-1].connect_by_id(1, sink, 1)

        src.send(dataSent)

        timeOutS = 0.5
        start = time.time()
        t = 0
        while dataReceived is None and t < timeOutS:
            t = time.time() - start
            time.sleep(0.01)

        src.disconnect_by_id(0, filt[0], 0)
        src.disconnect_by_id(1, filt[0], 1)
        for i in range(0, numberOfFiltNodes-1):
            filt[i].disconnect_by_id(0, filt[i+1], 0)
            filt[i].disconnect_by_id(1, filt[i+1], 1) 
        filt[numberOfFiltNodes-1].disconnect_by_id(0, sink, 0)
        filt[numberOfFiltNodes-1].disconnect_by_id(1, sink, 1)

        del src
        for f in filt:
            del f
        del filt
        del sink

        if t > timeOutS:
            assert False

        for i in range(0,len(dataSent)):
            assert np.array_equal(dataSent[i], dataReceived[i])

#TODO ADD TESTS WITH DIFFERENT DATATYPES
#TODO ADD TESTS WITH WITH DYNAMIC ATTACH DETACHING WHILE RUNNING

if __name__ == '__main__':
    try:
        filePath =  os.path.join(dir, os.path.basename(__file__).replace(".py", "") + ".txt") 
        with open(filePath, "w") as f:
            dual_stream = DualStream(f, sys.stdout)
            runner = unittest.TextTestRunner(stream=dual_stream, verbosity=2)
            unittest.main(testRunner=runner, exit=False)
    except SystemExit as e:
        pass