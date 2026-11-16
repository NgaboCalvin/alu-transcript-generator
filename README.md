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
