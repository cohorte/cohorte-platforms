#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
Startup scripts common file.

:author: Bassem Debbabi
:license: Apache Software License 2.0

:hostory:
    MOD_BD_20170306: enhance setup_jpype to support win32 bits
    MOD_BD_20161010: adding setup_jpype function

..

    Copyright 2014-2006 Cohorte-Technologies (e.x. isandlaTech)

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

# Standard Library
import json
import os
import platform
import shutil
from stat import S_IROTH  # Read by others
from stat import S_IRWXG  # Read, write, and execute by group
from stat import S_IRWXU  # Read, write, and execute by owner


# Documentation strings format
__docformat__ = "restructuredtext en"

# Boot module version
__version__ = "1.0.0"

WARNING_COMMENT = "/* WARNING!: do not edit, this file is generated " \
                  "automatically by COHORTE startup scripts. */"


def generate_run(node_dir):
    """
    Generates an executable 'run' file which launches cohorte node.
    """
    # generate posix run executable
    result = """#!/bin/bash
if test -z "$COHORTE_HOME"
then
  echo
  echo "[ERROR] the system environment variable COHORTE_HOME is not defined!"
  echo
  exit
fi
if test -z "$COHORTE_BASE"
then
  COHORTE_BASE=$(pwd)
fi
bash "$COHORTE_HOME/bin/cohorte-start-node" --base "$COHORTE_BASE" $*
"""

    file_name = os.path.join(node_dir, "run")
    with open(file_name, "w") as run:
        os.chmod(file_name, S_IRWXU | S_IRWXG | S_IROTH)
        run.write(result)

    # generate windows run executable
    result = """@echo off

if "%COHORTE_HOME%" == "" (
  echo [ERROR] the system environment variable COHORTE_HOME is not defined!
  exit /b 1
)

call %COHORTE_HOME%\\bin\cohorte-start-node.bat --base %CD% %*
"""

    file_name2 = os.path.join(node_dir, "run.bat")
    with open(file_name2, "w") as run_bat:
        run_bat.write(result)


def generate_composition_conf(node_dir, app_name):
    """
    Generates conf/composition.js file.
    """
    conf_dir = os.path.join(node_dir, 'conf')
    if not os.path.exists(conf_dir):
        os.makedirs(conf_dir)
    file_name = os.path.join(conf_dir, "composition.js")
    app = app_name.rsplit(".", 2)[-1]

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

    with open(file_name, "w") as composition:
        composition.write(result)


def update_startup_file(config_file, configuration):
    """
    Updates the provided startup file
    """
    with open(config_file, 'w') as outfile:
        json.dump(configuration, outfile, sort_keys=False,
                  indent=4, separators=(',', ': '))



def parse_version_file(version_file):
    """
    Parses the version file (conf/version.js).
    """
    data = None
    if os.path.isfile(version_file):
        with open(version_file) as json_data:
            data = json.load(json_data)
    return data


def get_installed_dist_info(cohorte_home):
    """
    Gets the installed distribution's version information.
    """
    actual = parse_version_file(
        os.path.join(cohorte_home, "conf", "version.js"))
    return actual


def show_installed_dist_info(dist):
    """
    Shows the installed distribution's version information.
    """
    msg = """\n'\
    '-----------------[ Installed COHORTE distribution ]--------------------\n
    '    - distribution : {0}
    '    - version      : {1}
    '    - stage        : {2}
    '    - timestamp    : {3}
    '    - git branch   : {4}
    '    - git commit   : {5}
    '    - location     : {6}\n
    '-----------------------------------------------------------------------\n"""
    distribution = dist["distribution"] if "distribution" in dist else "None"
    version = dist["version"] if "version" in dist else "None"
    stage = dist["stage"] if "stage" in dist else "None"
    timestamp = dist["timestamp"] if "timestamp" in dist else "None"
    git_branch = dist["git_branch"] if "git_branch" in dist else "None"
    git_commit = dist["git_commit"] if "git_commit" in dist else "None"
    COHORTE_HOME = dist["COHORTE_HOME"] if "COHORTE_HOME" in dist else "None"

    print(msg.format(distribution, version, stage, timestamp, git_branch, git_commit, COHORTE_HOME))
    
def setup_jpype(cohorte_home):
    platform_name = platform.system()
    # possible values: 'Linux', 'Windows', or 'Darwin'        
    repo_dir = os.path.join(cohorte_home, "repo")
    if platform_name == 'Darwin':
        jpype_file_name = "_jpype.so"                    
    elif platform_name == 'Windows':
        jpype_file_name = "_jpype.pyd"
    elif platform_name == 'Linux':
        jpype_file_name = "_jpype.cpython-34m.so"
    
    jpype_file = os.path.join(repo_dir, jpype_file_name)
    if not os.path.exists(jpype_file):        
        repo_dir = os.path.join(cohorte_home, 'repo')
        extra_dir = os.path.join(cohorte_home, 'extra')
        try:
            # remove existing jpype
            jpype_dir = os.path.join(repo_dir, 'jpype')
            if os.path.exists(jpype_dir):
                shutil.rmtree(jpype_dir)
            jpypex_dir = os.path.join(repo_dir, 'jpypex')
            if os.path.exists(jpypex_dir):
                shutil.rmtree(jpypex_dir)    
            for fname in os.listdir(repo_dir):
                if fname.startswith("_jpype"):
                    os.remove(os.path.join(repo_dir, fname))
            # install adequate jpype                
            shutil.copytree(os.path.join(extra_dir, "jpype"),
                        os.path.join(repo_dir, "jpype"))
            shutil.copytree(os.path.join(extra_dir, "jpypex"),
                        os.path.join(repo_dir, "jpypex"))
            # MOD_BD_20170306 support win 32 bits
            if "32bit" in platform.architecture():
                source_jpype_file = os.path.join(extra_dir, str(platform_name).lower(), "32", jpype_file_name)
            else:
                source_jpype_file = os.path.join(extra_dir, str(platform_name).lower(), jpype_file_name)
            
            shutil.copyfile(source_jpype_file, os.path.join(repo_dir, jpype_file_name))        
            

        except OSError:
            pass
