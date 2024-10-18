from utilities import *
from template_nodes import *
import unittest
import sys
import os
import time

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

import ioiocore as ioc

class PipelineTests(unittest.TestCase):
    def test_add_nodes(self):
        "Tests if nodes can be added to a pipeline and removed from the pipeline.\n"
        res = False
        try:
            p = ioc.Pipeline()
            p.add_node('source', Source())
            p.add_node('filter', Filter())
            p.add_node('sink', Sink(None))

            p.remove_node('source')
            p.remove_node('filter')
            p.remove_node('sink')
            res = True
        except Exception as e:
            print(f"An error occurred: {e}")
            res = False
        assert res
    
    def test_add_with_duplicate_name(self):
        "Tests if the pipeline rejects nodes that are attempted to be added, if the name is already in use.\n"
        res = False
        try:
            p = ioc.Pipeline()
            p.add_node('source', Source())
            p.add_node('filter', Filter())
            p.add_node('filter', Filter())
            p.add_node('sink', Sink(None))

            p.remove_node('source')
            p.remove_node('filter')
            p.remove_node('filter')
            p.remove_node('sink')
            res = False
        except:
            res = True
        assert res

    def test_connect_disconnect(self):
        "Tests if the connection between nodes is working properly. It must not matter if first argument is the input or output node.\n"
        p = ioc.Pipeline()
        p.add_node('source', Source())
        p.add_node('filter', Filter())
        p.add_node('sink', Sink(None))

        p.connect('source','out1','filter','in1')
        p.connect('source','out2','filter','in2')
        p.connect('filter','out1','sink','in1')
        p.connect('filter','out2','sink','in2')

        p.disconnect('source','out1','filter','in1')
        p.disconnect('source','out2','filter','in2')
        p.disconnect('filter','out1','sink','in1')
        p.disconnect('filter','out2','sink','in2')

        p.connect('filter','in1','source','out1')
        p.connect('filter','in2','source','out2')
        p.connect('sink','in1','filter','out1')
        p.connect('sink','in2','filter','out2')

        p.disconnect('filter','in1','source','out1')
        p.disconnect('filter','in2','source','out2')
        p.disconnect('sink','in1','filter','out1')
        p.disconnect('sink','in2','filter','out2')

        p.remove_node('source')
        p.remove_node('filter')
        p.remove_node('sink')

    def test_pipeline(self):
        "Tests if data is propagated properly for frequency sources, where continous data streams are sent as soon as \'start\' is called until \'stop\'is called"
        global dataReceivedCnt
        dataReceivedCnt = 0

        global p
        p = ioc.Pipeline()

        global sampling_rate
        sampling_rate = 250

        def event_handler(data):
            if data[0][0,0] == sampling_rate/2:
                p.stop()
            global dataReceivedCnt
            dataReceivedCnt += 1

        p.add_node('source', Counter([{'name':'out1','datatype':None},{'name':'out2','datatype':None}], sampling_rate, 8))
        p.add_node('filter', Filter())
        p.add_node('sink', Sink(event_handler))

        p.connect('source','out1','filter','in1')
        p.connect('source','out2','filter','in2')
        p.connect('filter','out1','sink','in1')
        p.connect('filter','out2','sink','in2')

        p.start()

        timeOutS = 1
        start = time.time()
        t = 0
        while dataReceivedCnt < sampling_rate/2 and t < timeOutS:
            t = time.time() - start
            time.sleep(0.01)

        p.stop()

        p.disconnect('source','out1','filter','in1')
        p.disconnect('source','out2','filter','in2')
        p.disconnect('filter','out1','sink','in1')
        p.disconnect('filter','out2','sink','in2')

        p.remove_node('source')
        p.remove_node('filter')
        p.remove_node('sink')
        del p

        if t > timeOutS:
            assert False

        assert dataReceivedCnt >= sampling_rate/2

if __name__ == '__main__':
    try:
        filePath =  os.path.join(dir, os.path.basename(__file__).replace(".py", "") + ".txt") 
        with open(filePath, "w") as f:
            dual_stream = DualStream(f, sys.stdout)
            runner = unittest.TextTestRunner(stream=dual_stream, verbosity=2)
            unittest.main(testRunner=runner, exit=False)
    except SystemExit as e:
        pass