@echo off

if "%COHORTE_HOME%" == "" (
  echo [ERROR] the system environment variable COHORTE_HOME is not defined!
  exit /b 1
)

call %COHORTE_HOME%\bin\cohorte-start-node.bat --base %CD% %*
