# Cohorte Platform Distributions

This repository contains scripts allowing the generation of the different Cohorte distributions (python and full).

# How to build

# How to Release

- update dependencies versions (if needed)
- update pom.xml version
- update DEPENDENCIES.txt file to set new versions
- update requirements.txt file to set new versions
- update p2/category.xml file to set new versions

## Dependencies

You should first compile all dependencies.
To specifiy the exact version to include in Cohorte Platform distribution, you have to update:
- **pom.xml** file for Java bundles and
- **requirements.xml** file for Python modules.

## Build profiles

The *pom.xml* file contains several profiles which are explained in the following table. To launch a profile use the following command:

> mvn clean install -P <profile_id>

| Profile id                                 | Description  |
|--------------------------------------------|---|
| full                                       | Builds the full distribution which runs on different platforms (Windows, Linus, MacOSX, etc) and which can have Python and/or Java components.  |
| python                                     | Builds Python only distribution which is suitable for Python only applications |
| generate_local_p2                          | Generates a local P2 repository containing all the Jars of the distributions. This local P2 is used by "generate_update_site" profile to construct the update P2 site of the current distribution.  |
| generate_update_site                       | Builds the P2 update site and push it to Nexus server. |
| generate_docker_base_image                 | Builds the "base" docker image used by Cohorte Docker containers. Its is based on Centos7, installs JDK8, Python 3.4 and several tools.  |
| generate_docker_base_image_from_jenkins    | Same as the previous profile but launches the build script on another Host machine containing Docker runtime installed. |
| generate_docker_runtime_image              | Builds the "runtime" docker image containing the compiled Cohorte distribution. |
| generate_docker_runtime_image_from_jenkins | Same as the previous profile but launches the build script on another Host machine containing Docker runtime installed.  |
| generate_docker_node_image                 | Builds a "node" docker image containing a ready to use Cohorte node pre-configured and which runs automatically when the container is started. |
| generate_docker_node_image_from_jenkins    | Same as the previous profile but launches the build script on another Host machine containing Docker runtime installed.  |
| generate_docker_demo_image                 | Builds a "demo" docker image used to validate and checks if all is Ok. |
| generate_docker_demo_image_from_jenkins    | Same as the previous profile but launches the build script on another Host machine containing Docker runtime installed.  |

## Where the artefacts are deployed?

The compiled Cohorte distribution tar.gz files and the built Docker images and deployed on a Nexus server as follow :

- https://nrm.cohorte.tech/repository/cohorte-releases : contains compiled **python** and **full** distribution tar.gz files.
- https://nrm.cohorte.tech/repository/cohorte-p2-[VERSION] : (where [VERSION] is the version of the compiled distribution) contains the update P2 site.
- https://dr.cohorte.tech : contains the builts Docker images.

