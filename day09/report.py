#!/usr/bin/env python3
"""
DAY09 REPORT (ALL-IN-ONE)

INPUT (expected in same folder as this script):
  - subjects.txt  (tab-separated lines, like: issue_id<TAB>state<TAB>title<TAB>...optional columns)

OUTPUT (written into the same folder):
  - normalized_titles.csv
  - missing_submissions.csv
  - missing_submissions_report.md

What the report includes:
  - per-student missing required assignments (based on REQUIRED_ASSIGNMENTS list)
  - assignment coverage (how many submitted each required assignment)
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set, Tuple


# -----------------------------
# CONFIG (EDIT THIS)
# -----------------------------
REQUIRED_ASSIGNMENTS: List[str] = [
    "day01",
    "day02",
    "day03",
    "day04",
    "day05",
    "day06",
    "day08",
    # add more if needed:
    # "day09",
    # "final_project_proposal",
]


# -----------------------------
# PATHS (AUTO)
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
SUBJECTS_PATH = BASE_DIR / "subjects.txt"

NORMALIZED_CSV_PATH = BASE_DIR / "normalized_titles.csv"
MISSING_CSV_PATH = BASE_DIR / "missing_submissions.csv"
REPORT_MD_PATH = BASE_DIR / "missing_submissions_report.md"


# -----------------------------
# DATA STRUCTURE
# -----------------------------
@dataclass(frozen=True)
class NormalizedRow:
    issue_id: int
    state: str
    raw_title: str
    student: str
    assignments: Tuple[str, ...]
    format_tag: str


# -----------------------------
# NORMALIZATION HELPERS
# -----------------------------
def normalize_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def normalize_student_name(name: str) -> str:
    """
    Keep one stable form for student names:
    - trim
    - collapse spaces
    - replace ' - ' with space (so "A - B" won't split weird)
    - Title Case per token
    """
    if not name:
        return "UNKNOWN"

    s = normalize_spaces(name)

    # normalize dash spacing: turn "Rachel - Steinitz" into "Rachel Steinitz"
    s = re.sub(r"\s*-\s*", " ", s)
    s = normalize_spaces(s)

    # title-case each word (keeps it simple and stable)
    return " ".join(part.capitalize() for part in s.split(" "))


def _norm_day(n: int) -> str:
    return f"day{n:02d}"


def normalize_title(raw_title: str) -> Tuple[str, Tuple[str, ...], str]:
    """
    Returns:
      student, assignments(tuple), format_tag

    assignments are normalized to:
      dayXX, final_project_proposal, project_submission, unknown_assignment
    """
    t = normalize_spaces(raw_title)
    tl = t.lower()

    assignments: List[str] = []

    # detect proposal-like
    if (
        "final project proposal" in tl
        or "project proposal" in tl
        or "proposal for final project" in tl
        or ("proposal" in tl and "final project" in tl)
    ):
        assignments.append("final_project_proposal")

    if "project submission" in tl:
        assignments.append("project_submission")

    # day numbers (day 05, day05, Day 8, etc.)
    day_nums = [int(x) for x in re.findall(r"\bday\s*(\d+)\b", tl)]

    # catch: "day 05 and 06"
    m_and = re.search(r"\bday\s*(\d+)\s*(?:and|&)\s*(\d+)\b", tl)
    if m_and:
        day_nums.append(int(m_and.group(2)))

    for n in day_nums:
        key = _norm_day(n)
        if key not in assignments:
            assignments.append(key)

    if not assignments:
        assignments = ["unknown_assignment"]

    # student parsing
    student = "UNKNOWN"
    format_tag = "other"

    # "... by NAME"
    m = re.search(r"\bby\b\s+(.+)$", t, flags=re.IGNORECASE)
    if m:
        student = m.group(1).strip()
        format_tag = "has_by"
    else:
        # "...-NAME" (dash at end)
        if "-" in t:
            candidate = t.split("-")[-1].strip()
            # avoid taking "project ..." etc as name
            if candidate and not re.search(r"\bday\b|\bproject\b", candidate, re.IGNORECASE):
                student = candidate
                format_tag = "has_dash"
        else:
            # "day06 NAME"
            m2 = re.match(r"^\s*(day\s*\d+|day\d+)\s+(.+?)\s*$", t, flags=re.IGNORECASE)
            if m2:
                student = m2.group(2).strip()
                format_tag = "day_then_name"

    student = normalize_student_name(student)

    return student, tuple(assignments), format_tag


# -----------------------------
# STEP 1: READ + CLEAN INPUT
# -----------------------------
def read_subjects_txt(subjects_path: Path) -> List[Tuple[int, str, str]]:
    """
    Reads subjects.txt which is expected to be tab-separated.
    We only need:
      issue_id, state, title

    Accepts lines with >=3 columns; ignores empty/bad lines safely.
    """
    if not subjects_path.exists():
        raise FileNotFoundError(
            f"Cannot find input file: {subjects_path}\n"
            f"Tip: put 'subjects.txt' next to this script ({BASE_DIR})."
        )

    lines = subjects_path.read_text(encoding="utf-8").splitlines()
    out: List[Tuple[int, str, str]] = []

    for line in lines:
        if not line.strip():
            continue

        parts = line.split("\t")
        if len(parts) < 3:
            continue

        try:
            issue_id = int(parts[0].strip())
        except ValueError:
            continue

        state = normalize_spaces(parts[1])
        title = parts[2].strip()

        out.append((issue_id, state, title))

    return out


# -----------------------------
# STEP 2: NORMALIZE + WRITE normalized_titles.csv
# -----------------------------
def build_normalized_titles(subjects_path: Path, normalized_csv_path: Path) -> List[NormalizedRow]:
    raw_rows = read_subjects_txt(subjects_path)

    rows: List[NormalizedRow] = []
    for issue_id, state, raw_title in raw_rows:
        student, assignments, format_tag = normalize_title(raw_title)
        rows.append(
            NormalizedRow(
                issue_id=issue_id,
                state=state,
                raw_title=raw_title,
                student=student,
                assignments=assignments,
                format_tag=format_tag,
            )
        )

    with normalized_csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["issue_id", "state", "raw_title", "student", "assignments", "format_tag"])
        for r in rows:
            w.writerow([r.issue_id, r.state, r.raw_title, r.student, ";".join(r.assignments), r.format_tag])

    return rows


# -----------------------------
# STEP 3: COMPUTE "MISSING"
# -----------------------------
def compute_missing(rows: List[NormalizedRow], required: List[str]) -> Tuple[Dict[str, Set[str]], Dict[str, List[str]]]:
    """
    Returns:
      submissions: student -> set(assignments submitted)
      missing: student -> sorted list(missing required assignments)
    """
    required_set = {x.strip().lower() for x in required if x.strip()}
    submissions: Dict[str, Set[str]] = defaultdict(set)

    for r in rows:
        if r.student and r.student != "UNKNOWN":
            for a in r.assignments:
                submissions[r.student].add(a.strip().lower())

    missing: Dict[str, List[str]] = {}
    for student, submitted in submissions.items():
        miss = sorted(required_set - submitted)
        missing[student] = miss

    return submissions, missing


def compute_assignment_coverage(
    submissions: Dict[str, Set[str]],
    required: List[str],
) -> List[Tuple[str, int, int, float]]:
    required_list = [x.strip().lower() for x in required if x.strip()]
    students = sorted(submissions.keys())
    total = len(students)

    results: List[Tuple[str, int, int, float]] = []
    for a in required_list:
        submitted_count = sum(1 for s in students if a in submissions[s])
        rate = (submitted_count / total) if total else 0.0
        results.append((a, submitted_count, total, rate))

    results.sort(key=lambda x: (x[3], x[0]))
    return results


# -----------------------------
# STEP 4: WRITE OUTPUTS
# -----------------------------
def write_missing_csv(missing: Dict[str, List[str]], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["student", "missing_count", "missing_assignments"])
        for student in sorted(missing.keys()):
            miss = missing[student]
            w.writerow([student, len(miss), ";".join(miss)])


def write_report_md(
    submissions: Dict[str, Set[str]],
    missing: Dict[str, List[str]],
    required: List[str],
    out_path: Path,
) -> None:
    run_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    students = sorted(submissions.keys())
    total_students = len(students)

    missing_students = [s for s in students if missing.get(s)]
    ok_students = [s for s in students if not missing.get(s)]

    coverage = compute_assignment_coverage(submissions, required)
    required_str = ", ".join([x.strip().lower() for x in required if x.strip()])

    lines: List[str] = []
    lines.append("# Missing Submissions Report")
    lines.append("")
    lines.append(f"- Generated: **{run_time}**")
    lines.append(f"- Input file: `{SUBJECTS_PATH.name}`")
    lines.append(f"- Normalized CSV: `{NORMALIZED_CSV_PATH.name}`")
    lines.append(f"- Missing CSV: `{MISSING_CSV_PATH.name}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total students in dataset: **{total_students}**")
    lines.append(f"- Students with all required submissions: **{len(ok_students)}**")
    lines.append(f"- Students missing ≥1 required submission: **{len(missing_students)}**")
    lines.append("")
    lines.append("## Required assignments")
    lines.append("")
    lines.append(required_str)
    lines.append("")
    lines.append("## Assignment coverage (lowest first)")
    lines.append("")
    lines.append("| Assignment | Submitted | Total | Rate |")
    lines.append("|---|---:|---:|---:|")
    for a, submitted_count, total, rate in coverage:
        lines.append(f"| {a} | {submitted_count} | {total} | {rate:.1%} |")
    lines.append("")
    lines.append("## Students missing submissions")
    lines.append("")
    lines.append("| Student | Missing count | Missing assignments |")
    lines.append("|---|---:|---|")
    for student in students:
        miss_list = missing.get(student, [])
        if miss_list:
            lines.append(f"| {student} | {len(miss_list)} | {', '.join(miss_list)} |")
    lines.append("")
    lines.append("## Students with all required submissions")
    lines.append("")
    for student in ok_students:
        lines.append(f"- {student}")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


# -----------------------------
# MAIN
# -----------------------------
def main() -> None:
    # 1) normalize
    rows = build_normalized_titles(SUBJECTS_PATH, NORMALIZED_CSV_PATH)

    # 2) compute missing
    submissions, missing = compute_missing(rows, REQUIRED_ASSIGNMENTS)

    # 3) write outputs
    write_missing_csv(missing, MISSING_CSV_PATH)
    write_report_md(submissions, missing, REQUIRED_ASSIGNMENTS, REPORT_MD_PATH)

    # 4) print short summary
    total_students = len(submissions)
    missing_count = sum(1 for s in submissions if missing.get(s))

    print("Missing Submissions Report")
    print("=" * 26)
    print(f"Total students: {total_students}")
    print(f"Students missing >=1: {missing_count}")
    print(f"Wrote: {NORMALIZED_CSV_PATH}")
    print(f"Wrote: {MISSING_CSV_PATH}")
    print(f"Wrote: {REPORT_MD_PATH}")


if __name__ == "__main__":
    main()
