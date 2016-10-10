@echo off

REM Go to the Cohorte platform directory
pushd %~dp0

REM Set environment variables
echo [INFO] Exporting the COHORTE_HOME environment variable...
set COHORTE_HOME=%~dp0
set PATH="%COHORTE_HOME%/bin";%PATH%
echo [INFO] COHORTE_HOME=%COHORTE_HOME%

REM setup jpype
call "%COHORTE_HOME%\bin\cohorte-setup.bat"
REM Get back where we were
popd

echo [INFO] Done.
