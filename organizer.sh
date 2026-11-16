#!/usr/bin/env bash
#
# organizer.sh
# ------------
# Archives the current grades.csv file into an "archive" folder, gives the
# archived copy a timestamp, creates a fresh empty grades.csv, and records
# every archiving action in organizer.log.
#
# Run it from the project folder:
#     ./organizer.sh
#
# Requirements: Bash and the standard "date", "mkdir", "mv", and "printf"
# commands, which are available on macOS and Linux.

# Variables used by the script. Keeping them at the top makes the script
# easy to read and easy to change.
CSV_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

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
# -d tests whether "archive" is already a directory. If it is, we reuse it.
# If it is not, mkdir creates it.
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
# -f is true only when the path exists AND is a regular file.
if [ ! -f "$CSV_FILE" ]; then
    echo "Error: '$CSV_FILE' was not found in the current directory."
    echo "Nothing to archive. The workspace was not changed."
    exit 1
fi

# ---------------------------------------------------------------------------
# 4. Build the archived filename
# ---------------------------------------------------------------------------
# ${CSV_FILE%.*} removes the shortest extension from the end: "grades.csv"
# becomes "grades". ${CSV_FILE##*.} keeps only the extension: "csv".
BASENAME="${CSV_FILE%.*}"
EXTENSION="${CSV_FILE##*.}"

DESTINATION="$ARCHIVE_DIR/${BASENAME}_${TIMESTAMP}.${EXTENSION}"

# ---------------------------------------------------------------------------
# 5. Avoid overwriting an existing archived file
# ---------------------------------------------------------------------------
# If the timestamped name is already taken (for example the script is run
# twice within the same second), add -1, -2, ... until a free name is found.
# -e is true when the path exists (a file OR a directory).
COUNT=1
while [ -e "$DESTINATION" ]; do
    DESTINATION="$ARCHIVE_DIR/${BASENAME}_${TIMESTAMP}-${COUNT}.${EXTENSION}"
    COUNT=$((COUNT + 1))
done

# ---------------------------------------------------------------------------
# 6. Move the CSV file into the archive directory
# ---------------------------------------------------------------------------
if mv "$CSV_FILE" "$DESTINATION"; then
    echo "Archived: $CSV_FILE -> $DESTINATION"
else
    echo "Error: Could not move '$CSV_FILE' to '$DESTINATION'."
    echo "The original file was left in place where possible."
    exit 1
fi

# ---------------------------------------------------------------------------
# 7. Create a new, empty grades.csv for the next batch
# ---------------------------------------------------------------------------
# The colon (:) does nothing successfully, so ": > file" simply creates an
# empty file (or empties an existing one).
if : > "$CSV_FILE"; then
    echo "Created a fresh empty $CSV_FILE for the next batch."
else
    echo "Error: Could not create a new '$CSV_FILE'."
    exit 1
fi

# ---------------------------------------------------------------------------
# 8. Append an entry to the log file
# ---------------------------------------------------------------------------
# >> means append, so old log entries are never deleted.
if printf 'Timestamp: %s\nOriginal File: %s\nArchived File: %s\n\n' \
    "$TIMESTAMP" "$CSV_FILE" "$DESTINATION" >> "$LOG_FILE"; then
    echo "Log entry added to $LOG_FILE"
else
    echo "Error: Could not write to '$LOG_FILE'."
    exit 1
fi

echo "=== Archiving finished successfully ==="
exit 0
