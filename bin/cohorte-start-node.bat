@echo off

REM Use "python" if no interpreter is specified
if "%PYTHON_INTERPRETER%"=="" set PYTHON_INTERPRETER="python"
%PYTHON_INTERPRETER% %COHORTE_HOME%\bin\scripts\cohorte-start-node.py -c %*
