FROM ubuntu:18.04

#-----------------------------------------------------------------------------
# Cohorte Base image X86 for cohorte device
#
# Contains: 
# - Ubuntu linux 
# - ZULU JVM 8 
#
# Installed tools:
# - vim
# - wget
# - tar
# - nc
#
#-----------------------------------------------------------------------------

# meta-data
MAINTAINER "Aurelien Pisu" <aurelien.pisu@cohorte-technologies.com>


ENV container docker
ENV JAVA_HOME /opt/java
ENV PATH $JAVA_HOME/bin:$PATH
# installation du systemd au lieu du fakesystemd
# ceci est necessaire pour pouvoir lancer mysql et openldap comme un service OS
# avec les commandes "service" et "systemctl".
RUN mkdir -p $JAVA_HOME
COPY ./jdk/* /opt/java/
RUN chmod +x /opt/java/bin/*

RUN apt-get update
RUN apt-get install  vim wget tar netcat-openbsd

# Test de java
RUN java -version

# Pour definir des limitations (cpu, ram, etc) a des groupes de processus
VOLUME [ "/sys/fs/cgroup", "/var/log/journal" ]

CMD ["bash"]
