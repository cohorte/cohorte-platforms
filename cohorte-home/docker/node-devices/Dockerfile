FROM cohorte/runtime-devices:latest

#-----------------------------------------------------------------------------
# Cohorte Runtime image.
#
# Cohorte Platform version: 1.2.1
#-----------------------------------------------------------------------------

MAINTAINER "Bassem Debbabi" <bassem.debbabi@cohorte-technologies.com>

ENV REFRESHED_AT 20170707_1130

# Installation commands

ENV COHORTE_BASE /opt/node
ENV COHORTE_DATA /opt/data

RUN mkdir -p $COHORTE_BASE
RUN mkdir -p $COHORTE_DATA
COPY ./install/run_service /opt
COPY ./install/boot.sh /opt
COPY ./install/cohorte.service ./etc/systemd/system/cohorte.service
COPY ./install/get-pip.py /tmp/
COPY ./install/init_* /opt/

RUN chmod +x /opt/init*.sh

# install pip 
RUN python3 /tmp/get-pip.py 
RUN pip3 install jsoncomment simpleeval

RUN chmod +x /opt/boot.sh

RUN systemctl enable cohorte.service

ENTRYPOINT ["/opt/boot.sh"]

RUN ls -l /opt

VOLUME [ "/opt/node" ]

EXPOSE 9000 9001 8000 8001 8002 8003 8004 8005 8006 8007 8008 8009 8010
