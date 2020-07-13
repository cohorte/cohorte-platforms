#!/bin/sh 

mvn clean install -U -Ppython

mvn deploy -U -Ppython

mvn clean install -U -Pfull

mvn deploy -U -Pfull

mvn deploy -U -P generate_local_p2

mvn deploy -U -P generate_update_site

mvn install -P generate_docker_runtime_image

mvn install -P generate_docker_node_image

mvn install -P generate_docker_demo_image
