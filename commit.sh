#!/bin/bash

# Module name
MODULE="gencdr"

# Current date
DATE=$(date +%Y-%m-%d)

# Increment patch version
PATCH=$(date +%Y%m%d)
VERSION="v1.0.$PATCH"

# Git operations
git add .
git commit -m "$MODULE $DATE"
git tag $VERSION
git push origin main $VERSION