#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
Update cohorte distribution from Internet.
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
 
# Documentation strings format
__docformat__ = "restructuredtext en"
 
# module version
__version__ = "1.0.0"
 
import sys
import os
import urllib2
import urllib
import json
import tarfile
import shutil
import argparse

# cohorte scripts
import common 

# actions to do
UPGRADE = 1
UPDATE  = 2
UPDATE_EXPERIMENTAL = 3
UPTODATE = 4 

# download and archive folders
DOWNLOAD_FOLDER = ".download"
ARCHIVE_FOLDER = ".archive"

UPDATE_RELEASE_URL = "http://cohorte.github.io/latests/distributions_release.json"
UPDATE_DEV_URL = "http://cohorte.github.io/latests/distributions_dev.json"

def get_latest_dist_info(dist):
    print("[INFO] getting latest " + dist + " info (from internet)...")    
    url = UPDATE_DEV_URL
    response = urllib.urlopen(url)
    data = json.loads(response.read())    
    latest_dev = {}
    latest_dev["distribution"] = dist
    latest_dev["version"] = data[dist]["version"]
    latest_dev["stage"] = data[dist]["stage"]
    latest_dev["timestamp"] = data[dist]["timestamp"]
    latest_dev["changelog"] = data[dist]["changelog"]
    latest_dev["file"] = data[dist]["files"]["tar.gz"]
    
    url = UPDATE_RELEASE_URL
    response = urllib.urlopen(url)
    data = json.loads(response.read())    
    latest_release = {}
    latest_release["distribution"] = dist
    latest_release["version"] = data[dist]["version"]
    latest_release["stage"] = data[dist]["stage"]
    latest_release["timestamp"] = data[dist]["timestamp"]
    latest_release["changelog"] = data[dist]["changelog"]
    latest_release["file"] = data[dist]["files"]["tar.gz"]
    
    return latest_dev, latest_release
     
def analyse_versions(installed, latest_dev, latest_release):
    installed_version = installed["version"]
    latest_dev_version = latest_dev["version"]
    latest_release_version = latest_release["version"]
    installed_timestamp = installed["timestamp"]
    latest_dev_timestamp = latest_dev["timestamp"]
    latest_release_timestamp = latest_release["timestamp"]
    installed_stage = installed["stage"]
    if installed_stage == "dev":
        installed_stage = "dev    "
    show = """
    +-----------+-----------------+-----------------+-----------------+
    |           | ACTUAL          | LATEST DEV      | LATEST RELEASE  |
    +-----------+-----------------+-----------------+-----------------+
    | version   | {act_v}           | {dev_v}           | {rel_v}           |
    +-----------+-----------------+-----------------+-----------------+    
    | stage     | {act_s}         | dev             | release         |    
    +-----------+-----------------+-----------------+-----------------+    
    | timestamp | {act_t} | {dev_t} | {rel_t} |
    +-----------+-----------------+-----------------+-----------------+
""".format(act_v=installed_version, dev_v=latest_dev_version,rel_v=latest_release_version,
            act_t=installed_timestamp, dev_t=latest_dev_timestamp,rel_t=latest_release_timestamp,
            act_s=installed_stage)

    print(show)
    
    tmp = installed_version.split(".")    
    inst_v = (int(tmp[0]) * 1000000) + (int(tmp[1]) * 1000) + int(tmp[2])
    tmp = latest_dev_version.split(".")
    ldev_v = (int(tmp[0]) * 1000000) + (int(tmp[1]) * 1000) + int(tmp[2])
    tmp = latest_release_version.split(".")
    lrel_v = (int(tmp[0]) * 1000000) + (int(tmp[1]) * 1000) + int(tmp[2])

    inst_s = 1 if installed["stage"] == "dev" else 10
    ldev_s = 1
    lrel_s = 10
    
    inst_t = int(installed_timestamp.replace("-", ""))
    ldev_t = int(latest_dev_timestamp.replace("-", ""))
    lrel_t = int(latest_release_timestamp.replace("-", ""))
    
    if inst_v < lrel_v:        
        return UPGRADE
    elif inst_v == lrel_v:
        if inst_s < lrel_s:
            return UPGRADE
        else:
            return UPTODATE
    elif inst_v > lrel_v:
        if inst_v < ldev_v:
            if inst_s == 10:
                return UPDATE_EXPERIMENTAL
            else:
                return UPDATE
        elif inst_v == ldev_v:
            if inst_t >= ldev_t:
                return UPTODATE
            elif inst_t < ldev_t:
                if inst_s == 10:
                    return UPDATE_EXPERIMENTAL
                else:
                    return UPDATE
        elif inst_v > ldev_v:
            return UPTODATE
                
def upgrade(dist):    
    return update(dist)

def update(dist):        
    attemps = 0
    while attemps < 3:
        choice = user_choise()
        if choice.lower() == "yes":            
            new_dist_file = download_distribution(dist)
            archive_actual_dist()
            remove_actual_dist()            
            install_new_dist(new_dist_file, dist)
            break
        elif choice.lower() == "no":
            break
        elif choice.lower() == "log":
            #print("Showing changelog is not yet implemented!")
            show_log(dist)
            attemps = 0
        else:
            print("We didn't understand your choice!")
            attemps += 1        
    print("")
    print("Bye!")
    print("")
    return 0

def show_log(dist):
    print("----------------------------------------------------------------------------")
    print("")
    changelog_file_url = dist["changelog"] 
    if changelog_file_url is not None:        
        log = ""
        for line in urllib2.urlopen(changelog_file_url):
            log += line
        print(log)
    print("")
    print("----------------------------------------------------------------------------")

def update_experimental(dist):
    return update(dist)

def uptodate():
    print("[INFO] Your distribution is up-to-date.")
    print("")
    print("Bye!")
    print("")
    return 0

def user_choise():    
    attemps = 0
    while attemps < 3:        
        choice = raw_input("     | Would you like to install it (yes/no)? or show its changelog (log)? ")
        if choice.lower() == "yes":
            return "yes"
        elif choice.lower() == "no":
            return "no"
        elif choice.lower() == "log":
            return "log"
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
 
    temp_path = os.path.join(cohorte_dir, DOWNLOAD_FOLDER)
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path);
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
 
def download_distribution(dist):
    print("")
    print("[INFO] downloading " + dist["distribution"] + "-" + dist["version"] + "-" + dist["timestamp"] 
          + " (" + dist["stage"] + ") ...")
    download_chunks(dist["file"])
    filename = dist["file"].split('/')[-1].split('#')[0].split('?')[0]    
    return filename
 
def exclude_archive_function(filename):
    if DOWNLOAD_FOLDER in filename:
        return True
    if ARCHIVE_FOLDER in filename:
        return True
    if '.git' in filename:
        return True
    if '.project' in filename:
        return True
    return False
 
 
def archive_actual_dist():
    print("")
    print("[INFO] archiving actual distribution ...")
    cohorte_dir = os.environ.get('COHORTE_HOME')
    archive_dir = os.path.join(cohorte_dir, ARCHIVE_FOLDER)
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
            if ARCHIVE_FOLDER not in root and DOWNLOAD_FOLDER not in root:
                os.remove(os.path.join(root, name))
            else:
                #print(root)
                pass
        for name in dirs:
            if name not in (ARCHIVE_FOLDER, DOWNLOAD_FOLDER):
                os.rmdir(os.path.join(root, name))
    print("     | Done.")
 
 
def install_new_dist(new_dist_file, update):    
    print("")
    print("[INFO] installing new distribution " + update["distribution"] + "-" + update["version"]
          + "-" + update["timestamp"] + " (" + update["stage"] + ") ...")
    cohorte_dir = os.environ.get('COHORTE_HOME')
    tmp_dir = os.path.join(cohorte_dir, DOWNLOAD_FOLDER)
    if not os.path.exists(tmp_dir):
        print("non existing .download directory!")
    else:
        new_dist = os.path.join(tmp_dir, new_dist_file)
        with tarfile.open(new_dist, "r:gz") as tar:
            tar.extractall('.')
        for x in os.listdir(cohorte_dir):
            if x.startswith('cohorte'):
                for f in os.listdir(os.path.join(cohorte_dir, x)):
                    shutil.move(os.path.join(cohorte_dir, x, f), os.path.join(cohorte_dir, f))
                os.rmdir(os.path.join(cohorte_dir, x))
                break                                 
    print("     | Done.")

def install_archived_dist():    
    print("")
    print("[INFO] installing archived distribution ...")
    cohorte_dir = os.environ.get('COHORTE_HOME')
    tmp_dir = os.path.join(cohorte_dir, ARCHIVE_FOLDER)
    if not os.path.exists(tmp_dir):
        print("non existing .archive directory!")
    else:
        new_dist = os.path.join(tmp_dir, "archived_distribution.tar.gz")
        with tarfile.open(new_dist, "r:gz") as tar:
            tar.extractall('.')
        for x in os.listdir(cohorte_dir):
            if x.startswith('cohorte'):
                for f in os.listdir(os.path.join(cohorte_dir, x)):
                    shutil.move(os.path.join(cohorte_dir, x, f), os.path.join(cohorte_dir, f))
                os.rmdir(os.path.join(cohorte_dir, x))
                break                                 
    print("     | Done.") 

def roll_back():
    print("")
    print("[INFO] Rolling back to previous installed distribution...")
    cohorte_dir = os.environ.get('COHORTE_HOME')
    tmp_dir = os.path.join(cohorte_dir, ARCHIVE_FOLDER, "archived_distribution.tar.gz")
    if not os.path.exists(tmp_dir):
        print("     | non existing archive copy!")
        print("")
        return 1
    remove_actual_dist()
    install_archived_dist()
    return 0
 
def main(args=None):
    """
    main script
    """    
    
    # Test if the COHORTE_HOME environment variable is set. If not exit
    COHORTE_HOME = os.environ.get('COHORTE_HOME')
    if not COHORTE_HOME:
        print("[ERROR] environment variable COHORTE_HOME not set")
        return 1
    
    if not args:
        args = sys.argv[1:]
 
    # Define arguments
    parser = argparse.ArgumentParser(description="Create COHORTE node (base)")
 
    group = parser.add_argument_group("Create node options")
 
    group.add_argument("-r", "--roll-back", action="store_true",
                       dest="roll_back", help="Rollback the last update/upgrade")

 
    # Parse arguments
    args = parser.parse_args(args)
    if args.roll_back:
        return roll_back()
    
    # get installed version    
    installed = {}
    installed = common.get_installed_dist_info(COHORTE_HOME)    
    common.show_installed_dist_info(installed)
        
    # get latest versions 
    latest_dev = {}
    latest_release = {}
    latest_dev, latest_release = get_latest_dist_info(installed["distribution"]) 
    
    # compare actual version with latest 
    result = analyse_versions(installed, latest_dev, latest_release)
    if result == UPGRADE:
        print("[INFO] There is a new 'release' version!")
        return upgrade(latest_release)
    elif result == UPDATE:
        print("[INFO] There is a new 'development' version!")
        return update(latest_dev)
    elif result == UPDATE_EXPERIMENTAL:
        print("[INFO] There is a new 'development/experimental' version!")
        return update_experimental(latest_dev)
    elif result == UPTODATE:
        return uptodate()
        
    return 0
 
if __name__ == "__main__":
    sys.exit(main())