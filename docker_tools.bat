@echo off
setlocal enabledelayedexpansion

rem Check if docker.exe is in the PATH
where docker.exe >nul 2>&1
if %errorlevel% neq 0 (
    echo docker.exe not found in PATH.
    exit /b 1
)

rem Check if Dockerfile exists in the current directory
if not exist Dockerfile (
    echo Dockerfile not found in the current directory.
    exit /b 1
)

rem Check if docker-compose.yml file exists in the current directory
if not exist docker-compose.yml (
    echo docker-compose.yml not found in the current directory.
    exit /b 1
)

rem Check if an ssh directory exists in the current directory
if not exist ssh\ (
    echo ssh directory not found in the current directory.
    exit /b 1
)

REM Check the number of arguments
if "%~1"=="" (
    goto :noArguments
)

:main
set "option=%~1"

if "%option%"=="--build-image" (
    call :buildImage %2 %3
    exit /b 1
) else if "%option%"=="--remove-image" (
    call :removeImage %2
    exit /b 1
) else if "%option%"=="--start-container" (
    call :startContainer
    exit /b 1
) else if "%option%"=="--stop-container" (
    call :stopContainer
    exit /b 1
) else (
    echo Invalid option: %option%
    exit /b 1
)

shift
goto :main

:noArguments
echo Usage: %~nx0 [OPTION]
echo. 
echo Options:
echo   --build-image ^<image_name^> ^<app_path^>
echo   --remove-image ^<image_name^>
echo   --start-container
echo   --stop-container
exit /b 1

:buildImage
set "image_name=%1"
set "app_path=%2"
set "sanitized_app_path=!app_path:.=!!"
set "sanitized_app_path=!sanitized_app_path:\=!!"

echo Building image %image_name%
echo build --build-arg="app_dir_name=%sanitized_app_path%" -t "%image_name%" .
docker build --build-arg="app_dir_name=%sanitized_app_path%" -t "%image_name%" .
exit /b 0

:removeImage
set "image_name=%1"

echo Removing image %image_name%
docker rmi "%image_name%"
exit /b 0

:startContainer
echo Starting container...
docker-compose up -d
exit /b 0

:stopContainer
echo Stopping container...
docker-compose down
exit /b 0
