FROM arm64v8/centos

#-----------------------------------------------------------------------------
# Cohorte Base image ARM
#
# Contains: 
# - Centos7 
# - Oracle JVM 8 
# - Python 3.4
#
# Installed tools:
# - systemd (in place of fakesystemd) see https://hub.docker.com/_/centos/
# - vim
# - wget
# - tar
# - nc
# - python 3.4
#
# UPDATES:
# - MOD_BD_20161013 moving from centos7.1.x to centos7.2.15.11 
#      (needs systemd v232 - installed 219)
#-----------------------------------------------------------------------------

# meta-data
MAINTAINER "Bassem Debbabi" <bassem.debbabi@cohorte-technologies.com>

# force rebuilind all this Dockerfile by changing the date
ENV REFRESHED_AT 20161013_1730

ENV JAVA_VERSION 8u40
ENV JAVA_LONG_VERSION 8u40-b26
ENV JAVA_HOME /opt/java
ENV PATH $JAVA_HOME/bin:$PATH

# informer systemd qu'il s'execute sur un conteneur docker
ENV container docker

# installation du systemd au lieu du fakesystemd
# ceci est necessaire pour pouvoir lancer mysql et openldap comme un service OS
# avec les commandes "service" et "systemctl".
RUN yum -y update
RUN yum -y swap -- remove fakesystemd -- install systemd systemd-libs
RUN yum clean all; \
(cd /lib/systemd/system/sysinit.target.wants/; for i in *; \
do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;

# installer d'autres outils
RUN yum -y install vim wget tar nc && yum clean all 
RUN yum install -y epel-release
RUN yum install -y python34

# Installer Java 8 (Oracle)
# inspired from: https://hub.docker.com/r/cooniur/java/
RUN mkdir -p $JAVA_HOME \
    && wget --output-document=/tmp/java.tar.gz \
        --no-cookies --no-check-certificate \
        --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" \
        "http://download.oracle.com/otn-pub/java/jdk/$JAVA_LONG_VERSION/server-jre-$JAVA_VERSION-linux-x64.tar.gz"
RUN tar -xvf "/tmp/java.tar.gz" --directory="$JAVA_HOME" --strip-components 1
RUN rm /tmp/java.tar.gz*

# Test de java
RUN java -version

# Pour definir des limitations (cpu, ram, etc) a des groupes de processus
VOLUME [ "/sys/fs/cgroup", "/var/log/journal" ]

# au demarage lancer du conteneur, il faut lancer /usr/sbin/init (systemd)
CMD ["/usr/sbin/init"]
