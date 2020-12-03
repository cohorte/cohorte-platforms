FROM azul/zulu-openjdk-alpine:8

#-----------------------------------------------------------------------------
# Cohorte Base image X86 for cohorte device
#
# Contains: 
# - alpine linux 
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
MAINTAINER "Aurelien Pisu" <aurelien.pisu@cohorte-technologies.com>


ENV container docker

# installation du systemd au lieu du fakesystemd
# ceci est necessaire pour pouvoir lancer mysql et openldap comme un service OS
# avec les commandes "service" et "systemctl".

RUN apk update
RUN apk add  vim wget tar netcat-openbsd

RUN apk add  tzdata 



RUN apk add build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libssl-dev openssl lzma lzma-dev liblzma-dev make


RUN wget https://www.python.org/ftp/python/3.4.4/Python-3.4.4.tgz

RUN tar xzf Python-3.4.4.tgz

RUN cd Python-3.4.4; ./configure --prefix=/opt/python3.4 --with-zlib-dir=/usr/local/lib/ --with-ensurepip=install

RUN cd Python-3.4.4 ; make altinstall

RUN ln -s /opt/python3.4/bin/python3.4 /usr/bin/python
RUN ln -s /opt/python3.4/bin/python3.4 /usr/bin/python3
RUN ln -s /opt/python3.4/bin/python3.4 /usr/bin/python3.4
RUN ln -s /opt/python3.4/bin/pip3.4 /usr/bin/pip3
RUN ln -s /opt/python3.4/bin/pip3.4 /usr/bin/pip
RUN ln -s /opt/python3.4/bin/pip3.4 /usr/bin/pip3.4s


RUN cd Python-3.4.4 ; make clean



# Test de java
RUN java -version

# Pour definir des limitations (cpu, ram, etc) a des groupes de processus
VOLUME [ "/sys/fs/cgroup", "/var/log/journal" ]

CMD ["bash"]
