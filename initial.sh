#!/bin/bash

# Content to be written into the file
content="private_key_here_with_0x
private_key_here_with_0x"

# Function to create the privatekey.txt file in the current directory and subdirectories
create_privatekey() {
    # Loop through the directories
    for dir in $(find . -type d); do
        # Check if the privatekey.txt file already exists in the directory
        if [ ! -f "$dir/privatekey.txt" ]; then
            # If the file doesn't exist, create it and write the content
            echo "$content" > "$dir/privatekey.txt"
            echo "Created privatekey.txt in $dir"
        else
            # If the file exists, skip
            echo "Skipping $dir, privatekey.txt already exists"
        fi
    done
}

# Call the function
create_privatekey
