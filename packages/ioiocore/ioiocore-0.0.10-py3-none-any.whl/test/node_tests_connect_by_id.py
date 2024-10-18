from utilities import *
from template_nodes import *
import unittest

class NodeTests_ConnectByID(unittest.TestCase):    
    def test_connect_by_id_no_disconnect(self):
        "Tests if nodes can be connected. Destructor not called actively. No error must be thrown."
        src = Source()
        filt = Filter()

        res = False
        try:
            src.connect_by_id(0, filt, 0)
            res = True
        except:
            res = False
        assert res

    def test_connect_by_id_disconnect(self):
        "Tests if nodes can be connected and disconnected."
        src = Source()
        filt = Filter()

        res = False
        try:
            src.connect_by_id(0, filt, 0)
            src.disconnect_by_id(0, filt, 0)
            res = True
        except:
            res = False
        assert res

    def test_connect_by_id_disconnect_connect(self):
        "Tests if nodes can be connected, disconnected and connected again."
        src = Source()
        filt = Filter()

        res = False
        try:
            src.connect_by_id(0, filt, 0)
            src.disconnect_by_id(0, filt, 0)
            src.connect_by_id(0, filt, 0)
            res = True
        except:
            res = False
        assert res

    def test_connect_by_id_duplicate_connections(self):
        "Connection attempts must fail if a node is already connected."
        src = Source()
        filt = Filter()

        res = False
        try:
            src.connect_by_id(0, filt, 0)
            src.connect_by_id(0, filt, 0)
            res = False
        except:
            res = True
        assert res

    def test_connect_by_id_invalid(self):
        "Invalid connection attempts must fail."
        src = Source()
        filt = Filter()

        def connect_by_id(outputPortId, node, inputPortId):
            res = False
            try:
                src.connect_by_id(outputPortId, node, inputPortId)
                res = False
            except:
                res = True
            return res

        assert connect_by_id(0, filt, 10)
        assert connect_by_id(10, filt, 0)
        assert connect_by_id(0, None, 0)

    def test_connect_by_id_split(self):
        "It must be possible to connect multiple inputs to an output."
        filt1 = Filter()
        filt2 = Filter()

        res = False
        try:
            filt1.connect_by_id(0, filt2, 0)
            filt1.connect_by_id(0, filt2, 1)
            res = True
        except:
            res = False
        assert res

    def test_connect_by_id_merge(self):
        "It must not be possible to connect multiple outputs to one input."
        filt1 = Filter()
        filt2 = Filter()

        res = False
        try:
            filt1.connect_by_id(0, filt2, 0)
            filt1.connect_by_id(1, filt2, 0)
            res = False
        except:
            res = True
        assert res

if __name__ == '__main__':
    try:
        filePath =  os.path.join(dir, os.path.basename(__file__).replace(".py", "") + ".txt") 
        with open(filePath, "w") as f:
            dual_stream = DualStream(f, sys.stdout)
            runner = unittest.TextTestRunner(stream=dual_stream, verbosity=2)
            unittest.main(testRunner=runner, exit=False)
    except SystemExit as e:
        pass