FROM azul/zulu-openjdk:8

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

# installation du systemd au lieu du fakesystemd
# ceci est necessaire pour pouvoir lancer mysql et openldap comme un service OS
# avec les commandes "service" et "systemctl".

RUN apt-get update
RUN apt-get install -y vim wget tar netcat-openbsd 

RUN apt-get install -y tzdata python3


RUN python3 --version

# Test de java
RUN java -version

# Pour definir des limitations (cpu, ram, etc) a des groupes de processus
VOLUME [ "/sys/fs/cgroup", "/var/log/journal" ]

CMD ["bash"]
