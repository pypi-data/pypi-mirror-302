from utilities import *
from template_nodes import *
import unittest
import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

import ioiocore as ioc

class SourceInvalid(ioc.Node):
    def __init__(self):
        super().__init__(outputPorts = [{'name':'out1','datatype':None}, {'name':'out1','datatype':None}])

    def send(self, data):
        self._write(data)

    def update(self, data):
        pass
    
class FilterInvalid1(ioc.Node):
    def __init__(self):
        super().__init__(inputPorts = [{'name':'in1','datatype':None}, {'name':'in1','datatype':None}], outputPorts = [{'name':'out1','datatype':None}, {'name':'out2','datatype':None}])

    def update(self, data):
        return data
    
class FilterInvalid2(ioc.Node):
    def __init__(self):
        super().__init__(inputPorts = [{'name':'in1','datatype':None}, {'name':'in2','datatype':None}], outputPorts = [{'name':'out1','datatype':None}, {'name':'out1','datatype':None}])

    def update(self, data):
        return data

'''class FilterInvalid3(ioc.Node):
    def __init__(self):
        super().__init__(inputPorts = [{'name':'in1','datatype':None}, {'name':'in2','datatype':None}], outputPorts = [{'name':'in1','datatype':None}, {'name':'in2','datatype':None}])

    def update(self, data):
        return data'''

class SinkInvalid(ioc.Node):
    def __init__(self, event_handler):
        super().__init__(inputPorts = [{'name':'in1','datatype':None}, {'name':'in1','datatype':None}])
        self.__event_handler = event_handler

    def update(self, data):
        self.__event_handler(data)

class NodeTests(unittest.TestCase):
    def test_valid_port_names(self):
        "Test if nodes with valid port naming conventions can be initialized."
        def init_node( fcn):
            res = False
            try:
                fcn()
                res = True
            except:
                res = False
            return res

        assert init_node( lambda: Source())
        assert init_node( lambda: Filter())
        assert init_node( lambda: Sink(None))

    def test_invalid_port_names(self):
        "Test that nodes with invalid port naming conventions (duplicate portnames) can't be initialized."
        def init_node( fcn):
            res = False
            try:
                fcn()
                res = False
            except:
                res = True
            return res

        assert init_node( lambda: SourceInvalid())
        assert init_node( lambda: FilterInvalid1())
        assert init_node( lambda: FilterInvalid2())
        #assert init_node( lambda: FilterInvalid3())
        assert init_node( lambda: SinkInvalid(None))

if __name__ == '__main__':
    try:
        filePath =  os.path.join(dir, os.path.basename(__file__).replace(".py", "") + ".txt") 
        with open(filePath, "w") as f:
            dual_stream = DualStream(f, sys.stdout)
            runner = unittest.TextTestRunner(stream=dual_stream, verbosity=2)
            unittest.main(testRunner=runner, exit=False)
    except SystemExit as e:
        pass