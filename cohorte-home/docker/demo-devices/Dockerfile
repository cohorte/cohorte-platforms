FROM cohorte/node-devices:latest

#-----------------------------------------------------------------------------
# Cohorte Demo image. 
#-----------------------------------------------------------------------------

MAINTAINER "Bassem Debbabi" <bassem.debbabi@cohorte-technologies.com>

ENV REFRESHED_AT 20170824_1623

# Installation commands

COPY ./install/node /opt/node
COPY ./install/init.sh /opt

RUN chmod +x /opt/init.sh

RUN ls -l /opt
RUN ls -l /opt/node

EXPOSE 8090 8091 8092 8093
