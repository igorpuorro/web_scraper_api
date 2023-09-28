@echo off
setlocal enabledelayedexpansion

REM Check for the command-line options
:check_options
set args=%*
if "%args%"=="" (
    echo Usage: %0 [--keygen] [--connect-to-container]
    exit /b 1
)
:parse_args
if "%~1"=="--keygen" (
    call :generate_ssh_key
    exit /b 0
)
if "%~1"=="--connect-to-container" (
    call :connect_to_container
    exit /b 0
)
echo Invalid option: %~1
exit /b 1

REM Function to generate an SSH key pair
:generate_ssh_key
echo Generating SSH key pair...
if not exist .\ssh mkdir .\ssh
ssh-keygen -t rsa -b 4096 -f .\ssh\id_rsa -N ""
goto :EOF

REM Function to connect to a container using SSH
:connect_to_container
echo Connecting to container using SSH...
if not exist .\ssh (
    echo SSH directory does not exist.
    exit /b 1
)

if not exist .\ssh\id_rsa (
    echo id_rsa file does not exist.
    exit /b 1
)

ssh-keygen -R "[localhost]:2222"
ssh -i .\ssh\id_rsa root@localhost -p 2222
goto :EOF
