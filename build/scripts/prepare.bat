REM Python preparation file
@echo off
echo [INFO] Preparing Python dependencies...

REM Variables
set INDEX_URL=http://forge.cohorte-technologies.com:7080/jenkins/cohorte/+simple/
set VENV_NAME=tmp_venv
set PATH=%WORKSPACE%/%VENV_NAME%/bin;%PATH%

REM Prepare the virtual environment
if exist %VENV_NAME% rmdir /S /Q %VENV_NAME%
python -m venv %VENV_NAME% || exit /b 2

REM Activate it
call %VENV_NAME%\Scripts\activate.bat

REM Install test and deployment tools
pip install --upgrade --index-url=%INDEX_URL% pip setuptools || exit /b 2
pip install --upgrade --index-url=%INDEX_URL% wheel || exit /b 2
pip install --upgrade --index-url=%INDEX_URL% nose || exit /b 2
pip install --upgrade --index-url=%INDEX_URL% devpi-client || exit /b 2

REM Install JPype
pip install --upgrade --index-url=%INDEX_URL% JPype1-py3 || exit /b 2

REM Install dependencies
pip install --upgrade --index-url=%INDEX_URL% -r build/scripts/requirements.txt || exit /b 2

REM Copy dependencies to repo
move /Y %VENV_NAME%\Lib\site-packages\jsonrpclib repo
move /Y %VENV_NAME%\Lib\site-packages\sleekxmpp repo
move /Y %VENV_NAME%\Lib\site-packages\requests repo
move /Y %VENV_NAME%\Lib\site-packages\herald repo
move /Y %VENV_NAME%\Lib\site-packages\jpype repo
move /Y %VENV_NAME%\Lib\site-packages\jpypex repo
move /Y %VENV_NAME%\Lib\site-packages\_jpype.pyd repo
move /Y %VENV_NAME%\Lib\site-packages\pelix repo
move /Y %VENV_NAME%\Lib\site-packages\cohorte repo
move /Y %VENV_NAME%\Lib\site-packages\webadmin repo

REM Clean up
call %VENV_NAME%\Scripts\deactivate.bat
rmdir /S /Q %VENV_NAME%

echo [INFO] Python dependencies are installed on repo
