cd /home/rigel/Documents/Project/RCWA/python
#!/bin/bash

# Get the range of commits to compare
COMMIT_RANGE="HEAD~1 HEAD"

# Get the renamed files
changed_files=$(git diff --name-status --diff-filter=ACDM $COMMIT_RANGE)

modified_python_files=()

cd ..

# Filter the modified files to include only those in the python/ directory
for file in $changed_files; do
    if [[ $file == python/*.py ]]; then
        python $file
    fi
done



