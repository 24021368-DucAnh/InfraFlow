"""Check the PR #20 documentation package without contacting AWS or using secrets."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    ROOT / "docs/design/DUC-25-web-database-blueprint-review.md",
    ROOT / "docs/design/DUC-27-url-sleeping-health-cutover-review.md",
    ROOT / "docs/planning/DUC-24-G1-poc-authorization-and-evidence.md",
    ROOT / "docs/planning/DUC-25-27-40-41-week6-week7-handoff.md",
    ROOT / "docs/planning/DUC-25-27-P3-P5-evidence-test-sheets.md",
    ROOT / "docs/planning/DUC-25-27-W8-evidence-review.md",
    ROOT / "docs/planning/DUC-40-v12-contract-traceability-register.md",
    ROOT / "docs/superpowers/plans/2026-10-21-w6-w7-baseline-reconciliation.md",
]
errors: list[str] = []
texts: dict[str, str] = {}
relative_links = 0
external_links = 0


def fail(path: Path, line: int, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}:{line}: {message}")


for path in DOCS:
    if not path.is_file():
        errors.append(f"missing: {path.relative_to(ROOT)}")
        continue
    content = path.read_text(encoding="utf-8")
    texts[path.name] = content
    lines = content.splitlines()
    fence = None
    previous_heading = 0
    table_columns = None
    for number, line in enumerate(lines, 1):
        if line.rstrip() != line:
            fail(path, number, "trailing whitespace")
        if "\t" in line:
            fail(path, number, "tab in Markdown")
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            char, width = marker.group(1)[0], len(marker.group(1))
            if fence is None:
                fence = (char, width, number)
            elif fence[0] == char and width >= fence[1]:
                fence = None
            continue
        if fence is not None:
            continue
        heading = re.match(r"^(#{1,6})\s+", line)
        if heading:
            level = len(heading.group(1))
            if previous_heading and level > previous_heading + 1:
                fail(path, number, "skipped heading level")
            previous_heading = level
        if line.startswith("|") and line.endswith("|"):
            columns = line.count("|") - 1
            if table_columns is not None and columns != table_columns:
                fail(path, number, f"table has {columns} columns; expected {table_columns}")
            table_columns = columns
        else:
            table_columns = None
        for target in re.findall(r"(?<!!)\[[^]]+\]\((<[^>]+>|[^)]+)\)", line):
            target = target.strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme in {"https", "http"}:
                external_links += 1
                continue
            if parsed.scheme or target.startswith("#"):
                continue
            relative_links += 1
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_file():
                fail(path, number, f"broken relative link: {target}")
    if fence is not None:
        fail(path, fence[2], "unclosed code fence")


def catalogue(name: str, prefix: str) -> Counter[str]:
    text = texts.get(name, "")
    return Counter(re.findall(rf"^\| ({prefix}-\d{{2}}) \|", text, re.MULTILINE))


blueprint = catalogue("DUC-25-web-database-blueprint-review.md", "BP")
url = catalogue("DUC-27-url-sleeping-health-cutover-review.md", "URL")
contracts = catalogue("DUC-40-v12-contract-traceability-register.md", "CT")
maps = catalogue("DUC-40-v12-contract-traceability-register.md", "MAP")
for label, actual, expected in [
    ("BP", blueprint, {f"BP-{n:02d}" for n in range(1, 17)}),
    ("URL", url, {f"URL-{n:02d}" for n in range(1, 17)}),
    ("CT", contracts, {f"CT-{n:02d}" for n in range(1, 15)}),
    ("MAP", maps, {f"MAP-{n:02d}" for n in range(1, 13)}),
]:
    if set(actual) != expected or any(count != 1 for count in actual.values()):
        errors.append(f"{label} catalogue mismatch: missing={sorted(expected-set(actual))}, extra/duplicates={actual}")

sheet = texts.get("DUC-25-27-P3-P5-evidence-test-sheets.md", "")
recipe_rows = re.findall(r"^\| \*\*(P[35]-\d{2})\*\* → ([^|]+) \|", sheet, re.MULTILINE)
recipes = Counter(recipe for recipe, _ in recipe_rows)
recipe_coverage = {
    recipe: set(re.findall(r"(?:BP|URL)-\d{2}", covered))
    for recipe, covered in recipe_rows
}
expected_recipes = {f"P{probe}-{n:02d}" for probe in (3, 5) for n in range(1, 9)}
if set(recipes) != expected_recipes or any(count != 1 for count in recipes.values()):
    errors.append(f"P3/P5 recipe mismatch: missing={sorted(expected_recipes-set(recipes))}, counts={recipes}")

primary = re.findall(r"^\| (BP-\d{2}) \| (P[35]-\d{2}) \| (URL-\d{2}) \| (P[35]-\d{2}) \|$", sheet, re.MULTILINE)
mapped = Counter(item for row in primary for item in (row[0], row[2]))
expected_ids = set(blueprint) | set(url)
if len(primary) != 16 or set(mapped) != expected_ids or any(count != 1 for count in mapped.values()):
    errors.append(f"primary one-to-one coverage mismatch: rows={len(primary)}, counts={mapped}")
for row in primary:
    for case, recipe in ((row[0], row[1]), (row[2], row[3])):
        if recipe not in recipes:
            errors.append(f"primary map references undefined recipe {recipe}")
        elif case not in recipe_coverage[recipe]:
            errors.append(f"primary recipe {recipe} does not cover {case}")

all_docs = "\n".join(texts.values())
for stale in ("get_document` returned empty", "Source text v1.2 not fully retrievable", "anonymous Wake →", "conflicting work is denied/serialized", "Conflict denied/serialized"):
    if stale in all_docs:
        errors.append(f"stale source or Wake claim remains: {stale}")

if errors:
    print("DOC QA FAILED")
    print("\n".join(errors))
    raise SystemExit(1)
print(
    f"DOC QA PASS: {len(DOCS)} Markdown files; {relative_links} relative links; "
    f"{external_links} external link references; BP={len(blueprint)}, URL={len(url)}, "
    f"CT={len(contracts)}, MAP={len(maps)}, recipes={len(recipes)}, primary mappings={len(mapped)}"
)
