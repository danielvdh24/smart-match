#!/bin/bash

# Directory containing the model files
directory="$(pwd)/classifier/model"

# Initialize the highest version and filename variables
highest_version=""
highest_file=""

# Loop through each file in the directory matching the pattern
for file in "$directory"/model_v*.pkl; do
    # Extract the version number from the filename
    version=$(basename "$file" | grep -oP 'v\K[0-9]+\.[0-9]+\.[0-9]+')

    # If the highest version is not set, initialize it with the current version
    if [[ -z $highest_version ]]; then
        highest_version=$version
        highest_file=$(basename "$file" .pkl)  # Strip directory and extension
    else
        # Compare the current version with the highest version
        if [[ $(printf '%s\n' "$version" "$highest_version" | sort -Vr | head -n 1) == "$version" ]]; then
            highest_version=$version
            highest_file=$(basename "$file" .pkl)  # Strip directory and extension
        fi
    fi
done

# Output only the filename with its version
if [[ -n $highest_file ]]; then
    echo "$highest_file"
else
    echo "No matching files found in $directory"
fi
