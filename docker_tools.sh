#!/bin/bash

DOCKER_BIN="$(type -p docker 2>&1)"
DOCKERFILE="Dockerfile"
DOCKER_COMPOSE="docker-compose.yml"
SSH_DIR="ssh"

# Function to check dependency existence
check_dependency() {
    if [ ! -e "$1" ]; then
        echo >&2 "$1 not found."
        exit 1
    fi
}

# Function to check all dependencies
check_dependencies() {
    check_dependency "$DOCKER_BIN"
    check_dependency "$DOCKERFILE"
    check_dependency "$DOCKER_COMPOSE"
    check_dependency "$SSH_DIR"
}

# Print usage message
usage() {
    echo "Usage: $0 [OPTION]"
    echo
    echo "Options:"
    echo "  --build-image <image_name> <app_path>"
    echo "  --remove-image <image_name>"
    echo "  --start-container"
    echo "  --stop-container"
    exit 1
}

# Main

check_dependencies

# Parse command-line options
case "$1" in
    --build-image)
        if [ $# -ne 3 ]; then
            usage
        fi

        image_name="$2"
        app_path="$3"
        sanitized_app_path="$(sed 's/\. \// /g' <<<$app_path)"

        # Build image logic here
        echo "Building image '$image_name'"
        check_dependency "$app_path"
        docker build --build-arg="app_dir_name=$sanitized_app_path" -t "$image_name" .
        ;;

    --remove-image)
        if [ $# -ne 2 ]; then
            usage
        fi

        image_name="$2"

        echo "Removing image '$image_name'..."
        docker rmi "$image_name"
        ;;

    --start-container)
        if [ $# -ne 1 ]; then
            usage
        fi

        echo "Starting container..."
        docker-compose up -d
        ;;

    --stop-container)
        if [ $# -ne 1 ]; then
            usage
        fi

        echo "Stopping container..."
        docker-compose down
        ;;

    *)
        usage
        ;;
esac
