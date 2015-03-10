@echo off

if "%COHORTE_HOME%" == "" (
	echo [ERROR] the system environment variable COHORTE_HOME is not defined!
	exit /b 1
)

if "%PYTHON_INTERPRETER%"=="" (
	echo [WARNING] the system environment variable PYTHON_INTERPRETER is not defined!
	echo           we will try to use 'python' by default!	
	set PYTHON_INTERPRETER=python
)

"%PYTHON_INTERPRETER%" "%COHORTE_HOME%\bin\scripts\cohorte-create-node.py" %*