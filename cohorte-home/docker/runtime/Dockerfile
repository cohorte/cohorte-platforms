FROM cohorte/base:1.5

#-----------------------------------------------------------------------------
# Cohorte Runtime image.
#
# Cohorte Platform version: 1.2.1
#-----------------------------------------------------------------------------

MAINTAINER "Bassem Debbabi" <bassem.debbabi@cohorte-technologies.com>

ENV REFRESHED_AT 20170707_1130

ENV COHORTE_HOME /opt/cohorte 

COPY ./install/cohorte.tar.gz ./opt/cohorte.tar.gz

RUN cd ./opt ; tar xvf cohorte.tar.gz
RUN rm -f ./opt/cohorte.tar.gz
RUN ls -l ./opt
RUN mv -f /opt/cohorte-* /opt/cohorte
RUN ls -l ./opt
RUN cd ${COHORTE_HOME}
#RUN mv -f /opt/cohorte/extra/linux /opt/cohorte/extra/Linux
RUN ls -l /opt/cohorte/extra/linux/
RUN sh ${COHORTE_HOME}/setup.sh
RUN sh ${COHORTE_HOME}/bin/cohorte-version
