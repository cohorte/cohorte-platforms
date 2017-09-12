#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
Create COHORTE node (base) script.

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

import os
import sys
import common

# Documentation strings format
__docformat__ = "restructuredtext en"

# Boot module version
__version__ = "1.0.0"


def create_node(args):
    """
    Create node directory with necessary run script and configuration files
    """
    # create the node directory
    node_dir = args.node_name
    if not os.path.exists(node_dir):
        os.makedirs(node_dir)
    else:
        print("[ERROR] directory '" + node_dir + "' already exists!")
        print("        change the parent location or choose another node name.")
        sys.exit(1)

    os.makedirs(os.path.join(node_dir, 'repo'))
    os.makedirs(os.path.join(node_dir, 'conf'))
    # generate run script
    common.generate_run(args.node_name)

    # generate composition file
    if args.composition_name:
        common.generate_composition_conf(args.node_name, args.composition_name)

    # generate run configuration file
    CONFIG_FILE = os.path.join(node_dir, 'conf', 'run.js')
    configuration = {}
    COHORTE_HOME = os.environ.get('COHORTE_HOME')
    actual_dist = common.get_installed_dist_info(COHORTE_HOME)
    COHORTE_VERSION = actual_dist["version"]

    configuration["cohorte-version"] = COHORTE_VERSION
    if args.app_id:
        configuration["app-id"] = args.app_id
    configuration["node"] = {
        "name": args.node_name,
        "http-port": 0,
        "shell-port": 0,
        "top-composer": False,
        "console": True}

    if 'PYTHON_INTERPRETER' in os.environ:
        python_interpreter = os.environ['PYTHON_INTERPRETER']
        if python_interpreter:
            configuration["node"]["interpreter"] = python_interpreter

    configuration["transport"] = ['http']
    configuration["transport-http"] = {"http-ipv": 6}
    common.update_startup_file(CONFIG_FILE, configuration)


def main(args=None):
    """
    main script
    """
    import argparse
    if not args:
        args = sys.argv[1:]

    # Define arguments
    parser = argparse.ArgumentParser(description="Create COHORTE node (base)")

    # Node configuration
    group = parser.add_argument_group("Create node options")

    group.add_argument("-n", "--name", action="store",
                       dest="node_name", help="Name of the node")

    # Application configuration
    group.add_argument("-c", "--composition-name", action="store",
                       dest="composition_name",
                       help="application's composition name")

    group.add_argument("-a", "--app-id", action="store",
                       dest="app_id", help="application's ID")

    # Parse arguments
    args = parser.parse_args(args)

    if not os.environ.get('COHORTE_HOME'):
        print("[ERROR] environment variable COHORTE_HOME not set")
        return 1

    if not args.node_name:
        print("[ERROR] you should provide a node name (using --name option)")
        return -1
    # creates the node directory
    create_node(args)

if __name__ == "__main__":
    sys.exit(main())
