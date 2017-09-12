#!/usr/bin/python
#-- Content-Encoding: UTF-8 --
"""
Component C.

:author: Bassem Debbabi
:copyright: Copyright 2013, isandlaTech
:license:  Apache Software License 2.0
"""

from pelix.ipopo.decorators import ComponentFactory, Provides

@ComponentFactory("hello_spanish_factory")
@Provides("java:/cohorte.demos.hello.HelloService")
class HelloSpanish(object):

    def say_hello(self):
        return "Hola, soy un componente Python!"

    def get_name(self):
        return "ES"