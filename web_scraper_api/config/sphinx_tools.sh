#!/bin/bash

# Define paths
script_path="$(dirname "$(realpath "$0")")"
sphinx_path="$script_path"/sphinx
module_path="$(dirname "$script_path")"
docs_path="$module_path"/docs

# Check if make and sphinx-apidoc are available
if ! command -v make >/dev/null || ! command -v sphinx-apidoc >/dev/null; then
    echo "Error: 'make' and 'sphinx-apidoc' commands are required."
    exit 1
fi

# Function to perform 'create_rsts' action
create_rsts_action() {
    cd "$sphinx_path" || exit
    sphinx-apidoc -f -t "$sphinx_path"/_templates -o "$sphinx_path" "$module_path"
}

# Function to perform 'make_clean' action
make_clean_action() {
    cd "$sphinx_path" || exit
    ls "$sphinx_path"/*.rst | fgrep -v 'index.rst' | xargs rm -f
    make clean
}

# Function to perform 'make_html' action
make_html_action() {
    cd "$sphinx_path" || exit
    make html
}

# Parse command line arguments
case "$1" in
    create_rsts)
        create_rsts_action
        ;;
    make_clean)
        make_clean_action
        ;;
    make_html)
        make_html_action
        ;;
    *)
        echo "Usage: $0 {create_rsts|make_clean|make_html}"
        exit 1
esac