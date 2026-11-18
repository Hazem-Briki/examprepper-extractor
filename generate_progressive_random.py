
import json
import random
from pathlib import Path

import generate_random


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "questions.json"
OUTPUT_DIR = BASE_DIR / "exam_pages"

BATCH_SIZE = 20


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {INPUT_FILE}. "
            "Run html_to_json.py first."
        )

    # Load the existing question data.
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        questions = json.load(file)

    if not isinstance(questions, list):
        raise ValueError(
            "questions.json must contain a JSON list of questions."
        )

    total_questions = len(questions)

    if total_questions <= BATCH_SIZE:
        print(
            "20 or fewer questions found. "
            "No progressive pages needed."
        )
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total_batches = (
        total_questions + BATCH_SIZE - 1
    ) // BATCH_SIZE

    page_count = 0

    # Start at page 2 because progressive pages begin with 40 questions.
    for batch_number in range(2, total_batches + 1):
        target_count = min(
            batch_number * BATCH_SIZE,
            total_questions,
        )

        # Each page contains all questions from question 1 onward.
        page_questions = questions[:target_count].copy()

        # Randomize question order without changing the source JSON.
        random.shuffle(page_questions)

        folder_name = f"page_{batch_number:02d}"
        file_name = f"p_{batch_number:02d}_progressive.html"

        batch_dir = OUTPUT_DIR / folder_name
        batch_dir.mkdir(parents=True, exist_ok=True)

        output_file = batch_dir / file_name

        document = generate_random.render_document(
            page_questions,
            "Google Professional Data Engineer — "
            f"Progressive Random Practice (1–{target_count})",
            f"{target_count} cumulative questions · Random order",
        )

        output_file.write_text(document, encoding="utf-8")

        page_count += 1

        print(
            f"Generated: {output_file.relative_to(BASE_DIR)} "
            f"({target_count}/{total_questions} questions)"
        )

    print("\nProgressive random generation completed!")
    print(f"Total questions: {total_questions}")
    print(f"Progressive pages created: {page_count}")
    print(f"Output folder: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
