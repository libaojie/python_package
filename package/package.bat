@echo off

:: 复制必要的dll
md C:\Users\li\.virtualenvs\package_project-kQjJIRGx\DLLS\
copy C:\Users\li\Documents\01_Code\02_Python\python_package\package\windows\sqlite3.dll C:\Users\li\.virtualenvs\package_project-kQjJIRGx\DLLS\sqlite3.dll


:: 打包
rd /s /q build
python -m pipenv run python setup.py build

pause