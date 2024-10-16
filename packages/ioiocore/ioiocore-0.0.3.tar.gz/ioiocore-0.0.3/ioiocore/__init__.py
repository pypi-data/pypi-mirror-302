# -*- coding: utf-8 -*-
"""
ioiocore
-------

A realtime processing framework for python

:copyright: (c) 2024 g.tec medical engineering GmbH

"""

# compatibility
from __future__ import absolute_import, division, print_function

# get version
from .__version__ import __version__

# allow lazy loading
#pattern
from .pattern.constants import NodeInfo, PortInfo
from .pattern.node import Node
from .pattern.sources import ManualSource, FixedFrequencySource, DeviceSource, FrequencyGenerator
from .pattern.pipeline import Pipeline
