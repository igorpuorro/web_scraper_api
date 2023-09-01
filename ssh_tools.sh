#!/bin/bash

# Function to generate an SSH key pair
function generate_ssh_key() {
    echo "Generating SSH key pair..."

    test ! -d ./ssh && mkdir ./ssh
    ssh-keygen -t rsa -b 4096 -f ./ssh/id_rsa -N ""
}

# Function to connect to a container using SSH
function connect_to_container() {
    echo "Connecting to container using SSH..."

    if [ ! -d ./ssh ]; then
        echo "SSH directory does not exist."
        exit 1
    fi

    if [ ! -f ./ssh/id_rsa ]; then
        echo "id_rsa file does not exist."
        exit 1
    fi

    ssh-keygen -R localhost

    ssh -i ./ssh/id_rsa root@localhost -p 2222
}

# Check for the command-line options
while [[ $# -gt 0 ]]; do
    case "$1" in
        --keygen)
            generate_ssh_key
            exit 0
            ;;
        --connect-to-container)
            connect_to_container
            exit 0
            ;;
        *)
            echo "Invalid option: $1"
            exit 1
            ;;
    esac
    shift
done

# If no valid options are provided, show usage information
echo "Usage: $0 [--keygen] [--connect-to-container]"
exit 1
