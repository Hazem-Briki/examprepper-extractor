
import json
import random
from pathlib import Path

import generate_random


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "questions.json"
OUTPUT_DIR = BASE_DIR / "progressive_random_pages"

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

    if total_questions == 0:
        print("No questions found in questions.json.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    page_count = 0

    # Generate cumulative pages: 20, 40, 60, ... until all questions.
    for target_count in range(
        BATCH_SIZE,
        total_questions + BATCH_SIZE,
        BATCH_SIZE,
    ):
        target_count = min(target_count, total_questions)

        # Each page contains all questions from question 1 onward.
        page_questions = questions[:target_count].copy()

        # Randomize question order without changing the source JSON.
        random.shuffle(page_questions)

        page_count += 1

        output_file = OUTPUT_DIR / (
            f"questions_random_{page_count:03d}.html"
        )

        document = generate_random.render_document(
            page_questions,
            "Google Professional Data Engineer — "
            f"Progressive Random Practice (1–{target_count})",
            f"{target_count} cumulative questions · Random order",
        )

        output_file.write_text(document, encoding="utf-8")

        print(
            f"Created: {output_file.relative_to(BASE_DIR)} "
            f"({target_count}/{total_questions} questions)"
        )

        if target_count == total_questions:
            break

    print("\nProgressive random generation completed!")
    print(f"Total questions: {total_questions}")
    print(f"Pages generated: {page_count}")
    print(f"Output folder: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
