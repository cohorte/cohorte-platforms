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

# Standard Library
import os
import json
import shutil

WARNING_COMMENT = "/* WARNING!: do not edit, this file is generated " \
                  "automatically by COHORTE startup scripts. */"


def generate_run(node_dir):
    """
    Generates an executable 'run' file which launches cohorte node.
    """
    from stat import S_IRWXU
    file_name = os.path.join(node_dir, "run")
    with open(file_name, "w") as run:
        os.chmod(file_name, S_IRWXU)
        result = """#!/bin/bash
if test -z "$COHORTE_HOME"
then
  echo
  echo "[ERROR] the system environment variable COHORTE_HOME is not defined!"
  echo
  exit
fi

bash $COHORTE_HOME/bin/cohorte-start-node --base $(pwd) $*
"""
        run.write(result)


def generate_composition_conf(node_dir, app_name):
    """
    Generates conf/composition.js file.
    """
    file_name = os.path.join(node_dir, 'conf', "composition.js")
    app = app_name.rsplit(".", 2)[-1]
    with open(file_name, "w") as composition:
        result = """{{
    "name": "{app_name}",
    "root": {{
        "name": "{app}-composition",
        "components": [
            /* your component descriptions here */
        ]
    }}
}}
""".format(app_name=app_name, app=app)
        composition.write(result)

def generate_boot_common(node_dir, app_name):
    """
    Generates boot-common.js file which defines the application's id on which the node will be connected.
    """
    file_name = os.path.join(node_dir, 'conf', "boot-common.js")
    with open(file_name, "w") as boot_common:
        result = """{header}
{{
    "import-files" : [ "boot-common.js" ],
    "properties" : {{
        "herald.application.id" : "{app_name}"
    }}
}}
""".format(header=WARNING_COMMENT, app_name=app_name)
        boot_common.write(result)


def generate_boot_forker(node_dir, http_port, shell_port):
    """
    Generates conf/boot_forker.js file.
    """
    file_name = os.path.join(node_dir, 'conf', "boot-forker.js")
    with open(file_name, "w") as boot_forker:
        result = """{header}
{{
    "import-files" : [ "boot-forker.js" ],
    "composition" : [
    {{
        "name" : "pelix-http-service",
        "properties" : {{
            "pelix.http.port" : {http_port}
        }}
    }}, {{
        "name" : "pelix-remote-shell",
        "properties" : {{
            "pelix.shell.port" : {shell_port}
        }}
    }}
    ]
}}
""".format(header=WARNING_COMMENT, http_port=http_port, shell_port=shell_port)
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
        result = """{header}
{{
    "import-files" : [ "java-xmpp.js" ]
}}
""".format(header=WARNING_COMMENT)
        java_transport.write(result)

    file_name = os.path.join(herald_dir, 'python-transport.js')
    with open(file_name, "w") as python_transport:
        result = """{header}
{{
    "import-files" : [ "python-xmpp.js" ]
}}
""".format(header=WARNING_COMMENT)
        python_transport.write(result)

    file_name = os.path.join(herald_dir, 'all-xmpp.js')
    with open(file_name, "w") as all_xmpp:
        result = """{header}
{{
    "import-files" : [ "all-xmpp.js" ],
    "composition" : [
    {{
        "name" : "herald-xmpp-transport",
        "properties" : {{
            "xmpp.server" : "{server}",
            "xmpp.port" : "{port}",
            "xmpp.monitor.jid" : "{monitor_jid}",
            "xmpp.room.jid" : "{room_jid}",
            "xmpp.monitor.key" : "{key}"
        }}
    }}
    ]
}}
""".format(header=WARNING_COMMENT, server=server, port=port,
           monitor_jid=monitor_jid, room_jid=room_jid, key=key)
        all_xmpp.write(result)


def update_startup_file(config_file, configuration):
    """
    Updates the provided startup file
    """
    with open(config_file, 'w') as outfile:
        json.dump(configuration, outfile, sort_keys=False,
                  indent=4, separators=(',', ': '))


def generate_top_composer_config(node_dir, composition_file, autostart):
    """
    Generate Top Composer configuration file_name
    """
    tc_dir = os.path.join(node_dir, 'conf', 'composer')
    if not os.path.exists(tc_dir):
        os.makedirs(tc_dir)
    file_name = os.path.join(tc_dir, 'python-top.js')
    with open(file_name, "w") as top_composer:
        result = """{header}
{{
    "import-files" : [ "python-top.js" ],
    "composition" : [
    {{
        "factory" : "cohorte-composer-top-factory",
        "name" : "cohorte-composer-top",
        "properties" : {{
            "autostart" : "{autostart}",
            "composition.filename" : "{composition}"
        }}
    }}
    ]
}}
""".format(header=WARNING_COMMENT, autostart=autostart,
           composition=composition_file)
        top_composer.write(result)


def delete_top_composer_config(node_dir):
    """
    Delete Top Composer configuration
    """
    try:
        shutil.rmtree(os.path.join(node_dir, 'conf', 'composer'))
    except OSError:
        pass
