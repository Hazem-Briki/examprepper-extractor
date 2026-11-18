
import json
from pathlib import Path
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent
SAVED_PAGES_DIR = BASE_DIR / "saved_pages"


pages = sorted(
    SAVED_PAGES_DIR.glob(
        "Google - Professional Data Engineer - Page * _ Examprepper.html"
    ),
    key=lambda p: int(p.name.split("Page ")[1].split(" ")[0])
)

print(f"Found {len(pages)} pages.")

if len(pages) == 0:
    print("No HTML pages found in saved_pages.")
    raise SystemExit(1)

# Inspect the first three pages and the last page.
pages_to_inspect = pages[:3]

if len(pages) > 3:
    pages_to_inspect.append(pages[-1])

for page in pages_to_inspect:
    with page.open("r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")

    script = soup.find("script", id="__NEXT_DATA__")

    if script is None or not script.string:
        print(f"\nCould not find __NEXT_DATA__ in {page.name}")
        continue

    data = json.loads(script.string)
    questions = data["props"]["pageProps"]["questions"]

    print(f"\n--- {page.name} ---")

    for index, question in enumerate(questions, start=1):
        text = question.get("question_text", "")
        print(f"{index}. {text[:180]}")
