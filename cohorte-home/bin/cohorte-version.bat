@echo off

if "%COHORTE_HOME%" == "" (
	echo [ERROR] the system environment variable COHORTE_HOME is not defined!
	exit /b 1
)

echo --------------------------------------------------------------------
echo COHORTE 
echo    version : 1.0.1
echo    home    : %COHORTE_HOME%
echo --------------------------------------------------------------------  