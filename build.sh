#!/bin/bash

for file in ./*.gz
do
  if [[ -f "$file" ]]; then
    echo "Processing $file..."
    python build_db.py "$file"
    
  else
    echo "No .gz files found in the directory."
  fi
done
echo "Build complete.  If there were no errors, the .gz files are not needed"
