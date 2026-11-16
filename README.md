# ALU Transcript Generator

## Overview

The **ALU Transcript Generator** is a small command-line project for
African Leadership University (ALU). It reads a CSV file containing a
student's assignment grades, validates the data, calculates the weighted
course grade and GPA, decides whether the student passed, and lists the
Formative assignments that are eligible for resubmission.

A companion Bash script, `organizer.sh`, archives the current grades file
with a timestamp and prepares a fresh workspace for the next batch of
grades.

This project was completed for **Lab 2: ALU Transcript Generator**.

---

## Purpose

The application demonstrates how to:

- Read and validate data from a CSV file.
- Apply assignment weights to calculate a final grade.
- Separate Formative (60%) and Summative (40%) performance.
- Convert a percentage grade into a GPA out of 5.0.
- Apply an independent pass mark to each category.
- Select resubmission candidates using a rule that handles ties.
- Automate file archiving, timestamping, and logging with Bash.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| **Python 3** | Main grading application |
| **CSV module** | Reading the grades file |
| **Bash** | Automating archive, reset, and logging |
| **Markdown** | Project documentation |

No third-party libraries are required.

---

## Project Files

| File | Purpose |
|---|---|
| `grade-evaluator.py` | Reads and validates grades, calculates the weighted grade and GPA, decides pass/fail, and finds resubmission options. |
| `grades.csv` | The input data: one row per assignment with `assignment`, `group`, `score`, and `weight`. |
| `organizer.sh` | Archives `grades.csv` into `archive/` with a timestamp, creates a new empty `grades.csv`, and appends to `organizer.log`. |
| `organizer.log` | Created automatically by the Bash script. Each run appends one entry; previous entries are preserved. |
| `archive/` | Created automatically by the Bash script. Stores timestamped copies of past grades files. |
| `README.md` | This documentation file. |

### CSV format

```csv
assignment,group,score,weight
Quiz,Formative,85,20
Group Exercise,Formative,40,20
Functions and Debugging Lab,Formative,45,20
Midterm Project - Simple Calculator,Summative,70,20
Final Project - Text-Based Game,Summative,60,20
```

- `group` must be `Formative` or `Summative` (capitalisation does not matter).
- `score` must be a number from 0 to 100.
- `weight` must be a positive number from 0 to 100.

---

## How to Run the Python Application

### Option 1: Pass the filename directly (recommended)

```bash
python3 grade-evaluator.py grades.csv
```

### Option 2: Let the program ask for the filename

```bash
python3 grade-evaluator.py
```

Then type:

```text
grades.csv
```

### Requirements

- Python 3.7 or newer.
- Run the command from the project folder, where `grades.csv` is located.

---

## How to Run the Bash Organizer

The script has executable permissions. Run it from the project folder:

```bash
./organizer.sh
```

If you ever need to restore the executable permission:

```bash
chmod +x organizer.sh
```

What the script does, in order:

1. Generates a timestamp in `YYYYMMDD-HHMMSS` format.
2. Creates the `archive/` directory if it does not exist (otherwise reuses it).
3. Checks that `grades.csv` exists.
4. Builds a unique archived filename such as
   `archive/grades_20261116-170000.csv`.
5. Moves the file into `archive/`. If that name already exists, `-1`, `-2`,
   and so on are added instead of overwriting.
6. Creates a new, empty `grades.csv` for the next batch.
7. Appends the timestamp, original filename, and archived filename to
   `organizer.log`.

### Example log output

```text
Timestamp: 20261116-170000
Original File: grades.csv
Archived File: archive/grades_20261116-170000.csv
```

> **Note:** Running `organizer.sh` moves the real `grades.csv`. To try it
> without touching your data, run it inside a temporary copy of the project.

---

## How GPA Is Calculated

Each assignment contributes:

```text
Weighted marks = (Score × Weight) / 100
```

The **total weighted grade** is the sum of the weighted marks of every
assignment:

```text
Total Grade = Sum of all (Score × Weight) / 100
```

The **GPA** is then scaled to a maximum of 5.0:

```text
GPA = (Total Grade / 100) × 5.0
```

### Worked example (the supplied `grades.csv`)

| Assignment | Group | Score | Weight | Weighted marks |
|---|---|---|---|---|
| Quiz | Formative | 85 | 20 | 17.00 |
| Group Exercise | Formative | 40 | 20 | 8.00 |
| Functions and Debugging Lab | Formative | 45 | 20 | 9.00 |
| Midterm Project - Simple Calculator | Summative | 70 | 20 | 14.00 |
| Final Project - Text-Based Game | Summative | 60 | 20 | 12.00 |

- Formative marks = 17 + 8 + 9 = **34 / 60** → **56.67%**
- Summative marks = 14 + 12 = **26 / 40** → **65.00%**
- Total weighted grade = **60.00%**
- GPA = (60 / 100) × 5.0 = **3.00 / 5.00**

---

## How the Pass/Fail Decision Works

A student passes only when **both** category percentages are at least 50%:

```text
Formative percentage >= 50%  AND  Summative percentage >= 50%   -> PASSED
Otherwise                                                       -> FAILED
```

The overall grade is **not** used to decide the status. For example, a
student could have a 60% overall grade but still fail if one category is
below 50%.

For the supplied data:

- Formative: 56.67% (passes)
- Summative: 65.00% (passes)
- **FINAL STATUS: PASSED**

---

## How Resubmission Eligibility Is Determined

Only **Formative** assignments can be resubmitted. Summative assignments
are never included.

The program:

1. Collects every Formative assignment with a score **below 50%**.
2. Finds the **highest weight** among those failed assignments.
3. Lists **every** failed assignment that shares that highest weight.
4. If nothing failed, prints a message saying no resubmission is needed.

For the supplied data, two Formative assignments failed and both have a
weight of 20:

- Group Exercise (Score: 40, Weight: 20)
- Functions and Debugging Lab (Score: 45, Weight: 20)

**Both** are listed, because they tie for the highest weight.

---

## Validation and Error Handling

The Python program validates the data before calculating anything. It
prints a clear message and stops when it finds:

- A missing file.
- An empty file, or a file with headers but no data rows.
- Missing or duplicate CSV columns.
- Empty rows or blank cells.
- Non-numeric scores or weights.
- Negative scores or scores above 100.
- Zero or negative weights.
- Weights that do not total 100.
- Formative weights that do not total 60.
- Summative weights that do not total 40.
- Assignment groups other than `Formative` or `Summative`.

The Bash script reports and exits on missing files, archive directory
creation failures, move failures, and log write failures.

---

## Example Commands

```bash
# Go to the project folder
cd alu-transcript-generator

# Run the grading application
python3 grade-evaluator.py grades.csv

# Run it interactively
python3 grade-evaluator.py

# Make the organizer executable (only needed once)
chmod +x organizer.sh

# Archive the current grades file and reset the workspace
./organizer.sh

# View the log history
cat organizer.log

# View archived files
ls -l archive/
```

---

## Expected Output for the Supplied Data

```text
Formative marks:       34.00 / 60   (56.67%)
Summative marks:       26.00 / 40   (65.00%)
Total weighted grade:  60.00%
Final GPA:             3.00 / 5.0

FINAL STATUS: PASSED

--- Resubmission Options ---
Failed Formative assignment(s) with the highest weight (20) that can be resubmitted:
  - Group Exercise (Score: 40, Weight: 20)
  - Functions and Debugging Lab (Score: 45, Weight: 20)
```

(Spacing may vary slightly; the values are what matter.)

---

## Author

Student project submitted for the ALU Individual Coding Lab,
**Lab 2: ALU Transcript Generator**.
