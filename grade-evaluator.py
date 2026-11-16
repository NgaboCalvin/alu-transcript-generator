#!/usr/bin/env python3
"""
Lab 2: ALU Transcript Generator
--------------------------------
Reads a CSV file of assignment grades, validates the data, calculates the
student's weighted grade and GPA, decides whether the student passed, and
lists the Formative assignments that can be resubmitted.

Usage:
    python3 grade-evaluator.py grades.csv
    python3 grade-evaluator.py            # the program will ask for a filename
"""

import csv
import math
import os
import sys

# ---------------------------------------------------------------------------
# Constants used throughout the program (kept in one place for easy checking)
# ---------------------------------------------------------------------------
REQUIRED_COLUMNS = ["assignment", "group", "score", "weight"]

FORMATIVE = "Formative"
SUMMATIVE = "Summative"

FORMATIVE_TOTAL_WEIGHT = 60.0   # Formative assignments must add up to 60
SUMMATIVE_TOTAL_WEIGHT = 40.0   # Summative assignments must add up to 40
TOTAL_WEIGHT = 100.0            # The whole course must add up to 100

PASS_MARK = 50.0                # Minimum percentage needed in each category
GPA_SCALE = 5.0                 # GPA is calculated out of 5.0

# Small tolerance so that decimal weights such as 33.33 + 26.67 compare safely.
TOLERANCE = 0.001


# ---------------------------------------------------------------------------
# 1. LOADING AND VALIDATING THE CSV DATA
# ---------------------------------------------------------------------------
def load_csv_data(filename=None):
    """
    Ask the user for a CSV filename (or accept one from the command line),
    check that the file exists, and return a list of assignment dictionaries.

    Each dictionary looks like this:
        {
            "assignment": "Quiz",
            "group": "Formative",
            "score": 85.0,
            "weight": 20.0
        }

    If anything is wrong, a clear error message is printed and None is
    returned so that the rest of the program does not run.
    """
    # If no filename was passed in, ask the user for one.
    if filename is None:
        try:
            filename = input(
                "Enter the name of the CSV file to process (e.g., grades.csv): "
            ).strip()
        except EOFError:
            # This happens when the program runs without any keyboard input.
            print("Error: No filename was provided.")
            return None

    if filename == "":
        print("Error: No filename was provided. Please try again.")
        return None

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        return None

    if not os.path.isfile(filename):
        print(f"Error: '{filename}' is not a regular file.")
        return None

    assignments = []
    errors = []

    try:
        # utf-8-sig removes a hidden BOM some spreadsheet programs add.
        with open(filename, mode="r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            # An empty file has no header row at all.
            if reader.fieldnames is None:
                print(f"Error: The file '{filename}' is empty.")
                return None

            # Normalise the headers: remove spaces and ignore capital letters.
            clean_headers = []
            for header in reader.fieldnames:
                if header is None:
                    clean_headers.append("")
                else:
                    clean_headers.append(header.strip().lower())

            # Check for duplicate columns (for example two "score" columns).
            for column in REQUIRED_COLUMNS:
                if clean_headers.count(column) > 1:
                    print(f"Error: The column '{column}' appears more than once.")
                    return None

            # Check that every required column is present.
            missing_columns = []
            for column in REQUIRED_COLUMNS:
                if column not in clean_headers:
                    missing_columns.append(column)

            if missing_columns:
                print(
                    "Error: The CSV file is missing required column(s): "
                    + ", ".join(missing_columns)
                )
                print("Required columns are: " + ", ".join(REQUIRED_COLUMNS))
                return None

            # Read the data rows one by one. Row 1 is the header, so the
            # first data row is row 2.
            row_number = 1
            for row in reader:
                row_number += 1

                # Ignore the "None" key that csv uses for extra values.
                extra_values = row.get(None)
                if extra_values:
                    errors.append(
                        f"Row {row_number}: has more values than the header row."
                    )
                    continue

                # Build a dictionary with clean keys and values.
                record = {}
                for key, value in row.items():
                    if key is None:
                        continue
                    clean_key = key.strip().lower()
                    if value is None:
                        value = ""
                    record[clean_key] = value.strip()

                # Skip rows where every field is blank (an empty row).
                row_is_empty = True
                for value in record.values():
                    if value != "":
                        row_is_empty = False
                if row_is_empty:
                    errors.append(f"Row {row_number}: the row is empty.")
                    continue

                # Check that no cell is blank.
                blank_fields = []
                for column in REQUIRED_COLUMNS:
                    if record.get(column, "") == "":
                        blank_fields.append(column)
                if blank_fields:
                    errors.append(
                        f"Row {row_number}: missing value(s) for "
                        + ", ".join(blank_fields)
                        + "."
                    )
                    continue

                assignment_name = record["assignment"]
                group_name = record["group"]

                # Convert the score and weight from text to numbers.
                try:
                    score = float(record["score"])
                except ValueError:
                    errors.append(
                        f"Row {row_number} ('{assignment_name}'): score "
                        f"'{record['score']}' is not a valid number."
                    )
                    continue

                try:
                    weight = float(record["weight"])
                except ValueError:
                    errors.append(
                        f"Row {row_number} ('{assignment_name}'): weight "
                        f"'{record['weight']}' is not a valid number."
                    )
                    continue

                # Reject NaN and infinity, which are technically floats but
                # cannot be used in grade calculations.
                if not math.isfinite(score):
                    errors.append(
                        f"Row {row_number} ('{assignment_name}'): score must "
                        "be a normal number."
                    )
                    continue
                if not math.isfinite(weight):
                    errors.append(
                        f"Row {row_number} ('{assignment_name}'): weight must "
                        "be a normal number."
                    )
                    continue

                # Scores must be percentages between 0 and 100.
                if score < 0 or score > 100:
                    errors.append(
                        f"Row {row_number} ('{assignment_name}'): score "
                        f"{score:g} is invalid. Scores must be between 0 and 100."
                    )
                    continue

                # Weights must be positive. A weight above 100 is also
                # impossible when the total has to be 100.
                if weight <= 0:
                    errors.append(
                        f"Row {row_number} ('{assignment_name}'): weight "
                        f"{weight:g} is invalid. Weights must be greater than 0."
                    )
                    continue
                if weight > 100:
                    errors.append(
                        f"Row {row_number} ('{assignment_name}'): weight "
                        f"{weight:g} is invalid. A weight cannot be more than 100."
                    )
                    continue

                # The group must be either Formative or Summative.
                group_key = group_name.strip().lower()
                if group_key == "formative":
                    group_name = FORMATIVE
                elif group_key == "summative":
                    group_name = SUMMATIVE
                else:
                    errors.append(
                        f"Row {row_number} ('{assignment_name}'): unknown group "
                        f"'{group_name}'. Use '{FORMATIVE}' or '{SUMMATIVE}'."
                    )
                    continue

                # Everything for this row is valid, so store it.
                assignments.append(
                    {
                        "assignment": assignment_name,
                        "group": group_name,
                        "score": score,
                        "weight": weight,
                    }
                )

    except PermissionError:
        print(f"Error: Permission denied while reading '{filename}'.")
        return None
    except UnicodeDecodeError:
        print(f"Error: '{filename}' is not a valid text/CSV file.")
        return None
    except csv.Error as error:
        print(f"Error: The CSV file could not be read: {error}")
        return None
    except OSError as error:
        print(f"Error: Could not open '{filename}': {error}")
        return None

    # If any row was invalid, show every problem and stop.
    if errors:
        print("\nData validation failed:")
        for message in errors:
            print(f"  - {message}")
        print("\nGrades were not calculated because the data is invalid.")
        return None

    # A file with a header but no data rows is also invalid.
    if len(assignments) == 0:
        print(f"Error: '{filename}' does not contain any assignment rows.")
        return None

    return assignments


# ---------------------------------------------------------------------------
# 2. WEIGHT VALIDATION
# ---------------------------------------------------------------------------
def validate_weights(assignments):
    """
    Check the three weight rules:
        * Total weight  = 100
        * Formative     = 60
        * Summative     = 40

    Returns a list of error messages. An empty list means all rules passed.
    """
    formative_weight = 0.0
    summative_weight = 0.0

    for item in assignments:
        if item["group"] == FORMATIVE:
            formative_weight += item["weight"]
        else:
            summative_weight += item["weight"]

    total_weight = formative_weight + summative_weight
    errors = []

    if abs(total_weight - TOTAL_WEIGHT) > TOLERANCE:
        errors.append(
            f"Total assignment weight must be exactly 100, "
            f"but it is {total_weight:g}."
        )

    if abs(formative_weight - FORMATIVE_TOTAL_WEIGHT) > TOLERANCE:
        errors.append(
            f"Formative weight must be exactly 60, "
            f"but it is {formative_weight:g}."
        )

    if abs(summative_weight - SUMMATIVE_TOTAL_WEIGHT) > TOLERANCE:
        errors.append(
            f"Summative weight must be exactly 40, "
            f"but it is {summative_weight:g}."
        )

    return errors


# ---------------------------------------------------------------------------
# 3. GRADE CALCULATIONS
# ---------------------------------------------------------------------------
def calculate_category(assignments, group):
    """
    Calculate the marks earned in one category (Formative or Summative).

    Each assignment contributes: (score * weight) / 100

    Returns three values:
        earned   -> weighted marks earned
        weight   -> total weight of that category
        percent  -> earned / weight * 100
    """
    earned = 0.0
    weight = 0.0

    for item in assignments:
        if item["group"] == group:
            earned += (item["score"] * item["weight"]) / 100.0
            weight += item["weight"]

    if weight > 0:
        percent = (earned / weight) * 100.0
    else:
        percent = 0.0

    return earned, weight, percent


def calculate_total_grade(assignments):
    """Add up the weighted marks of every assignment."""
    total = 0.0
    for item in assignments:
        total += (item["score"] * item["weight"]) / 100.0
    return total


# ---------------------------------------------------------------------------
# 5. DISPLAYING THE REPORT
# ---------------------------------------------------------------------------
def print_assignment_table(assignments):
    """Print a simple, readable table of all assignments."""
    print("\n--- Assignment Records ---")
    print(f"{'Assignment':<40}{'Group':<12}{'Score':>8}{'Weight':>8}")
    print("-" * 68)

    for item in assignments:
        print(
            f"{item['assignment']:<40}"
            f"{item['group']:<12}"
            f"{item['score']:>8g}"
            f"{item['weight']:>8g}"
        )

    print("-" * 68)


# ---------------------------------------------------------------------------
def evaluate_grades(data):
    """
    Validate the weights, calculate the results, and print the grade summary.
    Returns True when the calculation finished, False when the data is invalid.
    """
    print("\n--- Processing Grades ---")

    weight_errors = validate_weights(data)
    if weight_errors:
        print("\nWeight validation failed:")
        for message in weight_errors:
            print(f"  - {message}")
        print("\nGrades were not calculated because the weights are invalid.")
        return False

    print_assignment_table(data)

    # --- Category calculations ---
    formative_earned, formative_weight, formative_percent = calculate_category(
        data, FORMATIVE
    )
    summative_earned, summative_weight, summative_percent = calculate_category(
        data, SUMMATIVE
    )

    # --- Overall grade and GPA ---
    total_grade = calculate_total_grade(data)
    gpa = (total_grade / 100.0) * GPA_SCALE

    print("\n--- Weight Validation ---")
    print(f"Formative weight: {formative_weight:g} / 60   OK")
    print(f"Summative weight: {summative_weight:g} / 40   OK")
    print(f"Total weight:     {formative_weight + summative_weight:g} / 100  OK")

    print("\n--- Grade Summary ---")
    print(
        f"Formative marks:      {formative_earned:6.2f} / {formative_weight:g}"
        f"   ({formative_percent:.2f}%)"
    )
    print(
        f"Summative marks:      {summative_earned:6.2f} / {summative_weight:g}"
        f"   ({summative_percent:.2f}%)"
    )
    print(f"Total weighted grade: {total_grade:.2f}%")
    print(f"Final GPA:            {gpa:.2f} / {GPA_SCALE:.1f}")

    # --- Pass / Fail decision ---
    # BOTH categories must independently reach at least 50%.
    formative_passed = formative_percent >= PASS_MARK
    summative_passed = summative_percent >= PASS_MARK

    print("\n--- Final Decision ---")
    if formative_passed and summative_passed:
        print("FINAL STATUS: PASSED")
    else:
        print("FINAL STATUS: FAILED")
        if not formative_passed:
            print(
                f"Reason: Formative percentage ({formative_percent:.2f}%) "
                "is below 50%."
            )
        if not summative_passed:
            print(
                f"Reason: Summative percentage ({summative_percent:.2f}%) "
                "is below 50%."
            )

    return True
# ---------------------------------------------------------------------------
# 6. PROGRAM ENTRY POINT
# ---------------------------------------------------------------------------
def main():
    # A filename can be given on the command line:
    #     python3 grade-evaluator.py grades.csv
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = None

    course_data = load_csv_data(filename)
    if course_data is None:
        sys.exit(1)

    if not evaluate_grades(course_data):
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
