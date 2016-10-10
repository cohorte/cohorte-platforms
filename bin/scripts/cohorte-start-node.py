#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
Script for starting COHORTE node.

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

from __future__ import print_function

# Standard Library
import argparse
import logging
import os
import sys
import shutil
import json
import subprocess
import platform

# cohorte scripts
import common

# Documentation strings format
__docformat__ = "restructuredtext en"

# Script module version
__version__ = "1.0.0"


def parse_config_file(config_file):
    """
    Parses the startup configuration file (run.js).
    """
    data = None
    if os.path.isfile(config_file):
        with open(config_file) as json_data:
            data = json.load(json_data)
    return data


def get_external_config(parsed_conf_file, conf_name):
    """
    Returns the value of the wanted startup configuration.
    """
    if parsed_conf_file is not None and conf_name is not None:
        if conf_name == "app-id":
            if "app-id" in parsed_conf_file:
                return parsed_conf_file["app-id"]
            elif "application-id" in parsed_conf_file:     # compatibility with cohorte 1.0.0
                return parsed_conf_file["application-id"]  #

        if conf_name == "node-name":
            if "node" in parsed_conf_file:
                # Different key name
                return parsed_conf_file["node"].get("name")
            # return parsed_conf_file["node"].get(conf_name)

        if conf_name in ("top-composer", "auto-start", "composition-file",
                         "http-port", "shell-port", "use-cache",
                         "recomposition-delay", "interpreter", "console",
                         "data-dir"):
            if "node" in parsed_conf_file:
                conf_value = parsed_conf_file["node"].get(conf_name)
                if conf_value is None:                                      #
                    if conf_name in "http-port":                            # compatibility with cohorte 1.0.0
                        return parsed_conf_file["node"].get("web-admin")    #
                    if conf_name in "shell-port":                           #
                        return parsed_conf_file["node"].get("shell-admin")  #
                else:
                    return conf_value

        if conf_name == "transport":
            if "transport" in parsed_conf_file:
                return parsed_conf_file["transport"]

        if conf_name.startswith("xmpp-"):
            if "transport-xmpp" in parsed_conf_file:
                return parsed_conf_file["transport-xmpp"].get(conf_name)

        if conf_name.startswith("http-"):
            if "transport-http" in parsed_conf_file:
                return parsed_conf_file["transport-http"].get(conf_name)

    return None


def set_configuration_value(argument_value, parsed_conf_value, default_value):
    """
    Returns the value to be affected to a configuration property.
    """
    if argument_value:
        return argument_value
    elif parsed_conf_value is not None:
        return parsed_conf_value
    else:
        return default_value


def main(args=None):
    """
    main script
    """
    if not args:
        args = sys.argv[1:]

    # Test if the COHORTE_HOME environment variable is set. If not exit
    COHORTE_HOME = os.environ.get('COHORTE_HOME')
    if not COHORTE_HOME:
        print("[ERROR] environment variable COHORTE_HOME not set")
        return 1

    # Define arguments
    parser = argparse.ArgumentParser(description="Starting a COHORTE Node")

    group = parser.add_argument_group("Mandatory arguments")

    group.add_argument("-a", "--app-id", action="store",
                       dest="app_id", help="Application's ID")

    group = parser.add_argument_group("Config",
                                      "Startup configuration options")

    group.add_argument("--use-config", action="store", default="conf/run.js",
                       dest="config_file",
                       help="Configuration file to use for starting cohorte "
                            "node. By default the conf/run.js file is used if "
                            "available")

    group.add_argument("--update-config", action="store_true", default=False,
                       dest="update_config_file",
                       help="Update startup configuration file with provided "
                       "options")

    group.add_argument("--show-config", action="store_true", default=False,
                       dest="show_config_file",
                       help="Show startup configuration file content")

    group.add_argument("-i", "--interpreter", action="store",
                       dest="interpreter",
                       help="Path to Python interpreter to use "
                            "(python2 or python3)")

    group.add_argument("-b", "--base", action="store", default=None,
                       dest="base_absolute_path",
                       help="absolute file path of the node's directory")

    group = parser.add_argument_group("Node",
                                      "Information about the node to start")

    group.add_argument("-n", "--node", action="store",
                       dest="node_name", help="Node name")

    group.add_argument("--data-dir", action="store",
                       dest="node_data_dir", help="Node Data Dir")

    group.add_argument("--top-composer", action="store",
                       dest="is_top_composer",
                       help="Flag indicating that this node is a Top Composer")

    group.add_argument("--composition-file", action="store",
                       dest="composition_file",
                       help="Composition file (by default 'composition.js'). "
                            "All composition files should be placed on 'conf' "
                            "directory")

    group.add_argument("--auto-start", action="store",
                       dest="auto_start",
                       help="Auto-start the composition if this node is a "
                            "Top Composer")

    group.add_argument("--http-port", action="store", type=int,
                       dest="http_port", help="Node HTTP port")

    group.add_argument("--shell-port", action="store", type=int,
                       dest="shell_port", help="Node Remote Shell port")

    group.add_argument("--use-cache", action="store", dest="use_cache",
                       help="Use cache to accelerate startup time "
                            "(experimental)")

    group.add_argument("--recomposition-delay", action="store", type=int,
                       dest="recomposition_delay",
                       help="Delay in seconds between two recomposition "
                            "tentatives")

    group = parser.add_argument_group(
        "Transport", "Information about the transport protocols to use")

    group.add_argument("--transport", action="store",
                       dest="transport_modes",
                       help="Transport mode (http and/or xmpp - "
                            "seperated by comma)")

    group.add_argument("--xmpp-server", action="store",
                       dest="xmpp_server", help="XMPP server")

    group.add_argument("--xmpp-port", action="store", type=int,
                       dest="xmpp_port", help="XMPP server port")

    group.add_argument("--xmpp-user-jid", action="store", dest="xmpp_jid",
                       help="XMPP User JID")

    group.add_argument("--xmpp-user-password", action="store",
                       dest="xmpp_password", help="XMPP User password")

    group.add_argument("--http-ipv", action="store", type=int, dest="http_ipv",
                       help="HTTP IP version to use (4 or 6)")

    parser.add_argument("--console", action="store",
                    dest="install_shell_console", 
                    help="If True, the shell console will be started")

    # Parse arguments
    args, boot_args = parser.parse_known_args(args)
    COHORTE_BASE = args.base_absolute_path
    NODE_NAME = "node"
    NODE_DATA_DIR = ""
    TRANSPORT_MODES = []
    HTTP_PORT = 0
    SHELL_PORT = 0
    IS_TOP_COMPOSER = None
    AUTO_START = None
    COMPOSITION_FILE = None
    APPLICATION_ID = None
    USE_CACHE = None
    RECOMPOSITION_DELAY = None
    INSTALL_SHELL_CONSOLE = False
    PYTHON_INTERPRETER = None
    XMPP_SERVER = None
    XMPP_PORT = None
    XMPP_JID = None
    XMPP_PASS = None
    HTTP_IPV = None

    # set working directory (cohorte-base)
    os.chdir(COHORTE_BASE)

    # startup config file
    config_file = args.config_file
    if not os.path.isfile(config_file):      # compatibility with cohorte 1.0.0
        config_file = "run.js"               #

    if args.show_config_file:
        # show the content of the startup configuration file and exit.
        content = parse_config_file(config_file)
        if content:
            content = json.dumps(content, sort_keys=False,
                                 indent=4, separators=(',', ': '))
            print(content)
        else:
            print("[INFO] there is no startup configuration file! "
                  "Use '--use-config' option to refer to your config file")
        return 0

    # Check if the user has provided the --base option (Node's full path)
    if not COHORTE_BASE:
        print("[ERROR] the absolute path to the node's directory to execute "
              "is required. Use --base option")
        return 1
    else:
        os.environ["COHORTE_BASE"] = COHORTE_BASE

    # export python path
    added_paths = [value
                   for value in (os.environ.get('PYTHONPATH'),
                                 os.path.join(args.base_absolute_path, 'repo'),
                                 os.path.join(COHORTE_HOME, 'repo'))
                   if value is not None]
    os.environ['PYTHONPATH'] = os.pathsep.join(added_paths)

    # Special case: IronPython path uses a different environment variable
    if sys.platform == 'cli':
        os.environ['IRONPYTHONPATH'] = os.environ['PYTHONPATH']

    # Change our path
    sys.path = added_paths + sys.path

    external_config = parse_config_file(config_file)

    # useing cache
    USE_CACHE = set_configuration_value(
            args.use_cache,
            get_external_config( external_config, "use-cache"), False)
    os.environ['COHORTE_USE_CACHE'] = str(USE_CACHE)

    # recomposition delay
    RECOMPOSITION_DELAY = set_configuration_value(
            args.recomposition_delay,
            get_external_config( external_config, "recomposition-delay"), 120)
    os.environ['cohorte.recomposition.delay'] = str(RECOMPOSITION_DELAY)

    # python interpreter
    PYTHON_INTERPRETER = set_configuration_value(
            args.interpreter,
            get_external_config( external_config, "interpreter"), "python")
    os.environ['PYTHON_INTERPRETER'] = str(PYTHON_INTERPRETER)
    # export Node name
    NODE_NAME = set_configuration_value(
        args.node_name, get_external_config(external_config, "node-name"),
        os.path.basename(os.path.normpath(COHORTE_BASE)))
    os.environ['COHORTE_NODE_NAME'] = NODE_NAME

    # export Cohorte Root
    os.environ['COHORTE_ROOT'] = os.environ.get('COHORTE_HOME')

    # Data dir
    NODE_DATA_DIR = set_configuration_value(
        args.node_data_dir,
        get_external_config(external_config, "data-dir"),
        os.path.join(COHORTE_BASE, "data"))

    # configure application id
    APPLICATION_ID = set_configuration_value(
        args.app_id,
        get_external_config(external_config, "app-id"), None)

    if not APPLICATION_ID and not args.update_config_file:
        print("[ERROR] no application ID is given!")
        print("        You should provide a correct application ID managed "
              "by a COHORTE Top Composer!")
        print("        use '--app-id' option to provide the application's ID "
              "or update your startup configuration file.")
        return 1

    # generate boot config file
    common.generate_boot_common(COHORTE_BASE, APPLICATION_ID, NODE_DATA_DIR)

    # Node log file
    LOG_DIR = os.path.join(COHORTE_BASE, 'var')
    os.environ['COHORTE_LOGFILE'] = os.path.join(LOG_DIR, 'forker.log')

    HTTP_PORT = set_configuration_value(
        args.http_port,
        get_external_config(external_config, "http-port"), 0)
    SHELL_PORT = set_configuration_value(
        args.shell_port,
        get_external_config(external_config, "shell-port"), 0)
    # Generate webadmin and shell configs of the cohorte (main) isolate
    # of this node
    common.generate_boot_forker(COHORTE_BASE, HTTP_PORT, SHELL_PORT)

    # Log
    try:
        shutil.rmtree(os.path.join(COHORTE_BASE, 'var'))
    except OSError:
        pass
    if not os.path.exists(os.path.join(COHORTE_BASE, 'var')):
        os.makedirs(os.path.join(COHORTE_BASE, 'var'))

    # Top Composer
    if args.is_top_composer:
        IS_TOP_COMPOSER = args.is_top_composer.lower() in ("true", "yes")
    else:
        IS_TOP_COMPOSER = set_configuration_value(
            None,
            get_external_config(external_config, "top-composer"), False)

    if IS_TOP_COMPOSER:
        boot_args.append("-t")
        # composition file
        COMPOSITION_FILE = set_configuration_value(
            args.composition_file,
            get_external_config(external_config, "composition-file"),
            "composition.js")

        # handle auto-start flag
        AUTO_START = set_configuration_value(
            args.auto_start,
            get_external_config( external_config, "auto-start"), True)

        common.generate_top_composer_config(COHORTE_BASE, COMPOSITION_FILE,
                                            AUTO_START)
    else:
        common.delete_top_composer_config(COHORTE_BASE)

    # show console (or not)    
    if args.install_shell_console:
        INSTALL_SHELL_CONSOLE = args.install_shell_console.lower() in ("true", "yes")
    else:
        INSTALL_SHELL_CONSOLE = set_configuration_value(
            None,
            get_external_config(external_config, "console"), True)

    if INSTALL_SHELL_CONSOLE == True:
        boot_args.append("--console")

    # transport mode
    tmodes = None
    if args.transport_modes:
        tmodes = str(args.transport_modes).split(',')
    if not tmodes:
        TRANSPORT_MODES = set_configuration_value(
            None, get_external_config(external_config, "transport"), [])
    else:
        TRANSPORT_MODES = set_configuration_value(
            tmodes, get_external_config(external_config, "transport"), [])

    if "http" in TRANSPORT_MODES:
        HTTP_IPV = set_configuration_value(
            args.http_ipv,
            get_external_config(external_config, "http-ipv"), 6)
        if HTTP_IPV == 4:
            common.generate_common_http(COHORTE_BASE)
        else:
            common.delete_common_http(COHORTE_BASE)

    if "xmpp" in TRANSPORT_MODES:
        XMPP_SERVER = set_configuration_value(
            args.xmpp_server,
            get_external_config(external_config, "xmpp-server"), "")
        XMPP_PORT = set_configuration_value(
            args.xmpp_port,
            get_external_config(external_config, "xmpp-port"), 5222)

        XMPP_JID = set_configuration_value(
            args.xmpp_jid,
            get_external_config(external_config, "xmpp-user-jid"), "")
        XMPP_PASS = set_configuration_value(
            args.xmpp_password,
            get_external_config(external_config, "xmpp-user-password"), "")

        if not args.update_config_file:
            print("[INFO] XMPP server configuration :")
            print("""
    - xmpp server: {server}
    - xmpp port: {port}
    - xmpp user jid: {jid}
    - xmpp user password: *
            """.format(server=XMPP_SERVER, port=XMPP_PORT, jid=XMPP_JID))

    
    # remove 'conf/herald' folder
    try:
        shutil.rmtree(os.path.join(COHORTE_BASE, 'conf', 'herald'))
    except OSError:
        pass
    
    # create conf/herald configs for node
    common.generate_herald_conf(COHORTE_BASE, TRANSPORT_MODES,
                                XMPP_SERVER, XMPP_PORT,
                                XMPP_JID, XMPP_PASS)
        # all-xmpp.js
        #
    #else:        

    # update configuration if not exists
    CONFIG_FILE = config_file
    if not os.path.exists(CONFIG_FILE) or args.update_config_file:
        configuration = {}
        actual_dist = common.get_installed_dist_info(COHORTE_HOME)
        COHORTE_VERSION = actual_dist["version"]
        configuration["cohorte-version"] = COHORTE_VERSION
        if APPLICATION_ID:
            configuration["app-id"] = APPLICATION_ID

        configuration["node"] = {
            "name": NODE_NAME,
            "top-composer": IS_TOP_COMPOSER,
            "http-port": HTTP_PORT,
            "shell-port": SHELL_PORT,
            "use-cache": USE_CACHE,
            "recomposition-delay": RECOMPOSITION_DELAY,
            "interpreter": PYTHON_INTERPRETER,
            "console": INSTALL_SHELL_CONSOLE,
            "data-dir": NODE_DATA_DIR}

        if IS_TOP_COMPOSER:
            configuration["node"]["auto-start"] = AUTO_START
            configuration["node"]["composition-file"] = COMPOSITION_FILE

        configuration["transport"] = TRANSPORT_MODES
        if "xmpp" in TRANSPORT_MODES:
            configuration["transport-xmpp"] = {
                "xmpp-server": XMPP_SERVER,
                "xmpp-port": XMPP_PORT,
                "xmpp-user-jid": XMPP_JID,
                "xmpp-user-password": XMPP_PASS
            }
        if "http" in TRANSPORT_MODES:
            configuration["transport-http"] = {"http-ipv": HTTP_IPV}

        common.update_startup_file(CONFIG_FILE, configuration)
        print("[INFO] config file '" + CONFIG_FILE + "' updated! ")
        if args.update_config_file:
            return 0
        
    # get python interpreter version (to be used by cohorte)
    output = subprocess.check_output([PYTHON_INTERPRETER , "-c", 
            'import sys; print("{0}.{1}.{2}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2]))'])
    PYTHON_VERSION = output.decode("utf-8").strip()
    # get cohorte_home version
    conf_dir = os.path.join(COHORTE_HOME, "conf")
    with open(os.path.join(conf_dir, "version.js")) as version_file:
        version = json.load(version_file)
    if not version:
        print("conf/version.js file not found! we cannot determine Cohorte distribution installed on your machine!")
        print("Please download a correct version of Cohorte distribution from http://cohorte.github.io")
        return 2
    COHORTE_VERSION = "{0}_{1}_{2}".format(version["version"], version["timestamp"], version["stage"])

    # show some useful information
    msg1 = """
   _____ ____  _    _  ____  _____ _______ ______
  / ____/ __ \| |  | |/ __ \|  __ \__   __|  ____|
 | |   | |  | | |__| | |  | | |__) | | |  | |__
 | |   | |  | |  __  | |  | |  _  /  | |  |  __|
 | |___| |__| | |  | | |__| | | \ \  | |  | |____
  \_____\____/|_|  |_|\____/|_|  \_\ |_|  |______|
    
     APPLICATION ID : {appid}
          NODE NAME : {node_name}
         TRANSPORTS : {transports}

       TOP COMPOSER : {is_top}

          HTTP PORT : {http_port}
         SHELL PORT : {shell_port}
""".format(appid=APPLICATION_ID, node_name=os.environ.get('COHORTE_NODE_NAME'),
           transports=",".join(TRANSPORT_MODES), is_top=IS_TOP_COMPOSER,
           http_port=HTTP_PORT, shell_port=SHELL_PORT)

    if IS_TOP_COMPOSER:
        msg1 += """
   COMPOSITION FILE : {composition}
         AUTO START : {auto_start}
""".format(composition=COMPOSITION_FILE, auto_start=AUTO_START)

    msg1 += """

    COHORTE VERSION : {cohorte_version}
       COHORTE HOME : {home}
       COHORTE BASE : {base}
       COHORTE DATA : {data}
 PYTHON INTERPRETER : {python} ({python_version})
           LOG FILE : {logfile}

""".format(home=COHORTE_HOME, base=os.environ['COHORTE_BASE'],
           data=NODE_DATA_DIR,
           logfile=os.environ.get('COHORTE_LOGFILE'),
           python=PYTHON_INTERPRETER, 
           python_version=PYTHON_VERSION, 
           cohorte_version=COHORTE_VERSION)

    print(msg1)

    # if java distribution => check python version > 3.4    

    if version["distribution"] not in ("cohorte-python-distribution"):
        # java distribution
        # => should have python 3.4                
        python_version_tuple = tuple(map(int, (PYTHON_VERSION.split("."))))
        if python_version_tuple < (3,4):
            print("You should have Python 3.4 to launch Java isolates!\n")
            print("If you need only Python isolates,")
            print("   please download cohorte-python-distribution which requires only Python 2.7.\n")
            print("It you have Python 3.4 installed on your machine and its Python 2.x which is used,")
            print("   use --interpreter <PATH_TO_PYTHON34> argument when starting your node.\n")
            return 3     
        elif python_version_tuple > (3,4):
            print("You should have Python 3.4 to launch Java isolates!\n")
            print("Your Python version is not yet supported!\n")   
        
        # change jpype implementation depending on platform system
        common.setup_jpype(COHORTE_HOME)        

    # write to log file
    with open(str(os.environ.get('COHORTE_LOGFILE')), "w") as log_file:
        log_file.write(msg1)

    # starting cohorte isolate
    result_code = 0
    # python_interpreter = prepare_interpreter()

    # Interpreter arguments
    interpreter_args = ['-m', 'cohorte.boot.boot']
    if sys.platform == 'cli':
        # Enable frames support in IronPython
        interpreter_args.insert(0, '-X:Frames')

    try:
        p = subprocess.Popen(
            [PYTHON_INTERPRETER] + interpreter_args + boot_args,
            stdin=None, stdout=None, stderr=None, shell=False)
    except Exception as ex:
        print("Error starting node:", ex)
        logging.exception("Error starting node: %s -- interpreter = %s",
                          ex, PYTHON_INTERPRETER)
        result_code = 1
    else:
        try:
            p.wait()
        except KeyboardInterrupt as ex1:
            print("Node stopped by user!")
            result_code = 0
        except Exception as ex:
            print("Error waiting for the node to stop:", ex)
            result_code = 1

        # stopping XMPP bot process
        if p:
            try:
                p.terminate()
            except OSError:
                pass

    return result_code

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    sys.exit(main())
