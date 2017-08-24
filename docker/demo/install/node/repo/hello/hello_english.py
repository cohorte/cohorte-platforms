#!/usr/bin/python
#-- Content-Encoding: UTF-8 --
"""
Component A.

:author: Bassem Debbabi
:copyright: Copyright 2013, isandlaTech
:license:  Apache Software License 2.0
"""

from pelix.ipopo.decorators import ComponentFactory, Provides

@ComponentFactory("hello_english_factory")
@Provides("java:/cohorte.demos.hello.HelloService")
class HelloEnglish(object):

    def say_hello(self):
        return "Hi, I am a Python component!"

    def get_name(self):
    	return "EN"