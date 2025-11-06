#!/usr/bin/env bash
# This script provides two functions:
# 1. build - creates a virtual environment and installs dependencies
# 2. run - runs a Python script within that environment (requires --url argument)

set -e  # Exit immediately on error

VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
PYTHON_SCRIPT="uncl_extract.py"

build() {
    echo "🔧 Setting up Python virtual environment..."

    # Create virtual environment if not exists
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv "$VENV_DIR"
        echo "✅ Virtual environment created at '$VENV_DIR'"
    else
        echo "ℹ️ Virtual environment already exists at '$VENV_DIR'"
    fi

    # Activate environment
    source "$VENV_DIR/bin/activate"

    # Install dependencies
    if [ -f "$REQUIREMENTS_FILE" ]; then
        echo "📦 Installing dependencies from $REQUIREMENTS_FILE..."
        pip install --upgrade pip
        pip install -r "$REQUIREMENTS_FILE"
        echo "✅ Dependencies installed successfully."
    else
        echo "⚠️ No $REQUIREMENTS_FILE found. Skipping dependency installation."
    fi

    deactivate
}

run() {
    local URL_ARG=""

    # Parse arguments for --url
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            --url)
                if [[ -n "$2" && "$2" != --* ]]; then
                    URL_ARG="$2"
                    shift 2
                else
                    echo "❌ Error: --url requires a value."
                    exit 1
                fi
                ;;
            *)
                echo "⚠️ Unknown argument: $1"
                exit 1
                ;;
        esac
    done

    # Ensure URL is provided
    if [ -z "$URL_ARG" ]; then
        echo "❌ Error: The '--url' argument is mandatory."
        echo "Usage: $0 run --url <URL>"
        exit 1
    fi

    echo "🚀 Running Python program..."
    if [ ! -d "$VENV_DIR" ]; then
        echo "❌ Virtual environment not found. Run './uncl.sh build' first."
        exit 1
    fi

    # Activate environment
    source "$VENV_DIR/bin/activate"

    # Execute Python script with URL argument
    if [ -f "$PYTHON_SCRIPT" ]; then
        echo "🌐 Passing URL argument: $URL_ARG"
        python "$PYTHON_SCRIPT" --url "$URL_ARG"
    else
        echo "❌ Python script '$PYTHON_SCRIPT' not found."
        deactivate
        exit 1
    fi

    deactivate
}

# Main entry point
case "$1" in
    build)
        build
        ;;
    run)
        shift  # Remove the command name
        run "$@"
        ;;
    *)
        echo "Usage:"
        echo "  $0 build"
        echo "  $0 run --url <URL>"
        exit 1
        ;;
esac