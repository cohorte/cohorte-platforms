FROM ubuntu:18.04

#-----------------------------------------------------------------------------
# Cohorte Base image X86 for cohorte device
#
# Contains: 
# - ubuntu Bionic 
# - ZULU JVM 8 
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


ENV container docker

# installation du systemd au lieu du fakesystemd
# ceci est necessaire pour pouvoir lancer mysql et openldap comme un service OS
# avec les commandes "service" et "systemctl".

RUN apt-get update
RUN apt-get  install -y curl vim wget tar netcat-openbsd
RUN apt-get install -y java-common libasound2 libx11-6 libxau6 libxcb1 libxdmcp6 libxext6 libxi6 libxrender1 libxtst6 libfontconfig1
RUN wget https://cdn.azul.com/zulu/bin/zulu8.42.0.23-ca-jdk8.0.232-linux_amd64.deb
RUN dpkg -i *.deb

RUN apt-get install -y tzdata 

# installer d'autres outils and python3.4 for ubuntu 16.04 @see https://github.com/mhbashari/Install-Python3.4-on-Ubuntu-16.04

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

RUN cd Python-3.4.4 ; make clean



# Test de java
RUN java -version

# Pour definir des limitations (cpu, ram, etc) a des groupes de processus
VOLUME [ "/sys/fs/cgroup", "/var/log/journal" ]

# au demarage lancer du conteneur, il faut lancer /usr/sbin/init (systemd)
CMD ["/usr/sbin/init"]
