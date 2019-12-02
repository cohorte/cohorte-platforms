FROM ubuntu:18.04

#-----------------------------------------------------------------------------
# Cohorte Base image X86 for cohorte device
#
# Contains: 
# - ubuntu Bionic 
# - Oracle JVM 8 
# - Python 3.6
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
ENV JAVA_VERSION 8u151
ENV JAVA_LONG_VERSION 8u151-b12
ENV JAVA_HOME /opt/java
ENV PATH $JAVA_HOME/bin:$PATH

# informer systemd qu'il s'execute sur un conteneur docker
ENV container docker


# installation du systemd au lieu du fakesystemd
# ceci est necessaire pour pouvoir lancer mysql et openldap comme un service OS
# avec les commandes "service" et "systemctl".
RUN apt-get update

RUN apt-get install -y tzdata 

# installer d'autres outils and python3.4 for ubuntu 16.04 @see https://github.com/mhbashari/Install-Python3.4-on-Ubuntu-16.04
RUN apt-get  install -y curl vim wget tar netcat-openbsd

RUN apt-get  remove -y python3 python

RUN apt-get install -y build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libssl-dev openssl lzma lzma-dev liblzma-dev make


RUN wget https://www.python.org/ftp/python/3.4.4/Python-3.4.4.tgz

RUN tar xzf Python-3.4.4.tgz

RUN cd Python-3.4.4; ./configure --prefix=/opt/python3.4 --with-zlib-dir=/usr/local/lib/ --with-ensurepip=install

RUN cd Python-3.4.4 ; make altinstall
RUN apt-get remove -y build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libssl-dev openssl lzma lzma-dev liblzma-dev
RUN apt-get auto-remove -y

RUN ln -s /opt/python3.4/bin/python3.4 /usr/bin/python
RUN ln -s /opt/python3.4/bin/python3.4 /usr/bin/python3
RUN ln -s /opt/python3.4/bin/python3.4 /usr/bin/python3.4
RUN ln -s /opt/python3.4/bin/pip3.4 /usr/bin/pip3
RUN ln -s /opt/python3.4/bin/pip3.4 /usr/bin/pip
RUN ln -s /opt/python3.4/bin/pip3.4 /usr/bin/pip3.4s

# to have systemctl command
RUN apt-get install -y systemd
# Installer Java 8 (Oracle)
# inspired from: https://hub.docker.com/r/cooniur/java/
RUN mkdir -p $JAVA_HOME
COPY ./jdk/* /opt/java/
RUN chmod +x /opt/java/bin/*
RUN cd Python-3.4.4 ; make clean



# Test de java
RUN java -version

# Pour definir des limitations (cpu, ram, etc) a des groupes de processus
VOLUME [ "/sys/fs/cgroup", "/var/log/journal" ]

# au demarage lancer du conteneur, il faut lancer /usr/sbin/init (systemd)
CMD ["/usr/sbin/init"]
