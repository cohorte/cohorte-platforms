#!/usr/bin/python3
# -- Content-Encoding: UTF-8 --
"""
Small script which is able to look for and install packages targeting another
platform, using pip.

This simplifies the creation of distribution files for different platform.

Only works for Python 3.4 downloads.

:author: Thomas Calmant
:copyright: Copyright 2014, isandlaTech
:license: Apache License 2.0
:version: 0.0.1
:status: Alpha

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

# Module version
__version_info__ = (0, 0, 1)
__version__ = ".".join(str(x) for x in __version_info__)

# Documentation strings format
__docformat__ = "restructuredtext en"

import argparse
import os

import pip
import pip.index
import pip.pep425tags
import pip.req


# Environment variable to fake distutils get_platform() result
ENV_PIP_PLATFORM = "_PYTHON_HOST_PLATFORM"

# Result of distutils.util.get_platform() for each platform
PIP_PLATFORMS = {
    "darwin": "macosx-10.9-intel",
    "linux-x86_64": "linux-x86_64",
    "linux-x86": "linux-x86",
    "windows-x86": "win32",
    "windows-x86_64": "win-amd64",
}


# Faked platform -> tag
PEP425_TAGS = {
    # Mac OS X tags
    "darwin": [
        ('cp34', 'cp34m', 'macosx_10_6_intel'),
        ('cp34', 'abi3', 'macosx_10_6_intel'),
        ('cp34', 'none', 'macosx_10_6_intel')],
    # Linux tags
    "linux-x86_64": [
        ('cp34', 'cp34m', 'linux_x86_64'),
        ('cp34', 'abi3', 'linux_x86_64'),
        ('cp34', 'none', 'linux_x86_64')],
    # TODO: verify Linux x86 tags (copied from x86_64 ones)
    "linux-x86": [
        ('cp34', 'cp34m', 'linux_x86'),
        ('cp34', 'abi3', 'linux_x86'),
        ('cp34', 'none', 'linux_x86')],
    # Windows tags
    "windows-x86": [
        ('cp34', 'none', 'win32')],
    "windows-x86_64": [
        ('cp34', 'none', 'win_amd64')],
}


def fake_platform(platform):
    """
    Replaces the supported tags in the pip wheel handling package, and forges
    the result of distutils.util.get_platform()

    :param platform: Platform to fake
    """
    # Fake the tags
    others = [tag for tag in pip.pep425tags.supported_tags if tag[2] == 'any']
    natives = PEP425_TAGS[platform]
    pip.pep425tags.supported_tags = natives + others

    # Update the cross-platform environment variable
    os.environ[ENV_PIP_PLATFORM] = PIP_PLATFORMS[platform]


def get_file_url(index_url, package, platform):
    """
    Returns the URL to download the package file

    :param package: Name of the package
    :param platform: Target operating system (see PEP425_TAGS)
    :return: The URL of the file to download
    """
    # Fake the platform
    if platform:
        fake_platform(platform)

    # Prepare the requirement
    req = pip.req.InstallRequirement.from_line(package)

    # Use pip to find the URL
    finder = pip.index.PackageFinder(
        find_links=[],
        index_urls=[index_url],
        use_wheel=True,
        allow_all_prereleases=True,
        process_dependency_links=True)

    url = finder.find_requirement(req, True)
    return url.url


def install_package(url):
    """
    Installs the package
    """
    command = pip.commands['install']()
    command.main([url])


def main(argv=None):
    """
    Script entry point
    """
    # Parse arguments
    parser = argparse.ArgumentParser(description="Package download utility")
    parser.add_argument("--index", metavar="URL", dest="index_url",
                        default="http://forge.cohorte.tech:7080/devpi/jenkins/cohorte/+simple/",
                        help="The PyPI index URL to use")
    parser.add_argument("--package", metavar="NAME", dest="package",
                        required=True, help="Name of the package to install")
    parser.add_argument("--platform", metavar="PLATFORM", dest="platform",
                        choices=PEP425_TAGS.keys(),
                        help="Target platform, one of: {0}"
                        .format(", ".join(sorted(PEP425_TAGS))))
    parser.add_argument("--install", action="store_true", dest="install",
                        help="Installs the package if set, else prints the "
                             "download URL")
    args = parser.parse_args(argv)

    # Get file URL
    url = get_file_url(args.index_url, args.package, args.platform)
    if not args.install:
        # Print the URL only
        print(url)
    else:
        # Install the package
        install_package(url)


if __name__ == '__main__':
    main()