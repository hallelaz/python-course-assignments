# Day 09 – Submission Report

This project analyzes assignment submissions based on the GitHub issues listed in
`subjects.txt` and generates a report describing **missing submissions per student**.

The entire workflow is implemented in a **single Python script**, as required.

---

## Files

### `report.py` – submission analysis and reporting  
Reads the raw issues from `subjects.txt`, cleans and normalizes the data, and
produces structured output files and a human-readable report.

### `subjects.txt` – raw input data  
Issues copied from the shared course repository.  
Each line represents a single GitHub issue and contains tab-separated fields,


---

## What the program does

The program reads the raw issue titles, normalizes assignment names and student
names, and determines which required assignments were submitted by each student.

Based on this information, it identifies missing submissions and summarizes the
results in both CSV and Markdown formats.

---

## Generated output files

### `normalized_titles.csv`  
An intermediate file containing the cleaned and normalized representation of each
issue, including extracted student names and assignment identifiers.

### `missing_submissions.csv`  
A per-student summary listing:
- how many required assignments are missing
- which assignments were not submitted

### `missing_submissions_report.md`  
A human-readable report summarizing:
- total number of students
- how many students submitted all required assignments
- how many students are missing at least one submission
- assignment coverage statistics
- a detailed table of missing submissions per student

---

### Requirements

Python 3.9 or newer.

The script uses only Python’s standard library modules
(csv, pathlib, re, datetime, collections, dataclasses, typing).
No external packages need to be installed.

---
### Interaction with AI 
I initially used the AI to assist in writing code for normalizing the raw text data.
The normalization process required several refinement iterations due to numerous edge cases, such as student names containing hyphens and other formatting inconsistencies. Addressing these cases involved the use of regular expressions.
After obtaining a consistently normalized representation of the text, I then used ChatGPT to help develop code that iterates over the processed data and determines which assignments were submitted by each student.

---

## How to run

From the root of the `python-course-assignments` repository:

```bash
python day09/report.py





