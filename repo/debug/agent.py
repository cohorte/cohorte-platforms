#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
COHORTE debug agent, to send debug info to Debug REST API.

:author: Bassem Debbabi
:license: Apache Software License 2.0

..

    Copyright 2015 isandlaTech

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# Documentation strings format
__docformat__ = "restructuredtext en"

# Boot module version
__version__ = "1.0.0"

# ------------------------------------------------------------------------------

# Cohorte
import cohorte

# Pelix framework
from pelix.ipopo.decorators import ComponentFactory, Provides, \
    Validate, Invalidate, Property, Requires
import pelix.constants
import pelix.framework
import pelix.http
import pelix.ipopo.constants
import pelix.shell
from pelix.shell.ipopo import ipopo_state_to_str

# Herald
import herald
import herald.beans as beans

# Python standard library
import logging
import sys
import threading
import traceback

# cohorte plutform debug agent and api
import debug

# ------------------------------------------------------------------------------

_logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------

_SUBJECT_PREFIX = "cohorte/debug/agent"
""" Common prefix to cohorte agent  """

_SUBJECT_MATCH_ALL = "{0}/*".format(_SUBJECT_PREFIX)
""" Filter to match agent signals """

SUBJECT_GET_INSTANCES = "{0}/get_instances".format(_SUBJECT_PREFIX)
""" Signal to request the instances of the isolate """

SUBJECT_GET_INSTANCE_DETAIL = "{0}/get_instance_detail".format(_SUBJECT_PREFIX)
""" Signal to request the detail of one instance """


@ComponentFactory('cohorte-debug-agent-factory')
@Requires("_ipopo", pelix.ipopo.constants.SERVICE_IPOPO)
@Requires('_herald', herald.SERVICE_HERALD)
@Provides([debug.SERVICE_DEBUG, herald.SERVICE_LISTENER])
@Property('_filters', herald.PROP_FILTERS, [_SUBJECT_MATCH_ALL])
@Property('_reject', pelix.remote.PROP_EXPORT_REJECT, [debug.SERVICE_DEBUG])
class DebugAgent(object):
    """
    COHORTE Debug Agent
    """
    def __init__(self):
        """
        Constructor
        """
        # Bundle context
        self._context = None
        # iPOPO
        self._ipopo = None
        # Herald
        self._herald = None
        # Herald filter property
        self._filters = None

    def get_instances(self):
        ipopo_instances = self._ipopo.get_instances()
        return [
            {"instance-name" : name, 
             "instance-factory": factory, 
             "instance-state": ipopo_state_to_str(state)}
            for name, factory, state in ipopo_instances]

    def get_instance_detail(self, instance_name):
        details = None
        try:
            details = self._ipopo.get_instance_details(instance_name)
        except ValueError as ex:
            return "No value!"
        # basic info
        if details is not None:
            instance_detail = { "name": details["name"],
                                "factory": details["factory"],
                                "bundle-id": details["bundle_id"],
                                "state": ipopo_state_to_str(details["state"]),
                                "services": [ str(svc_ref) for svc_ref in details["services"].values() ],
                                "dependencies": [ {dep : { "specification": details["dependencies"][dep]["specification"],                                                            
                                                           "optional": details["dependencies"][dep]["optional"],
                                                           "aggregate": details["dependencies"][dep]["aggregate"],
                                                           "handler": details["dependencies"][dep]["handler"],
                                                           "filter": "not showed here!",
                                                           "bindings": [ str(binding) for binding in details["dependencies"][dep]["bindings"] ]
                                                         } 
                                                  } for dep in details["dependencies"] 
                                                ],
                                "properties" : details["properties"],
                                "error-trace" : details["error_trace"]
                              }
            # instance properties
            return instance_detail
        else:
            return "No value!"

    def herald_message(self, herald_svc, message):
        """
        Called by Herald when a message is received
        """
        subject = message.subject
        reply = None

        if subject == SUBJECT_GET_INSTANCES:
            reply = self.get_instances()        
        elif subject == SUBJECT_GET_INSTANCE_DETAIL:
            instance_name = message.content
            reply = self.get_instance_detail(instance_name)            
        if reply is not None:
            herald_svc.reply(message, reply)
        else:
            herald_svc.reply(message, "No value!")

    @Validate
    def validate(self, context):
        """
        Component validated

        :param context: The bundle context
        """
        # Store the framework access
        self._context = context
        _logger.info("Debug agent Ready")

    @Invalidate
    def invalidate(self, context):
        """
        Component invalidated

        :param context: The bundle context
        """
        # Clear the framework access
        self._context = None
        _logger.info("Debug agent Gone")
