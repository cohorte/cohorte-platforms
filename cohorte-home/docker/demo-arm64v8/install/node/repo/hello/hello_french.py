#!/usr/bin/python
#-- Content-Encoding: UTF-8 --
"""
Component B.

:author: Bassem Debbabi
:copyright: Copyright 2013, isandlaTech
:license:  Apache Software License 2.0
"""

from pelix.ipopo.decorators import ComponentFactory, Provides

@ComponentFactory("hello_french_factory")
@Provides("java:/cohorte.demos.hello.HelloService")
class HelloFrench(object):

    def say_hello(self):
        return "Bonjour, je suis un composant Python!"

    def get_name(self):
        return "FR"