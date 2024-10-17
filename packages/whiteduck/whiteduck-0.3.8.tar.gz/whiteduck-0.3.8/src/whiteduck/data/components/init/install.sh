#!/bin/bash

# Check if a path is provided as an argument
if [ -z "$1" ]; then
  echo "Please provide a path as an argument."
  exit 1
fi

# Change directory to the provided path
cd "$1" || { echo "Failed to change directory. Please ensure the path is correct."; exit 1; }

# Run the uv command with the specified arguments
uv init "$1" --lib
