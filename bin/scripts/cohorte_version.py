#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
Shows installed Cohorte distribution's version.
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

import sys
import os

# cohorte scripts
import common

# Documentation strings format
__docformat__ = "restructuredtext en"

# module version
__version__ = "1.0.0"


def main(args=None):
    """
    main script
    """
    # Test if the COHORTE_HOME environment variable is set. If not exit
    COHORTE_HOME = os.environ.get('COHORTE_HOME')
    if not COHORTE_HOME:
        print("[ERROR] environment variable COHORTE_HOME not set")
        return 1
    # Show actual version
    actual = common.get_installed_dist_info(COHORTE_HOME)
    common.show_installed_dist_info(actual)
    return 0

if __name__ == "__main__":
    sys.exit(main())
