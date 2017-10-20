FROM arm64v8/debian

#-----------------------------------------------------------------------------
# Cohorte Base image ARM
#
# Contains: 
# - Debian Stretch 
# - Oracle JVM 8 
# - Python 3.4
#
# Installed tools:
# - vim
# - wget
# - tar
# - nc
# - python 3.4
#
#-----------------------------------------------------------------------------

# meta-data
MAINTAINER "Bassem Debbabi" <bassem.debbabi@cohorte-technologies.com>

# force rebuilind all this Dockerfile by changing the date
ENV REFRESHED_AT 20161013_1730
ENV JAVA_VERSION 8u51
ENV JAVA_LONG_VERSION 8u51
ENV JAVA_HOME /opt/java
ENV PATH $JAVA_HOME/bin:$PATH

# informer systemd qu'il s'execute sur un conteneur docker
ENV container docker

# installation du systemd au lieu du fakesystemd
# ceci est necessaire pour pouvoir lancer mysql et openldap comme un service OS
# avec les commandes "service" et "systemctl".
RUN apt-get update


# installer d'autres outils
RUN apt-get  install -y vim wget tar netcat-openbsd
#RUN apt-get  install -y epel-release
RUN apt-get  install -y python3.4

# Installer Java 8 (Oracle)
# inspired from: https://hub.docker.com/r/cooniur/java/
RUN mkdir -p $JAVA_HOME
COPY ./jdk/* /opt/java/
   
# Test de java
RUN java -version
# Test de java
RUN java -version

# Pour definir des limitations (cpu, ram, etc) a des groupes de processus
VOLUME [ "/sys/fs/cgroup", "/var/log/journal" ]

# au demarage lancer du conteneur, il faut lancer /usr/sbin/init (systemd)
CMD ["/usr/sbin/init"]
