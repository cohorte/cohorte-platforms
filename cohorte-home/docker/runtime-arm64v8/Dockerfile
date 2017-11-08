FROM cohorte/base-arm64v8:latest

#-----------------------------------------------------------------------------
# Cohorte Runtime image.
#
# Cohorte Platform version: 1.2.1
#-----------------------------------------------------------------------------

MAINTAINER "Bassem Debbabi" <bassem.debbabi@cohorte-technologies.com>

ENV REFRESHED_AT 20170707_1130

ENV COHORTE_HOME /opt/cohorte 

COPY ./install/cohorte-* /opt/cohorte

RUN cd ${COHORTE_HOME}


RUN sh ${COHORTE_HOME}/setup.sh
RUN sh ${COHORTE_HOME}/bin/cohorte-version
