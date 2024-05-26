cd /home/rigel/Documents/Project/RCWA/python
#!/bin/bash

# Get the range of commits to compare
COMMIT_RANGE="HEAD~1 HEAD"

# Get the renamed files
renamed_files=$(git diff --name-status --diff-filter=R $COMMIT_RANGE)

# Check if there are renamed files
if [ -n "$renamed_files" ]; then
    echo "Renamed files:"
    echo "$renamed_files"
else
    echo "No renamed files found."
fi


