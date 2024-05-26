#!/bin/bash

# Define your repository directory
REPO_DIR="/path/to/your/repository"

# Pull the latest changes from the repository
git -C $REPO_DIR pull origin main

# Run your specific code or command here within the repository directory
# Replace `your_command_here` with the command you need to run
(cd $REPO_DIR && your_command_here)

# Check if there are any changes
if [ -n "$(git -C $REPO_DIR status --porcelain)" ]; then
  # Stage all changes
  git -C $REPO_DIR add .

  # Commit the changes with a message
  git -C $REPO_DIR commit -m "Automated commit message"

  # Push the changes to the repository
  git -C $REPO_DIR push origin main
else
  echo "No changes to commit."
fi
