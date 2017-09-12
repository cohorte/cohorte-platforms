#!/usr/bin/python
#-- Content-Encoding: UTF-8 --
"""
Component E.

:author: Bassem Debbabi
:copyright: Copyright 2013, isandlaTech
:license:  Apache Software License 2.0
"""

# iPOPO decorators
from pelix.ipopo.decorators import ComponentFactory, Provides

# Standard library
import logging

_logger = logging.getLogger(__name__)

@ComponentFactory("hello_ghost_factory")
@Provides("java:/cohorte.demos.hello.HelloService")
class HelloGhost(object):

    def say_hello(self):
        """
        Simple way to crash: free(-1)
        """
        _logger.critical("CRASHING...")
        import ctypes
        # which OS
        import platform
        os_system = platform.system()
        if os_system == "Darwin":
            ctypes.CDLL("libc.dylib").free(-1)
        elif os_system == "Linux":
            ctypes.CDLL("libc.so.6").free(-1)
        elif os_system == "Windows":
            #ctypes.CDLL("libc.so.6").free(-1)
            _logger.critical("No problem for Windows OS ;) ")            

        _logger.critical("!!! AFTERMATH !!!")
        return "I'm a Ghost Component!"

    def get_name(self):
        return "GHOST"