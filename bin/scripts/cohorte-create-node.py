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

# Documentation strings format
__docformat__ = "restructuredtext en"

# Boot module version
__version__ = "1.0.0"


import os
import sys
import common


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
    # generate configuration files
    common.generate_composition_conf(args.node_name, args.app_name)

    #configuration = {}
    #if args.app_name:
    #    configuration["application-id"] = args.app_name
    #configuration["node"] = {}
    #if args.node_name:
    #    configuration["node"]["name"] = args.node_name
    #common.update_startup_file(os.path.join(args.node_name, 'run.js'),
    #    configuration)
    #common.generate_boot_common(args.node_name, args.app_name)


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

    group.add_argument("-n", "--node", action="store",
                       dest="node_name", help="Name of the node")

    # Application configuration
    group.add_argument("-a", "--app-name", action="store",
                       default="symbolic-application-name",
                       dest="app_name", help="application's symbolic name")

    # Parse arguments
    args = parser.parse_args(args)

    if not args.node_name:
        print("[ERROR] you should provide a node name (using --node option)")
        return -1
    # creates the node directory from the template zip file
    create_node(args)

if __name__ == "__main__":
    sys.exit(main())
