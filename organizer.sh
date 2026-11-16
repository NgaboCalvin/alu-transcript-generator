#!/usr/bin/env bash
#
# organizer.sh
# ------------
# Archives the current grades.csv file into an "archive" folder, gives the
# archived copy a timestamp, and creates a fresh empty grades.csv.
#
# Run it from the project folder:
#     ./organizer.sh

CSV_FILE="grades.csv"
ARCHIVE_DIR="archive"

echo "=== ALU Grades Organizer ==="

# ---------------------------------------------------------------------------
# 1. Create a timestamp in the format YYYYMMDD-HHMMSS
# ---------------------------------------------------------------------------
TIMESTAMP=$(LC_ALL=C date +"%Y%m%d-%H%M%S")

if [ -z "$TIMESTAMP" ]; then
    echo "Error: Could not generate a timestamp. Archiving cancelled."
    exit 1
fi

echo "Timestamp: $TIMESTAMP"

# ---------------------------------------------------------------------------
# 2. Make sure the archive directory exists
# ---------------------------------------------------------------------------
if [ -d "$ARCHIVE_DIR" ]; then
    echo "Archive directory already exists: $ARCHIVE_DIR"
else
    if mkdir "$ARCHIVE_DIR"; then
        echo "Created archive directory: $ARCHIVE_DIR"
    else
        echo "Error: Could not create the '$ARCHIVE_DIR' directory. Archiving cancelled."
        exit 1
    fi
fi

# ---------------------------------------------------------------------------
# 3. Check that the grades file exists
# ---------------------------------------------------------------------------
if [ ! -f "$CSV_FILE" ]; then
    echo "Error: '$CSV_FILE' was not found in the current directory."
    echo "Nothing to archive. The workspace was not changed."
    exit 1
fi

# ---------------------------------------------------------------------------
# 4. Build the archived filename
# ---------------------------------------------------------------------------
BASENAME="${CSV_FILE%.*}"
EXTENSION="${CSV_FILE##*.}"

DESTINATION="$ARCHIVE_DIR/${BASENAME}_${TIMESTAMP}.${EXTENSION}"

# ---------------------------------------------------------------------------
# 5. Move the CSV file into the archive directory
# ---------------------------------------------------------------------------
if mv "$CSV_FILE" "$DESTINATION"; then
    echo "Archived: $CSV_FILE -> $DESTINATION"
else
    echo "Error: Could not move '$CSV_FILE' to '$DESTINATION'."
    echo "The original file was left in place where possible."
    exit 1
fi

# ---------------------------------------------------------------------------
# 6. Create a new, empty grades.csv for the next batch
# ---------------------------------------------------------------------------
if : > "$CSV_FILE"; then
    echo "Created a fresh empty $CSV_FILE for the next batch."
else
    echo "Error: Could not create a new '$CSV_FILE'."
    exit 1
fi

echo "=== Archiving finished successfully ==="
exit 0
