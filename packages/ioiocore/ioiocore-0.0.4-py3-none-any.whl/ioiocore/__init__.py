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
#utilities
from .templates.utilities.constants import NodeInfo, PortInfo
from .templates.utilities.frequency_generator import FrequencyGenerator

#common
from .templates.common.node import Node
from .templates.common.timeseries_node import TimeseriesNode

#source
from .templates.sources.manual_source import ManualSource
from .templates.sources.device_source import DeviceSource
from .templates.sources.timeseries_source import TimeseriesSource

#filter

#sink
from .templates.common.pipeline import Pipeline
