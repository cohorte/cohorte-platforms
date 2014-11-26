#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
Update cohorte home from Internet.

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
 
import sys
import os
import urllib2
import urllib
import json
import tarfile
 
def get_actual_dist():
    actual = {}
    actual["distribution"] = "cohorte-linux-distribution"
    actual["version"] = "1.0.0-20141210.221211"
    actual["branch"] = "dev"
    actual["changelog"] = "http://cohorte.github.io/changlogs/cohorte-distribution.1.0.0-SNAPSHOT.txt"
    actual["url"] = "http://repo.isandlatech.com/maven/org/cohorte/platforms/file.tar.gz"
    return actual
 
def show_actual_dist(dist):
    print("")
    print("---------[ Installed COHORTE distribution ]---------")
    print("")
    print("    - distribution : " + dist["distribution"])
    print("    - version      : " + dist["version"])
    print("    - branch       : " + dist["branch"])
    print("")
    print("----------------------------------------------------")
    print("")
 
def check_for_update():
    print("[INFO] checking for updates...")
    print("")
    url = "http://cohorte.github.io/latest_platforms.json"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    #print data
    update = {}
    update["distribution"] = "cohorte-linux-distribution"
    update["version"] = "1.0.0-20141212.000003"
    update["branch"] = "dev"
    update["changelog"] = "http://cohorte.github.io/changlogs/cohorte-distribution.1.0.0-SNAPSHOT.txt"
    update["url"] = "http://repo.isandlatech.com/maven/org/cohorte/platforms/file.tar.gz"
    return update
 
def user_choise(update):
    print("     | There is a new '"+update["branch"]+"' version ("+update["version"]+").")
    attemps = 0
    while attemps < 3:
        choice = raw_input("     | Would you like to install it (yes/no)? or show its changelog (log)? ")
        if choice.lower() == "yes":
            return "yes"
        elif choice.lower() == "no":
            return "no"
        elif choice.lower() == "log":
            print("CHANGELOG:")
            attemps = 0
        else:
            print("We didn't understand your choice!")
            attemps += 1
    if attemps == 3:
        return "non"
    return "yes"
 
def download_chunks(url):
    baseFile = os.path.basename(url)
    cohorte_dir = os.environ.get('COHORTE_HOME')
    #move the file to a more uniq path
    os.umask(0002)
 
    temp_path = os.path.join(cohorte_dir, "__tmp")
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    try:
        dfile = os.path.join(temp_path, baseFile)
        req = urllib2.urlopen(url)
        total_size = int(req.info().getheader('Content-Length').strip())
        print("     | total file size to download ~ " + str(total_size/1000000) + "Mb")
        downloaded = 0
        chunk = 0
        CHUNK = 256 * 10240
        with open(dfile, 'wb') as fp:
 
            while True:
                percent = float((downloaded * 100) / total_size) / 100
                bar_length = 15
                hashes = '#' * int(round(percent * bar_length))
                spaces = ' ' * (bar_length - len(hashes))
                sys.stdout.write("\r     | Progress: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
                sys.stdout.flush()
                # download chunk
                chunk = req.read(CHUNK)
                downloaded += len(chunk)
                if not chunk:
                    break
                fp.write(chunk)
    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, url
        return False
    sys.stdout.flush()
    print("")
    print("     | Done.")
 
def download_distribution(update):
    print("")
    print("[INFO] downloading " + update["distribution"] + "-" + update["version"]
          + " (" + update["branch"] + ") ...")
    download_chunks("http://repo.isandlatech.com/maven/snapshots/org/cohorte/platforms/cohorte/1.0.0-SNAPSHOT/cohorte-1.0.0-20141121.152538-145-linux-distribution.tar.gz")
    return "cohorte-1.0.0-20141121.152538-145-linux-distribution.tar.gz"
 
def exclude_archive_function(filename):
    if '__tmp' in filename:
        return True
    if '__archive' in filename:
        return True
    if '.git' in filename:
        return True
    return False
 
 
def archive_actual_dist(actual):
    print("")
    print("[INFO] archiving actual distribution ...")
    cohorte_dir = os.environ.get('COHORTE_HOME')
    archive_dir = os.path.join(cohorte_dir, "__archive")
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    output_filename = os.path.join(archive_dir, "archived_distribution.tar.gz")
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(cohorte_dir, arcname="cohorte", exclude=exclude_archive_function)
    print("     | Done.")
    print("     | you can rollback using --roll-back option.")
 
 
def remove_actual_dist():
    print("")
    print("[INFO] deleting actual distribution ...")
    cohorte_dir = os.environ.get('COHORTE_HOME')
    for root, dirs, files in os.walk(cohorte_dir, topdown=False):
        for name in files:
            if '__archive' not in root and '__tmp' not in root:
                os.remove(os.path.join(root, name))
            else:
                print(root)
        for name in dirs:
            if name not in ("__archive", "__tmp"):
                os.rmdir(os.path.join(root, name))
    print("     | Done.")
 
 
def install_new_dist(new_dist_file, update):
    print("")
    print("[INFO] installing new distribution " + update["distribution"] + "-" + update["version"]
          + " (" + update["branch"] + ") ...")
    cohorte_dir = os.environ.get('COHORTE_HOME')
    tmp_dir = os.path.join(cohorte_dir, "__tmp")
    if not os.path.exists(tmp_dir):
        print("non existing archive directory!")
    else:
        new_dist = os.path.join(tmp_dir, new_dist_file)
        with tarfile.open(new_dist, "w:gz") as tar:
            tar.extractall()
    print("     | Done.")
 
 
def main(args=None):
    """
    main script
    """
    import argparse
    if not args:
        args = sys.argv[1:]
 
    # Define arguments
    parser = argparse.ArgumentParser(description="Create COHORTE node (base)")
 
    group = parser.add_argument_group("Create node options")
 
    group.add_argument("-f", "--force", action="store_true",
                       dest="force_update", help="Force the update")
 
    group.add_argument("-v", "--verbose", action="store_true",                       
                       dest="verbose_mode", help="Verbose mode")
 
    group.add_argument("-c", "--changelog", action="store_true",
                       dest="show_changelog", help="Show changelog of actual version and exit")
 
 
    # Parse arguments
    args = parser.parse_args(args)
 
    # Show actual version
    actual = get_actual_dist()
    show_actual_dist(actual)
 
    # Check for updates
    update = {}
    update = check_for_update()
 
    # ask the user to choose whether he/she wants to install or not the update
    if update:
        choice = user_choise(update)
 
        # analyse user choice and proceed to update
        if choice.lower() == "yes":
            new_dist_file = download_distribution(update)
            archive_actual_dist(actual)
            remove_actual_dist()
            install_new_dist(new_dist_file, update)
        else:
            print("Bye!")
            return 2
    else:
        print("Your distribution is up-to-date.")
        print("")
 
if __name__ == "__main__":
    sys.exit(main())