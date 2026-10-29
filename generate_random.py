
import json
import html
import re
from pathlib import Path


INPUT_FILE = Path("questions.json")
OUTPUT_FILE = Path("questions_random.html")


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


with INPUT_FILE.open("r", encoding="utf-8") as file:
    questions = json.load(file)


cards = []

for question in questions:
    answer = str(question.get("correct_answer", "")).strip().upper()
    answer_letters = set(re.findall(r"[A-Z]", answer))

    options_html = []

    for option in question.get("options", []):
        # The JSON stores options such as "B. Serialization".
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

    correct_texts = [
        option.get("text", "")
        for option in []
    ]

    correct_answer_text = question.get("correct_answer_text", [])

    # Display the full correct answers because option letters are hidden.
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

    cards.append(f"""
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
    """)


document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Google Professional Data Engineer — Random Practice</title>

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
    margin: 12px 0;
  }}
</style>
</head>

<body>
<h1>Google Professional Data Engineer</h1>
<p class="summary">
  {len(questions)} questions · Random question order and random option order
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

// Randomize automatically whenever the page opens or refreshes.
shuffleAll();
</script>
</body>
</html>
"""

OUTPUT_FILE.write_text(document, encoding="utf-8")

print(f"Generated: {OUTPUT_FILE.resolve()}")
print(f"Questions included: {len(questions)}")
print("Questions and options will shuffle on every refresh.")