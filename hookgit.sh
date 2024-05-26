cd /home/rigel/Documents/Project/RCWA/python
#!/bin/bash

# Get the range of commits to compare
COMMIT_RANGE="HEAD~1 HEAD"

# Get the renamed files
changed_files=$(git diff --name-status --diff-filter=ACDM $COMMIT_RANGE)


# Check if there are renamed files
if [ -n "$changed_files" ]; then
    echo "changed files:"
    echo "$changed_files"
else
    echo "No changed files found."
fi


