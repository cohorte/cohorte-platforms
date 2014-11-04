#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
Startup scripts common file.

:author: Bassem Debbabi
:license: Apache Software License 2.0

..

    Copyright 2014 isandlaTech

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


import os

def generate_run(node_dir): 
    """
    Generates an executable 'run' file which launches cohorte node.
    """
    from stat import S_IRWXU
    file_name = os.path.join(node_dir, "run")
    with open(file_name, "w") as run:
        os.chmod(file_name, stat.S_IRWXU)
        result = '#!/bin/bash \n' \
            'if test -z "$COHORTE_HOME"\n' \
            'then\n' \
            '  echo \n' \
            '  echo "[ERROR] the system environment variable COHORTE_HOME is not defined!"\n' \
            '  echo \n' \
            '  exit \n' \
            'fi \n' \
            ' \n' \
            'bash $COHORTE_HOME/bin/cohorte-start-node --base $(pwd) $* \n' \
            ' \n'
        run.write(result)

def generate_autorun_conf(node_dir, app_name):
    """
    Generates conf/autorun_conf.js file.
    """
    file_name = os.path.join(node_dir, 'conf', "autorun_conf.js")
    with open(file_name, "w") as autorun_conf:    
        result = '{ \n' \
            '  "name": "' + app_name + '",\n' \
            '  "root": {\n' \
            '    "name": "' + app_name + '-composition",\n' \
            '    "components": [\n' \
            '      /* your component descriptions here */\n' \
            '    ]\n' \
            '  }\n' \
            '}' 
        autorun_conf.write(result)  
    
def generate_boot_common(node_dir, app_name):
    """
    Generates boot-common.js file which defines the application's id on which the node will be connected. 
    """
    file_name = os.path.join(node_dir, 'conf', "boot-common.js")
    with open(file_name, "w") as boot_common:     
        result = '/* WARNING!: do not edit, this file is generated automatically by COHORTE startup scripts. */ \n' \
            '{ \n' \
            '  "import-files" : [ "boot-common.js" ], \n' \
            '  "properties" : { \n' \
            '    "herald.application.id" : "'+app_name+'"\n' \
            '  }\n' \
            '}'     
        boot_common.write(result)

def generate_boot_forker(node_dir, http_port, shell_port):
    """
    Generates conf/boot_forker.js file.
    """
    file_name = os.path.join(node_dir, 'conf', "boot-forker.js")
    with open(file_name, "w") as boot_forker:
        result = '/* WARNING!: do not edit, this file is generated automatically by COHORTE startup scripts. */ \n' \
            '{ \n' \
            '  "import-files" : [ "boot-forker.js" ], \n' \
            '  "composition" : [ \n' \
            '   {\n' \
            '       "name" : "pelix-http-service",\n' \
            '       "properties" : {\n' \
            '           "pelix.http.port" : '+str(http_port)+'\n' \
            '       }\n' \
            '   }, {\n' \
            '       "name" : "pelix-remote-shell",\n' \
            '       "properties" : {\n' \
            '           "pelix.shell.port" : '+str(shell_port)+'\n' \
            '       }\n' \
            '   }\n' \
            '  ]\n' \
            '}'     
        boot_forker.write(result)

def generate_herald_xmpp_conf(node_dir, server, port, monitor_jid, room_jid, key):
    """
    Generates Herald XMPP transport configuration
    """    
    herald_dir = os.path.join(node_dir, 'conf', 'herald')
    if not os.path.exists(herald_dir):
        os.makedirs(herald_dir)
    file_name = os.path.join(herald_dir, 'java-transport.js')
    with open(file_name, "w") as java_transport:     
        result = '/* WARNING!: do not edit, this file is generated automatically by COHORTE startup scripts. */ \n' \
            '{\n' \
            '    "import-files" : [ "java-xmpp.js" ]\n' \
            '} \n'             
        java_transport.write(result)
    file_name = os.path.join(herald_dir, 'python-transport.js')
    with open(file_name, "w") as java_transport:     
        result = '/* WARNING!: do not edit, this file is generated automatically by COHORTE startup scripts. */ \n' \
            '{\n' \
            '    "import-files" : [ "python-xmpp.js" ]\n' \
            '} \n'             
        java_transport.write(result)
    file_name = os.path.join(herald_dir, 'java-transport.js')
    with open(file_name, "w") as python_transport:     
        result = '/* WARNING!: do not edit, this file is generated automatically by COHORTE startup scripts. */ \n' \
            '{\n' \
            '    "import-files" : [ "java-xmpp.js" ]\n' \
            '} \n'             
        python_transport.write(result)
    file_name = os.path.join(herald_dir, 'all-xmpp.js')
    with open(file_name, "w") as all_xmpp:
        result = '/* WARNING!: do not edit, this file is generated automatically by COHORTE startup scripts. */ \n' \
            '{ \n' \
            '  "import-files" : [ "all-xmpp.js" ], \n' \
            '  "composition" : [ \n' \
            '   {\n' \
            '       "name" : "herald-xmpp-transport",\n' \
            '       "properties" : {\n' \
            '           "xmpp.server" : "'+server+'",\n' \
            '           "xmpp.port" : "'+str(port)+'",\n' \
            '           "xmpp.monitor.jid" : "'+monitor_jid+'",\n' \
            '           "xmpp.room.jid" : "'+room_jid+'",\n' \
            '           "xmpp.monitor.key" : "'+key+'"\n' \
            '       }\n' \
            '   }\n' \
            '  ]\n' \
            '}'     
        all_xmpp.write(result)
