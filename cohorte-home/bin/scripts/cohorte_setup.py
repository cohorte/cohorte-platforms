#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
Install the good version of JPype
:author: Bassem Debbabi
:license: Apache Software License 2.0
..
    Copyright 2015-2016 Cohorte Technologies (ex. ISANDLATECH)
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

# cohorte scripts
import common

# Documentation strings format
__docformat__ = "restructuredtext en"

# module version
__version__ = "1.0.0"


def main(argv):
    """
    main script
    """
    # Test if COHORTE_HOME is given as parameter, otherelse, get it from OS 
    if len(argv) > 0:        
        COHORTE_HOME = argv[0]
    else:        
        COHORTE_HOME = os.environ.get('COHORTE_HOME')
    # Test if the COHORTE_HOME is set. If not exit
    if not COHORTE_HOME:
        print("[ERROR] environment variable COHORTE_HOME not set")
        return 1
    # install   
    common.setup_jpype(COHORTE_HOME)    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
