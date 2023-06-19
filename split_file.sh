#!/bin/bash

file="$1"
parts="${2:-2}"

# Check if the file argument is provided
if [ -z "$file" ]; then
    echo "Please provide the file name as the first argument."
    exit 1
fi

# Check if the file exists
if [ ! -f "$file" ]; then
    echo "File '$file' does not exist."
    exit 1
fi

# Get the base name of the file (without the extension)
base_name="${file%.*}"

# Determine the total number of lines in the file
total_lines=$(wc -l < "$file")

# Calculate the desired number of lines per part
lines_per_part=$(( (total_lines + parts - 1) / parts ))

# Split the file into the specified number of parts using awk
awk -v lines_per_part="$lines_per_part" -v base_name="$base_name" '
    BEGIN {
        part = 1
        file_name = base_name "_" sprintf("%02d", part) ".txt"
    }

    {
        print > file_name
        if (NR % lines_per_part == 0) {
            close(file_name)
            part++
            file_name = base_name "_" sprintf("%02d", part) ".txt"
        }
    }
' "$file"

echo "File '$file' has been split into $parts parts."


