
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent
SAVED_PAGES_DIR = BASE_DIR / "saved_pages"


def page_number(path):
    match = re.search(r"Page (\d+)", path.name)
    return int(match.group(1)) if match else 0


pages = sorted(
    SAVED_PAGES_DIR.glob(
        "Google - Professional Data Engineer - Page * _ Examprepper.html"
    ),
    key=page_number,
)

if not pages:
    raise SystemExit(f"No saved HTML pages found in: {SAVED_PAGES_DIR}")

seen = {}
duplicates = 0
total = 0

for page in pages:
    with page.open("r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")

    script = soup.find("script", id="__NEXT_DATA__")
    if not script or not script.string:
        print(f"WARNING: No question data: {page.name}")
        continue

    data = json.loads(script.string)
    questions = data["props"]["pageProps"]["questions"]
    page_duplicates = 0

    for question in questions:
        text = " ".join(
            question.get("question_text", "").split()
        ).casefold()

        total += 1

        if text in seen:
            duplicates += 1
            page_duplicates += 1
        else:
            seen[text] = page.name

    print(
        f"Page {page_number(page):2}: "
        f"{len(questions)} questions, "
        f"{page_duplicates} duplicates"
    )

print("\n--- SUMMARY ---")
print(f"Pages checked: {len(pages)}")
print(f"Total records: {total}")
print(f"Unique questions: {len(seen)}")
print(f"Duplicate records: {duplicates}")
