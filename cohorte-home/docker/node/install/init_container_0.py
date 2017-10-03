#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
python script that is used for initialization of component
e.g init data , init configuration file 

manage the generic parameter that can be handele for all isolate and node 
"""
import argparse;
import json;
import sys;

import jsoncomment;


def main(args=None):
    if not args:
       args = sys.argv[1:]
    print("initialization script of container argument {0}".format(args))
    parser = argparse.ArgumentParser(description="init container 0 - javaagent")
    group.add_argument("--jacoco", action="store_true", default=False,
                       dest="jacoco",
                       help="activate usage of jacoco agent");
    group.add_argument("--jacocoagent", action="store", default="",
                       dest="jacocoagent",
                       help="set jacoco agent property")
    
    args, boot_args = parser.parse_known_args(args)
    
    javaagent = "-javaagent:{pathjar}=output={output},address={address≠},port={port},includes={includes}"
    if args != None:
        if args.jacoco:
            javaagent = javaagent.format(pathjar="/opt/cohorte/extra/jacoco/jacocoagent.jar", output="tcpserver", address="*", port="6300", includes="com.cohorte.*:org.cohorte.*")
        elif args.jacocoagent != None:
            # use 
            javaagent = args.jacocoagent
            
        # find in conf all isolate 
        parser = jsoncomment.JsonComment(json)
        parser.loads()
    else:
        print("do nothin, no argument received")
        
if __name__ == "__main__":
    sys.exit(main())
