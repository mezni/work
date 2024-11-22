#!/bin/bash

# Module name
MODULE="gencdr"

# Current date
DATE=$(date +%Y-%m-%d)

# Increment patch version
PATCH=$(date +%Y%m%d)
VERSION="v1.0.$PATCH"

# Clean tags
git tag -d $(git tag)
#git push origin --delete $(git tag)

# Git operations
git add .
git commit -m "$MODULE $DATE"
git tag -f $VERSION
git push origin main $VERSION --delete $(git tag)