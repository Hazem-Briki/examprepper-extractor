
import json
import re
import html
from pathlib import Path
from bs4 import BeautifulSoup

BATCH_SIZE = 20

BASE_DIR = Path(__file__).resolve().parent
SAVED_PAGES_DIR = BASE_DIR / "saved_pages"
OUTPUT_FILE = BASE_DIR / "questions_static.html"
BATCH_DIR = BASE_DIR / "static_pages"


def page_number(path):
    match = re.search(r"Page (\d+)", path.name)
    return int(match.group(1)) if match else 0


def normalize_question(text):
    return " ".join(text.split()).casefold()


def escape(value):
    return html.escape(str(value), quote=True)


def render_images(images):
    result = []

    for image in images or []:
        if isinstance(image, str):
            url = image
        elif isinstance(image, dict):
            url = image.get("url") or image.get("src") or ""
        else:
            continue

        if url.startswith(("https://", "http://")):
            result.append(
                f'<img class="question-image" src="{escape(url)}" '
                f'alt="Question image" loading="lazy">'
            )

    return "\n".join(result)


def load_questions():
    pages = sorted(
        SAVED_PAGES_DIR.glob(
            "Google - Professional Data Engineer - Page * _ Examprepper.html"
        ),
        key=page_number,
    )

    if not pages:
        raise SystemExit(
            f"No saved HTML pages found in: {SAVED_PAGES_DIR}"
        )

    questions = []
    seen = set()

    for page in pages:
        with page.open("r", encoding="utf-8") as file:
            soup = BeautifulSoup(file.read(), "html.parser")

        script = soup.find("script", id="__NEXT_DATA__")

        if not script or not script.string:
            print(f"WARNING: No question data in {page.name}")
            continue

        data = json.loads(script.string)
        page_questions = data["props"]["pageProps"]["questions"]

        for item in page_questions:
            question_text = item.get("question_text", "").strip()
            key = normalize_question(question_text)

            if not question_text or key in seen:
                continue

            seen.add(key)

            choices = item.get("choices", {})

            if isinstance(choices, dict):
                options = sorted(
                    choices.items(),
                    key=lambda option: option[0],
                )
            else:
                options = []

                for option in choices:
                    match = re.match(
                        r"^\s*([A-Z])\.\s*(.*)",
                        option,
                        re.S,
                    )

                    if match:
                        options.append(
                            (match.group(1), match.group(2))
                        )

                options.sort(key=lambda option: option[0])

            questions.append({
                "number": len(questions) + 1,
                "question": question_text,
                "options": options,
                "answer": str(item.get("answer", "")).strip().upper(),
                "explanation": item.get("answer_description", "") or "",
                "question_images": item.get("question_images", []),
                "answer_images": item.get("answer_images", []),
            })

    if not questions:
        raise SystemExit("No questions were extracted from the saved pages.")

    return questions


def render_document(questions, title):
    cards = []

    for question in questions:
        number = question["number"]
        answer_letters = set(re.findall(r"[A-Z]", question["answer"]))

        options_html = []

        for letter, option_text in question["options"]:
            is_correct = letter in answer_letters

            options_html.append(
                f'<li class="option" data-letter="{escape(letter)}" '
                f'data-correct="{str(is_correct).lower()}">'
                f'<span class="option-letter">{escape(letter)}.</span> '
                f'{escape(option_text)}'
                f'</li>'
            )

        explanation_html = (
            f'<div class="explanation">'
            f'{escape(question["explanation"])}</div>'
            if question["explanation"]
            else '<div class="explanation">No explanation available.</div>'
        )

        cards.append(f"""
        <article class="question-card">
          <h2>Question {number}</h2>
          <div class="question-text">{escape(question["question"])}</div>
          {render_images(question["question_images"])}
          <ol class="options">{''.join(options_html)}</ol>
          <button class="answer-button" type="button"
                  aria-expanded="false">Show Answer</button>
          <div class="answer-panel" hidden>
            <p><strong>Correct answer:</strong> {escape(question["answer"])}</p>
            {explanation_html}
            {render_images(question["answer_images"])}
          </div>
        </article>
        """)

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<style>
  body {{
    font-family: Arial, sans-serif;
    line-height: 1.6;
    max-width: 1000px;
    margin: 0 auto;
    padding: 24px;
    background: #f5f7fa;
    color: #202124;
  }}
  h1 {{ line-height: 1.3; }}
  .summary {{ color: #5f6368; margin-bottom: 24px; }}
  .question-card {{
    background: white;
    border: 1px solid #dadce0;
    border-radius: 10px;
    padding: 22px;
    margin-bottom: 22px;
  }}
  .question-card h2 {{ font-size: 1.15rem; margin-top: 0; }}
  .question-text {{ white-space: pre-wrap; margin-bottom: 16px; }}
  .options {{ list-style: none; padding: 0; margin: 0 0 18px; }}
  .option {{
    padding: 10px 12px;
    margin: 8px 0;
    border: 1px solid #dadce0;
    border-radius: 6px;
    white-space: pre-wrap;
  }}
  .option-letter {{ font-weight: bold; }}
  .option.correct {{
    background: #e6f4ea;
    border-color: #188038;
    color: #137333;
  }}
  .answer-button {{
    padding: 10px 16px;
    border: 0;
    border-radius: 6px;
    background: #1a73e8;
    color: white;
    font-size: 0.95rem;
    cursor: pointer;
  }}
  .answer-panel {{
    margin-top: 16px;
    padding: 14px;
    background: #f8f9fa;
    border-radius: 6px;
  }}
  .explanation {{ white-space: pre-wrap; }}
  .question-image {{ display: block; max-width: 100%; margin: 12px 0; }}
  @media print {{
    body {{ background: white; }}
    .question-card {{ break-inside: avoid; }}
    .answer-button {{ display: none; }}
  }}
</style>
</head>
<body>
<h1>{escape(title)}</h1>
<p class="summary">{len(questions)} questions · Original question order and alphabetical option order</p>
{''.join(cards)}
<script>
document.querySelectorAll(".answer-button").forEach(button => {{
  button.addEventListener("click", () => {{
    const card = button.closest(".question-card");
    const panel = card.querySelector(".answer-panel");
    const showing = button.getAttribute("aria-expanded") === "true";

    button.setAttribute("aria-expanded", String(!showing));
    button.textContent = showing ? "Show Answer" : "Hide Answer";
    panel.hidden = showing;

    card.querySelectorAll(".option").forEach(option => {{
      option.classList.toggle(
        "correct",
        !showing && option.dataset.correct === "true"
      );
    }});
  }});
}});
</script>
</body>
</html>
"""

    return document


def remove_old_batches():
    if BATCH_DIR.exists():
        for file in BATCH_DIR.glob("questions_static_*.html"):
            file.unlink()


def main():
    questions = load_questions()

    # Always generate the complete question page in the project root.
    full_document = render_document(
        questions,
        "Google Professional Data Engineer — All Questions",
    )
    OUTPUT_FILE.write_text(full_document, encoding="utf-8")

    print(f"Generated full page: {OUTPUT_FILE}")
    print(f"Questions included: {len(questions)}")

    # Remove old batch files before generating the current set.
    remove_old_batches()

    if len(questions) > BATCH_SIZE:
        BATCH_DIR.mkdir(parents=True, exist_ok=True)

        for start in range(0, len(questions), BATCH_SIZE):
            batch_number = (start // BATCH_SIZE) + 1
            batch = questions[start:start + BATCH_SIZE]

            batch_file = BATCH_DIR / (
                f"questions_static_{batch_number:03d}.html"
            )

            batch_document = render_document(
                batch,
                f"Google Professional Data Engineer — "
                f"Static Batch {batch_number:03d}",
            )

            batch_file.write_text(batch_document, encoding="utf-8")

            print(
                f"Generated batch: {batch_file.relative_to(BASE_DIR)} "
                f"({len(batch)} questions)"
            )

        print(f"Static batches created: {BATCH_DIR}")
    else:
        print(
            f"Only {len(questions)} questions found. "
            "No static batch pages needed."
        )


if __name__ == "__main__":
    main()
