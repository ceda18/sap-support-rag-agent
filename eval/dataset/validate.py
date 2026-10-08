"""Check the frozen dataset (questions.jsonl) before any run uses it.

  docker compose exec -e PYTHONPATH=/app -w /eval api python -m dataset.validate
"""
import json
from collections import Counter
from pathlib import Path

from core.config import settings
from rag.retriever import load_chunks_from_json

QUESTIONS_PATH = Path(__file__).parent / "questions.jsonl"
EXPECTED_TYPES = {"synthetic": 30, "manual": 10, "unanswerable": 10}
EXPECTED_SUBTYPES = {"near_miss": 5, "out_of_domain": 5}
REQUIRED_FIELDS = {"id", "question", "type", "subtype", "gold_pages", "reference_answer"}


def load_questions(path=QUESTIONS_PATH):
    """One JSON object per line; blank lines are ignored."""
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def find_errors(questions, max_page):
    errors = []
    ids = Counter(q.get("id") for q in questions)
    errors += [f"duplicate id: {i}" for i, n in ids.items() if n > 1]

    for q in questions:
        qid = q.get("id", "?")
        missing = REQUIRED_FIELDS - q.keys()
        if missing:
            errors.append(f"{qid}: missing fields {sorted(missing)}")
            continue
        if not q["question"].strip():
            errors.append(f"{qid}: empty question")
        if q["type"] not in EXPECTED_TYPES:
            errors.append(f"{qid}: unknown type {q['type']!r}")
        elif q["type"] == "unanswerable":
            if q["gold_pages"]:
                errors.append(f"{qid}: unanswerable question must have gold_pages = []")
            if q["subtype"] not in EXPECTED_SUBTYPES:
                errors.append(f"{qid}: subtype must be near_miss or out_of_domain")
        else:
            if not q["gold_pages"]:
                errors.append(f"{qid}: answerable question needs at least one gold page")
            if not q["reference_answer"].strip():
                errors.append(f"{qid}: missing reference_answer")
            bad = [p for p in q["gold_pages"] if not isinstance(p, int) or not 1 <= p <= max_page]
            if bad:
                errors.append(f"{qid}: gold pages outside 1..{max_page}: {bad}")

    types = Counter(q.get("type") for q in questions)
    if dict(types) != EXPECTED_TYPES:
        errors.append(f"type counts {dict(types)}, expected {EXPECTED_TYPES}")
    subtypes = Counter(q.get("subtype") for q in questions if q.get("type") == "unanswerable")
    if dict(subtypes) != EXPECTED_SUBTYPES:
        errors.append(f"unanswerable subtypes {dict(subtypes)}, expected {EXPECTED_SUBTYPES}")
    return errors


def main():
    questions = load_questions()
    max_page = max(c.metadata["page"] for c in load_chunks_from_json(settings.CHUNKS_PATH))
    errors = find_errors(questions, max_page)

    print(f"{len(questions)} questions: {dict(Counter(q.get('type') for q in questions))}")
    multi = sum(1 for q in questions if len(q.get("gold_pages", [])) > 1)
    print(f"questions with more than one gold page: {multi}")
    if errors:
        print(f"\n{len(errors)} problem(s):")
        for e in errors:
            print("  -", e)
        raise SystemExit(1)
    print("OK - dataset is valid")


if __name__ == "__main__":
    main()