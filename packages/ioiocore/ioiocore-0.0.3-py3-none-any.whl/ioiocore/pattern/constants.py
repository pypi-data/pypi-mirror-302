from enum import Enum

class NodeInfo(str,Enum):
    NODE = 'node',
    INPUTS = 'inputs',
    OUTPUTS = 'outputs',

class PortInfo(str,Enum):
    NAME = 'name',
    TYPE = 'datatype',
    ID = 'id',