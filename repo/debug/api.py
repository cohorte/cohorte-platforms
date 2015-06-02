#!/usr/bin/python
# -- Content-Encoding: UTF-8 --
"""
Cohorte Debug REST API

:authors: Bassem Debbabi
:copyright: Copyright 2015, isandlaTech
:license:  Apache Software License 2.0
"""

# iPOPO decorators
from pelix.ipopo.decorators import ComponentFactory, Provides, Property, Instantiate, \
    Validate, Invalidate, Requires, RequiresMap, Bind, BindField, UnbindField
import pelix.remote

# Herald
import herald
import herald.beans as beans

# Cohorte 
import cohorte.composer
import cohorte.monitor

# Standard library
import logging
import threading
import json, time, os

try:
    # Python 3
    import urllib.parse as urlparse

except ImportError:
    # Python 2
    import urlparse

# cohorte plutform debug agent and api
import debug

_logger = logging.getLogger("debug.debug")

# collecting information 
SUBJECT_GET_HTTP = "cohorte/shell/agent/get_http"

# API path
DEBUG_REST_API_PATH = "debug/api/v1"

# API Version
DEBUG_REST_API_VERSION = "v1"

# VERSION
COHORTE_VERSION = "1.0.1.dev"


@ComponentFactory("cohorte-debug-api-factory")
@Provides(['pelix.http.servlet'])
@Property('_path', 'pelix.http.path', "/debug")\

@Requires("_agent", debug.SERVICE_DEBUG)
# Consume a single Herald Directory service
@Requires("_directory", herald.SERVICE_DIRECTORY)
@Requires('_herald', herald.SERVICE_HERALD)
# Consume an Isolate Composer service
@RequiresMap("_icomposers", cohorte.composer.SERVICE_COMPOSER_ISOLATE, 'endpoint.framework.uuid',
             optional=True, allow_none=False)
@Requires("_icomposerlocal", cohorte.composer.SERVICE_COMPOSER_ISOLATE,
          optional=True, spec_filter="(!(service.imported=*))")
@Requires("_isolates", cohorte.composer.SERVICE_COMPOSER_ISOLATE, aggregate=True, optional=True)
@Property('_reject', pelix.remote.PROP_EXPORT_REJECT, ['pelix.http.servlet', herald.SERVICE_DIRECTORY_LISTENER])
@Instantiate('cohorte-debug-api')
class DebugAPI(object):
    """
    A Component that provides the REST Admin API
    """

    def __init__(self):

        # lock
        self._lock = threading.Lock()

        # servlet's path
        self._path = None

        # cohorte platform debug agent
        self._agent = None

        # herald directory service
        self._directory = None
        self._herald = None
        # isolate composer service
        self._icomposers = {}
        self._icomposerlocal = None
        self._isolates = []

        # List of platform activities
        self._platform_activities = []
        self._platform_activities_index = 0

        # a Map of last updated lists
        self._last_updates = {}
        time_now = time.time()
        self._last_updates["nodes"] = time_now
        self._last_updates["platform_activities"] = time_now

    def decrypt_request(self, request, action="GET"):
        """
        Decrypts the request and extracts these information:

        :return path: full path without host:port (first and last / are removed)
        :return parts: list of query parts
        :return in_data: json object of the associated request data
        """
        o = urlparse.urlparse(request.get_path())
        path = o.path
        query = o.query

        # prepare query path: remove first and last '/' if exists
        if path[0] == '/':
            path = path[1:]
        if path[-1] == '/':
            path = path[:-1]
        parts = str(path).split('/')
        in_data = None
        if action == "GET":
            in_data = urlparse.parse_qs(query, keep_blank_values=True)
        else:
            data = request.read_data()
            if data != None:
                in_data = json.loads(str(data))
            else:
                in_data = urlparse.parse_qs(query, keep_blank_values=True)

        #print(json.dumps(in_data, sort_keys=False, indent=4, separators=(',', ': ')))
        return (path, parts, in_data)

    def prepare_response(self, request, action):
        data = {"meta": {}}
        data["meta"]["status"] = 200
        data["meta"]["msg"] = "OK"
        data["meta"]["api-version"] = DEBUG_REST_API_VERSION
        data["meta"]["api-method"] = ""
        data["meta"]["cohorte-version"] = COHORTE_VERSION
        data["meta"]["request-path"] = request.get_path()
        data["meta"]["request-method"] = action
        data["meta"]["duration"] = 0.0
        return data

    def send_json(self, data, response):
        result = json.dumps(data, sort_keys=False,
                            indent=4, separators=(',', ': '))
        response.send_content(data["meta"]["status"], result, "application/json")
    	
    def send_text(self, data, response, status):
        response.send_content(status, data, "text/plain")
        
    def bad_request(self, request, response, in_data, out_data):
        out_data["meta"]["status"] = 400
        out_data["meta"]["msg"] = "BAD REQUEST"

    """
    GET actions ========================================================================
    """

    def get_api_info(self, request, response, in_data, out_data):
        out_data["api"] = {"name": "debug"} 

    def get_isolates(self, request, response, in_data, out_data):
        out_data["isolates"] = []
        lp = self._directory.get_local_peer()
        out_data["isolates"].append({"uid": lp.uid, "name": lp.name,
                                     "node_uid": lp.node_uid, "node_name": lp.node_name})
        count = 1
        for p in self._directory.get_peers():
            out_data["isolates"].append({"uid": p.uid, "name": p.name,
                                         "node_uid": p.node_uid, "node_name": p.node_name})
            count += 1         
        out_data["meta"]["count"] = count

    def get_isolate(self, request, response, in_data, out_data, uuid):
        out_data["isolate"] = self._get_isolate_detail(uuid)
        
    def get_isolate_bundles(self, request, response, in_data, out_data, uuid):
        out_data["isolate"] = {"uuid" : uuid}
        bundles = self._get_isolate_bundles(uuid)
        out_data["bundles"] = bundles
        if bundles is not None:
            count = len(bundles)
        else:
            count = 0        
        out_data["meta"]["count"] = count
    
    def get_bundle_detail(self, request, response, in_data, out_data, isolate_uuid, bundle_id):
        out_data["isolate"] = {"uuid" : isolate_uuid}
        out_data["bundle"] = {}
        out_data["bundle"] = self._get_bundle_detail(isolate_uuid, bundle_id)   
            
    def get_isolate_factories(self, request, response, in_data, out_data, uuid):
        out_data["isolate"] = {"uuid" : uuid}
        factories = self._get_isolate_factories(uuid)
        out_data["factories"] = factories
        if factories is not None:
            count = len(factories)
        else:
            count = 0        
        out_data["meta"]["count"] = count

    def get_factory_detail(self, request, response, in_data, out_data, isolate_uuid, factory_name):
        out_data["isolate"] = {"uuid" : isolate_uuid}
        out_data["factory"] = {}
        out_data["factory"] = self._get_factory_detail(isolate_uuid, factory_name) 

    def get_isolate_instances(self, request, response, in_data, out_data, uuid):
        out_data["isolate"] = {"uuid" : uuid}                
        instances = self._get_isolate_instances(uuid)
        out_data["instances"] = instances        
        if instances is not None:
            count = len(instances)
        else:
            count = 0
        out_data["meta"]["count"] = count
    
    def get_instance_detail(self, request, response, in_data, out_data, isolate_uuid, instance_name):
        out_data["isolate"] = {"uuid" : isolate_uuid}
        out_data["instance"] = {}
        out_data["instance"] = self._get_instance_detail(isolate_uuid, instance_name)         
        
    def get_isolate_services(self, request, response, in_data, out_data, uuid):
        out_data["isolate"] = {"uuid" : uuid}
        services = self._get_isolate_services(uuid)
        out_data["services"] = services
        if services is not None:
            count = len(services)
        else:
            count = 0
        out_data["meta"]["count"] = count

    def get_isolate_threads(self, request, response, in_data, out_data, uuid):
        out_data["isolate"] = {"uuid" : uuid}
        threads = self._get_isolate_threads(uuid)
        out_data["threads"] = threads
        if threads is not None:
            count = len(threads)
        else:    
            count = 0        
        out_data["meta"]["count"] = count
        
    def get_isolate_logs(self, request, response, in_data, out_data, uuid):
        out_data["isolate"] = {"uuid" : uuid}
        logs = self._get_isolate_logs(uuid)
        out_data["logs"] = logs
        if logs is not None:
            count = len(logs)
        else:
            count = 0        
        out_data["meta"]["count"] = count

    def get_isolate_log(self, request, response, in_data, out_data, isolate_uuid, log_id):
        out_data["isolate"] = {"uuid" : isolate_uuid}        
        out_data["log"] = self._get_isolate_log(isolate_uuid, log_id)        
        
    """
    Internal agent methods ===========================================================================
    """

    def _get_isolate_detail(self, uuid):
        lp = self._directory.get_local_peer()
        if lp.uid != uuid:  
            # this is another isolate   
            try:       
                msg = beans.Message(debug.agent.SUBJECT_GET_ISOLATE_DETAIL)
                reply = self._herald.send(uuid, msg)
                return reply.content
            except KeyError:
                return None
        else:
            # this is the local isolate
            return self._agent.get_isolate_detail()

    def _get_isolate_bundles(self, uuid):
        lp = self._directory.get_local_peer()
        if lp.uid != uuid:  
            # this is another isolate          
            msg = beans.Message(debug.agent.SUBJECT_GET_BUNDLES)
            reply = self._herald.send(uuid, msg)
            return reply.content
        else:
            # this is the local isolate
            return self._agent.get_bundles()
    
    def _get_bundle_detail(self, uuid, bundle_id):
        lp = self._directory.get_local_peer()
        if lp.uid != uuid:  
            # this is another isolate          
            msg = beans.Message(debug.agent.SUBJECT_GET_BUNDLE_DETAIL, bundle_id)
            reply = self._herald.send(uuid, msg)
            return reply.content
        else:
            # this is the local isolate
            return self._agent.get_bundle_detail(bundle_id)
                
    def _get_isolate_factories(self, uuid):
        lp = self._directory.get_local_peer()
        if lp.uid != uuid:  
            # this is another isolate          
            msg = beans.Message(debug.agent.SUBJECT_GET_FACTORIES)
            reply = self._herald.send(uuid, msg)
            return reply.content
        else:
            # this is the local isolate
            return self._agent.get_factories()

    def _get_factory_detail(self, uuid, factory_name):
        lp = self._directory.get_local_peer()
        if lp.uid != uuid:  
            # this is another isolate          
            msg = beans.Message(debug.agent.SUBJECT_GET_FACTORY_DETAIL, factory_name)
            reply = self._herald.send(uuid, msg)
            return reply.content
        else:
            # this is the local isolate
            return self._agent.get_factory_detail(factory_name)
            
    def _get_isolate_instances(self, uuid):
        lp = self._directory.get_local_peer()
        if lp.uid != uuid:  
            # this is another isolate          
            msg = beans.Message(debug.agent.SUBJECT_GET_INSTANCES)
            reply = self._herald.send(uuid, msg)
            return reply.content
        else:
            # this is the local isolate
            return self._agent.get_instances()

    def _get_instance_detail(self, uuid, instance_name):
        lp = self._directory.get_local_peer()
        if lp.uid != uuid:  
            # this is another isolate          
            msg = beans.Message(debug.agent.SUBJECT_GET_INSTANCE_DETAIL, instance_name)
            reply = self._herald.send(uuid, msg)
            return reply.content
        else:
            # this is the local isolate
            return self._agent.get_instance_detail(instance_name)

    def _get_isolate_services(self, uuid):
        lp = self._directory.get_local_peer()
        if lp.uid != uuid:  
            # this is another isolate          
            msg = beans.Message(debug.agent.SUBJECT_GET_SERVICES)
            reply = self._herald.send(uuid, msg)
            return reply.content
        else:
            # this is the local isolate
            return self._agent.get_services()

    def _get_isolate_threads(self, uuid):
        lp = self._directory.get_local_peer()
        if lp.uid != uuid:  
            # this is another isolate          
            msg = beans.Message(debug.agent.SUBJECT_GET_THREADS)
            reply = self._herald.send(uuid, msg)
            return reply.content
        else:
            # this is the local isolate
            return self._agent.get_threads()
    	
    def _get_isolate_logs(self, uuid):
        lp = self._directory.get_local_peer()
        if lp.uid != uuid:  
            # this is another isolate          
            msg = beans.Message(debug.agent.SUBJECT_GET_ISOLATE_LOGS)
            reply = self._herald.send(uuid, msg)
            return reply.content
        else:
            # this is the local isolate
            return self._agent.get_isolate_logs()
            
    def _get_isolate_log(self, uuid, log_id):
        lp = self._directory.get_local_peer()
        if lp.uid != uuid:  
            # this is another isolate          
            msg = beans.Message(debug.agent.SUBJECT_GET_ISOLATE_LOG, log_id)
            reply = self._herald.send(uuid, msg)
            return reply.content
        else:
            # this is the local isolate
            return self._agent.get_isolate_log(log_id)    
        
    """
    Servlet (url mapping to rest api) ================================================================
    """

    def do_GET(self, request, response):
        """
        Handle a GET
        """
        path, parts, in_data = self.decrypt_request(request)

        out_data = self.prepare_response(request, "GET")

        if path.startswith(DEBUG_REST_API_PATH):
            if path == DEBUG_REST_API_PATH:
                out_data["meta"]["api-method"] = "get_api_info"
                self.get_api_info(request, response, in_data, out_data)
            elif path == DEBUG_REST_API_PATH + "/isolates":
                out_data["meta"]["api-method"] = "get_isolates"
                self.get_isolates(request, response, in_data, out_data)
            
            elif len(parts) == 5:    
                if path == DEBUG_REST_API_PATH + "/isolates/" + parts[4]:
                    out_data["meta"]["api-method"] = "get_isolate"
                    self.get_isolate(request, response, in_data, out_data, parts[4])
                else:
                    self.bad_request(request, response, in_data, out_data)
            
            elif len(parts) == 6:
                if path == DEBUG_REST_API_PATH + "/isolates/" + parts[4] + "/bundles":
                    out_data["meta"]["api-method"] = "get_isolate_bundles"
                    self.get_isolate_bundles(request, response, in_data, out_data, parts[4])
                
                elif path == DEBUG_REST_API_PATH + "/isolates/" + parts[4] + "/factories":
                    out_data["meta"]["api-method"] = "get_isolate_factories"
                    self.get_isolate_factories(request, response, in_data, out_data, parts[4])
                            
                elif path == DEBUG_REST_API_PATH + "/isolates/" + parts[4] + "/instances":
                    out_data["meta"]["api-method"] = "get_isolate_instances"
                    self.get_isolate_instances(request, response, in_data, out_data, parts[4])
                        
                elif path == DEBUG_REST_API_PATH + "/isolates/" + parts[4] + "/services":
                    out_data["meta"]["api-method"] = "get_isolate_services"
                    self.get_isolate_services(request, response, in_data, out_data, parts[4])
                
                elif path == DEBUG_REST_API_PATH + "/isolates/" + parts[4] + "/threads":
                    out_data["meta"]["api-method"] = "get_isolate_threads"
                    self.get_isolate_threads(request, response, in_data, out_data, parts[4])
                elif path == DEBUG_REST_API_PATH + "/isolates/" + parts[4] + "/logs":
                    out_data["meta"]["api-method"] = "get_isolate_logs"
                    self.get_isolate_logs(request, response, in_data, out_data, parts[4])
            
            elif len(parts) == 7:
                if path == DEBUG_REST_API_PATH + "/isolates/" + parts[4] + "/bundles/" + parts[6]:
                    out_data["meta"]["api-method"] = "get_bundle_detail"
                    self.get_bundle_detail(request, response, in_data, out_data, parts[4], parts[6])
                elif path == DEBUG_REST_API_PATH + "/isolates/" + parts[4] + "/factories/" + parts[6]:
                    out_data["meta"]["api-method"] = "get_factory_detail"
                    self.get_factory_detail(request, response, in_data, out_data, parts[4], parts[6])
                elif path == DEBUG_REST_API_PATH + "/isolates/" + parts[4] + "/instances/" + parts[6]:
                    out_data["meta"]["api-method"] = "get_instance_detail"
                    self.get_instance_detail(request, response, in_data, out_data, parts[4], parts[6])
                elif path == DEBUG_REST_API_PATH + "/isolates/" + parts[4] + "/logs/" + parts[6]:
                    if 'raw' in in_data:
                        # send raw log
                        log = self._get_isolate_log(parts[4], parts[6])
                        self.send_text(log, response, 200)
                    else:
                        # send log within a json object data["log"]
                        out_data["meta"]["api-method"] = "get_isolate_log"
                        self.get_isolate_log(request, response, in_data, out_data, parts[4], parts[6])
            else:
                self.bad_request(request, response, in_data, out_data)

        else:
            self.bad_request(request, response, in_data, out_data)

        self.send_json(out_data, response)


    """
	iPOPO STUFF --------------------------------------------------------------------------------------------------------
	"""

    @Validate
    def validate(self, context):
        _logger.info("Debug REST API validated")
        self._context = context


    @Invalidate
    def invalidate(self, context):
        _logger.info("Debug REST API invalidated")


    def bound_to(self, path, params):
        """
		Servlet bound to a path
		"""
        _logger.info('Bound to ' + path)
        return True

    def unbound_from(self, path, params):
        """
		Servlet unbound from a path
		"""
        _logger.info('Unbound from ' + path)
        return None