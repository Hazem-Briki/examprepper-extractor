
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup


# Project paths
BASE_DIR = Path(__file__).resolve().parent
SAVED_PAGES_DIR = BASE_DIR / "saved_pages"
OUTPUT_FILE = BASE_DIR / "questions.json"


def page_number(path):
    match = re.search(r"Page\s+(\d+)", path.name, re.IGNORECASE)
    return int(match.group(1)) if match else 0


def extract_questions(html_file):
    """Extract embedded question records from one saved HTML page."""
    try:
        with html_file.open("r", encoding="utf-8", errors="ignore") as file:
            soup = BeautifulSoup(file, "html.parser")

        script = soup.find("script", id="__NEXT_DATA__")

        if script is None or not script.string:
            print(f"SKIP: No embedded question data: {html_file.name}")
            return []

        data = json.loads(script.string)
        page_props = data.get("props", {}).get("pageProps", {})
        records = page_props.get("questions", [])

        if not isinstance(records, list):
            print(f"SKIP: Unexpected question format: {html_file.name}")
            return []

        extracted = []

        for item in records:
            if not isinstance(item, dict):
                continue

            question_text = item.get("question_text", "").strip()
            choices = item.get("choices", {})
            answer = str(item.get("answer", "")).strip().upper()

            if not question_text or not isinstance(choices, dict):
                continue

            options = [
                f"{letter}. {text}"
                for letter, text in choices.items()
            ]

            # Resolve single or multiple answer letters, e.g. B or BDE.
            correct_answers = []

            for letter in answer:
                if letter in choices:
                    correct_answers.append(
                        f"{letter}. {choices[letter]}"
                    )

            if not correct_answers and answer:
                correct_answers = [answer]

            extracted.append({
                "question": question_text,
                "options": options,
                "correct_answer": answer,
                "correct_answer_text": correct_answers,
                "explanation": item.get("answer_description", "") or "",
                "question_images": item.get("question_images", []),
                "answer_images": item.get("answer_images", []),
                "source_file": html_file.name,
                "source_id": item.get("id"),
            })

        print(f"READ: {html_file.name} -> {len(extracted)} questions")
        return extracted

    except (OSError, json.JSONDecodeError, AttributeError, TypeError) as error:
        print(f"ERROR: {html_file.name}: {error}")
        return []


def normalize_question(text):
    """Normalize whitespace for duplicate detection."""
    return re.sub(r"\s+", " ", text).strip().casefold()


def main():
    # Read source pages from saved_pages/, not the project root.
    if not SAVED_PAGES_DIR.is_dir():
        raise SystemExit(
            f"Saved pages folder not found: {SAVED_PAGES_DIR}"
        )

    source_files = sorted(
        [
            path
            for path in SAVED_PAGES_DIR.glob("*.html")
            if re.search(
                r"Google\s*-\s*Professional Data Engineer\s*-\s*Page\s+\d+",
                path.name,
                re.IGNORECASE,
            )
        ],
        key=page_number,
    )

    if not source_files:
        raise SystemExit(
            f"No saved ExamPrepper pages found in: {SAVED_PAGES_DIR}"
        )

    print(f"Found {len(source_files)} source pages.\n")

    all_questions = []
    seen_questions = set()
    duplicates = 0

    for source_file in source_files:
        page_questions = extract_questions(source_file)

        for question in page_questions:
            key = normalize_question(question["question"])

            if key in seen_questions:
                duplicates += 1
                print(
                    "DUPLICATE SKIPPED:",
                    question["question"][:100],
                )
                continue

            seen_questions.add(key)
            all_questions.append(question)

    # Do not overwrite existing data if extraction produced no questions.
    if not all_questions:
        raise SystemExit(
            "No questions extracted. Existing questions.json was not changed."
        )

    OUTPUT_FILE.write_text(
        json.dumps(all_questions, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\nExtraction finished.")
    print(f"Source pages: {len(source_files)}")
    print(f"Unique questions: {len(all_questions)}")
    print(f"Duplicate records skipped: {duplicates}")
    print(f"JSON saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
