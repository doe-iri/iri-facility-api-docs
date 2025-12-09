#!/bin/sh
#
# Usage: ./convert_plantuml.sh SRC_DIR DEST_DIR
# Converts PlantUML files in SRC_DIR to PNG and moves PNGs to DEST_DIR.

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 SRC_DIR DEST_DIR" >&2
    exit 1
fi

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
SRC_DIR=$1
DEST_DIR=$2

# Check that source directory exists
if [ ! -d "$SRC_DIR" ]; then
    echo "Error: source directory '$SRC_DIR' does not exist" >&2
    exit 1
fi

# Create destination directory if needed
if [ ! -d "$DEST_DIR" ]; then
    mkdir -p "$DEST_DIR" || {
        echo "Error: could not create destination directory '$DEST_DIR'" >&2
        exit 1
    }
fi

found_any=false

# Adjust extensions here if you use different ones
for ext in pml puml plantuml uml; do
    for file in "$SRC_DIR"/*."$ext"; do
        # If the glob doesn't match anything, it returns the pattern itself
        [ -e "$file" ] || continue

        found_any=true
        echo "Converting: $file"

        # Run PlantUML to produce a PNG in the same directory as the source file
        # Assumes `plantuml` is on your PATH. If not, replace with:
        #   java -jar /path/to/plantuml.jar -tpng "$file"
        java -jar "$SCRIPT_DIR/plantuml-1.2025.10.jar" -tpng "$file" || {
            echo "Warning: PlantUML failed for '$file'" >&2
            continue
        }

        # Expected PNG name is same basename + .png
        png_file=${file%.*}.png

        if [ -f "$png_file" ]; then
            mv "$png_file" "$DEST_DIR"/ || {
                echo "Warning: could not move '$png_file' to '$DEST_DIR'" >&2
            }
        else
            echo "Warning: PNG not found for '$file' (expected '$png_file')" >&2
        fi
    done
done

if [ "$found_any" = false ]; then
    echo "No PlantUML files (*.puml, *.plantuml, *.uml) found in '$SRC_DIR'." >&2
fi

