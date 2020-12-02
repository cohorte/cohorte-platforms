FROM mcr.microsoft.com/windows/servercore:1809

ARG PASSWORD
ENV PASSWORD ${PASSWORD:-root_password}

COPY install/install.psl C:/install.ps1

RUN powershell C:/install.ps1; \
    powershell -Command "Remove-Item C:/install.ps1 -Force"


CMD ["powershell"]