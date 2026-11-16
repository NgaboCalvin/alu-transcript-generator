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
