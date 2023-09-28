#!/bin/bash

# Get the current directory and store it in a variable
current_dir=$(pwd)

# Function to generate an SSH key pair
function generate_ssh_key() {
    echo "Generating SSH key pair..."

    test ! -d "$current_dir"/ssh && mkdir "$current_dir"/ssh
    ssh-keygen -t rsa -b 4096 -f "$current_dir"/ssh/id_rsa -N ""
}

# Function to connect to a container using SSH
function connect_to_container() {
    echo "Connecting to container using SSH..."

    if [ ! -d "$current_dir"/ssh ]; then
        echo "SSH directory does not exist."
        exit 1
    fi

    if [ ! -f "$current_dir"/ssh/id_rsa ]; then
        echo "id_rsa file does not exist."
        exit 1
    fi

    ssh-keygen -f ~/.ssh/known_hosts -R "[localhost]:2222"

    ssh -i "$current_dir"/ssh/id_rsa root@localhost -p 2222
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
