
import json
import html
import re
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "questions.json"
OUTPUT_FILE = BASE_DIR / "questions_random.html"
BATCH_DIR = BASE_DIR / "random_pages"

BATCH_SIZE = 20


def escape(value):
    return html.escape(str(value or ""), quote=True)


def get_image_url(image):
    if isinstance(image, str):
        return image
    if isinstance(image, dict):
        return image.get("url") or image.get("src") or ""
    return ""


def render_images(images):
    result = []

    for image in images or []:
        url = get_image_url(image)

        if url.startswith(("https://", "http://")):
            result.append(
                f'<img class="question-image" src="{escape(url)}" '
                f'alt="Question image" loading="lazy">'
            )

    return "\n".join(result)


def render_question(question):
    answer = str(question.get("correct_answer", "")).strip().upper()
    answer_letters = set(re.findall(r"[A-Z]", answer))

    options_html = []

    for option in question.get("options", []):
        option = str(option)

        # Keep the original answer-matching logic.
        match = re.match(r"^\s*([A-Z])\.\s*(.*)", option, re.S)

        if match:
            letter = match.group(1)
            option_text = match.group(2)
        else:
            letter = ""
            option_text = option

        is_correct = letter in answer_letters

        options_html.append(
            f'<li class="option" data-correct="{str(is_correct).lower()}">'
            f'{escape(option_text)}'
            f'</li>'
        )

    correct_answer_text = question.get("correct_answer_text", [])

    if isinstance(correct_answer_text, str):
        correct_answer_text = [correct_answer_text]

    if correct_answer_text:
        answer_display = "; ".join(
            re.sub(r"^\s*[A-Z]\.\s*", "", str(item))
            for item in correct_answer_text
        )
    else:
        answer_display = "See the green-highlighted option(s)."

    explanation = question.get("explanation", "")

    explanation_html = (
        f'<div class="explanation">{escape(explanation)}</div>'
        if explanation
        else '<div class="explanation">No explanation available.</div>'
    )

    return f"""
    <article class="question-card">
      <div class="question-text">{escape(question.get("question", ""))}</div>
      {render_images(question.get("question_images", []))}
      <ul class="options">{''.join(options_html)}</ul>

      <button class="answer-button" type="button"
              aria-expanded="false">Show Answer</button>

      <div class="answer-panel" hidden>
        <p><strong>Correct answer:</strong> {escape(answer_display)}</p>
        {explanation_html}
        {render_images(question.get("answer_images", []))}
      </div>
    </article>
    """


def render_document(questions, title, description):
    cards = [render_question(question) for question in questions]

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

  .summary {{
    color: #5f6368;
    margin-bottom: 24px;
  }}

  .question-card {{
    background: white;
    border: 1px solid #dadce0;
    border-radius: 10px;
    padding: 22px;
    margin-bottom: 22px;
  }}

  .question-text {{
    white-space: pre-wrap;
    font-weight: 600;
    margin-bottom: 16px;
  }}

  .options {{
    list-style: none;
    padding: 0;
    margin: 0 0 18px;
  }}

  .option {{
    padding: 10px 12px;
    margin: 8px 0;
    border: 1px solid #dadce0;
    border-radius: 6px;
    white-space: pre-wrap;
  }}

  .option.correct {{
    background: #e6f4ea;
    border-color: #188038;
    color: #137333;
  }}

  .answer-button, .shuffle-button {{
    padding: 10px 16px;
    border: 0;
    border-radius: 6px;
    background: #1a73e8;
    color: white;
    font-size: 0.95rem;
    cursor: pointer;
    margin: 4px 6px 12px 0;
  }}

  .answer-panel {{
    margin-top: 12px;
    padding: 14px;
    background: #f8f9fa;
    border-radius: 6px;
  }}

  .explanation {{ white-space: pre-wrap; }}

  .question-image {{
    display: block;
    max-width: 100%;
    height: auto;
    margin: 12px 0;
  }}
</style>
</head>

<body>
<h1>{escape(title)}</h1>
<p class="summary">
  {len(questions)} questions · {escape(description)}
</p>

<button class="shuffle-button" id="shuffle-button" type="button">
  Shuffle Again
</button>

<div id="questions">
  {''.join(cards)}
</div>

<script>
function shuffleChildren(container) {{
  const items = Array.from(container.children);

  for (let i = items.length - 1; i > 0; i--) {{
    const j = Math.floor(Math.random() * (i + 1));
    [items[i], items[j]] = [items[j], items[i]];
  }}

  items.forEach(item => container.appendChild(item));
}}

function resetAnswers() {{
  document.querySelectorAll(".question-card").forEach(card => {{
    const button = card.querySelector(".answer-button");
    const panel = card.querySelector(".answer-panel");

    button.textContent = "Show Answer";
    button.setAttribute("aria-expanded", "false");
    panel.hidden = true;

    card.querySelectorAll(".option").forEach(option => {{
      option.classList.remove("correct");
    }});
  }});
}}

function shuffleAll() {{
  resetAnswers();

  const questions = document.getElementById("questions");
  shuffleChildren(questions);

  questions.querySelectorAll(".options").forEach(shuffleChildren);
}}

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

document.getElementById("shuffle-button").addEventListener("click", shuffleAll);

shuffleAll();
</script>
</body>
</html>
"""

    return document


def remove_old_batches():
    if BATCH_DIR.exists():
        for file in BATCH_DIR.glob("questions_random_*.html"):
            file.unlink()


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {INPUT_FILE}. Run html_to_json.py first."
        )

    with INPUT_FILE.open("r", encoding="utf-8") as file:
        questions = json.load(file)

    if not isinstance(questions, list):
        raise ValueError("questions.json must contain a JSON list of questions.")

    # Generate the complete page, preserving the original question set.
    full_document = render_document(
        questions,
        "Google Professional Data Engineer — Random Practice",
        "Random question order and random option order"
    )
    OUTPUT_FILE.write_text(full_document, encoding="utf-8")

    # Remove old batch files so outdated questions cannot remain.
    remove_old_batches()

    batch_count = 0

    if len(questions) > BATCH_SIZE:
        BATCH_DIR.mkdir(parents=True, exist_ok=True)

        # Randomize batch membership without adding or removing questions.
        shuffled_questions = questions.copy()
        random.shuffle(shuffled_questions)

        for start in range(0, len(shuffled_questions), BATCH_SIZE):
            batch_count += 1
            batch_questions = shuffled_questions[
                start:start + BATCH_SIZE
            ]

            batch_file = BATCH_DIR / (
                f"questions_random_{batch_count:03d}.html"
            )

            batch_document = render_document(
                batch_questions,
                f"Google Professional Data Engineer — Random Practice "
                f"(Batch {batch_count:03d})",
                f"Batch {batch_count:03d} · "
                f"{len(batch_questions)} questions · Random order"
            )

            batch_file.write_text(batch_document, encoding="utf-8")

    print(f"Generated full page: {OUTPUT_FILE.resolve()}")
    print(f"Questions included in full page: {len(questions)}")

    if batch_count:
        print(f"Generated batch pages: {batch_count}")
        print(f"Batch folder: {BATCH_DIR.resolve()}")
    else:
        print("20 or fewer questions: no batch pages generated.")


if __name__ == "__main__":
    main()
