@ echo off
REM 声明采用UTF-8编码
chcp 65001

:: 区分是否有环境
for /f "delims=" %%i in ('python -m poetry env info -p') do set env_path=%%i

if "%env_path%"=="" (
echo 无环境
python -m poetry install
) else (
echo 有环境
python -m poetry run python -m pip install --upgrade pip
)

echo 更新环境
python -m poetry update
REM echo setuptools降级
REM python -m poetry run pip install setuptools==19.2.0

echo ------------------------------------------------
python -m poetry show
echo ------------------------------------------------
python -m poetry show --tree
echo ------------------------------------------------

python -m poetry env info -p | clip

pause