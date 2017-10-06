#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
python script that is used for initialization of component
e.g init data , init configuration file 

manage the generic parameter that can be handele for all isolate and node 
"""
import argparse;
import glob;
import json;
import logging
import shutil;
import sys;

import jsoncomment;


_logger = logging.getLogger(__name__)


def write_file(a_str, a_file_name):
    """
    read a json file comment and return a dictionnary 
    """
    # check if the str is still a correct commnted json 
    _logger.info("backup files {} to {}".format(a_file_name, a_file_name + ".origin"))
    shutil.copy(a_file_name, a_file_name + ".origin")

    with open(a_file_name, 'w') as obj_file:
        obj_file.write(a_str)
    _logger.info("write isolate configuration files {}".format(a_file_name))

    
def get_json_from_file(a_json_parser, a_file_name):
    """
    read a json file comment and return a dictionnary 
    """
    is_init_comment = False;
    start_read = True;
    with open(a_file_name, 'r') as obj_file:
        data = "".join(obj_file.readlines());
    return a_json_parser.loads(data)
    

def get_list_isolate():
    """
    allow to get the list of isolate name that is declare in the composition 
    return a list of string 
    """
    return glob.iglob("/opt/node/conf/isolate_*.js");

def main(args=None):
    if not args:
       args = sys.argv[1:]

    logging.basicConfig(level=logging.DEBUG)
    
    _logger.info("initialization script of container argument {0}".format(args))
   
        
    
    
    parser = argparse.ArgumentParser(description="init container 0 - javaagent")
    parser.add_argument("--jacoco", action="store_true", default=False,
                       dest="jacoco",
                       help="activate usage of jacoco agent");
    parser.add_argument("--jacocoagent", action="store", default=None,
                       dest="jacocoagent",
                       help="set jacoco agent property")
    
    args, boot_args = parser.parse_known_args(args)
    javaagent = None
    javaagent_format = "-javaagent:{pathjar}=output={output},address={address},port={port},includes={includes},classdumpdir={classdumpdir}"
    if args != None:
        if args.jacoco:
            javaagent = javaagent_format.format(pathjar="/opt/cohorte/extra/jacoco/jacocoagent.jar", output="tcpserver", address="*", port="6300", includes="com.cohorte.*:org.cohorte.*", classdumpdir="/opt/node/data/classdumpdir")
            _logger.info("-jacoco true is setted, construct automatic javaagent={}".format(javaagent))
        elif args.jacocoagent != None:
            # use 
            javaagent = "-javaagent:{pathjar}" + args.jacocoagent.format(pathjar="/opt/cohorte/extra/jacoco/jacocoagent.jar")
            _logger.info("-jacocoagent is setted , construct javaagent={}".format(javaagent))

        if javaagent is not None:
            w_parser = jsoncomment.JsonComment(json)
            _logger.info("read composition file in order to retreieve the isolate name and add vm_args if necessary")
            for isolate_name in get_list_isolate():
                
                
                w_isolate_json = get_json_from_file(w_parser, isolate_name)
                _logger.info("update isolate configuration files {}".format(isolate_name))

                if "vm_args" in w_isolate_json:
                    w_isolate_json["vm_args"].append(javaagent);
                else:
                     w_isolate_json["vm_args"] = [javaagent]
                # # add comment 
                w_str = '/*'\
                 ' Modify by init_container_0.py, add jacoco agent in vm_args '\
                 '*/';
                w_str = w_str + json.dumps(w_isolate_json, indent=4)
                write_file(w_str, isolate_name)
            
        else:
            print("do nothin, not relevant argument")
 
            # find in conf all isolat    
    else:
        print("do nothin, no argument received")
        
if __name__ == "__main__":
    sys.exit(main())
