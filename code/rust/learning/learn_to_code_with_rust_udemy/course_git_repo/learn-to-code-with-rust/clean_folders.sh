#!/bin/bash

# Loop through each directory in the current folder (one level deep)
for dir in */; do
  if [ -d "$dir" ]; then
    echo "Cleaning $dir..."
    (cd "$dir" && cargo clean)
  fi
done