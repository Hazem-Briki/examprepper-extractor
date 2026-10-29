# Exam Question Extraction and Study Automation Tool

A Python-based tool that extracts exam questions from saved HTML pages, converts them into structured JSON, detects duplicate questions, and generates interactive HTML study pages for exam preparation.

## Features

- Extract question data from saved HTML pages using BeautifulSoup.
- Convert extracted questions into a structured JSON dataset.
- Detect duplicate questions.
- Generate a static study page that preserves question order and sorts answer options alphabetically.
- Generate a randomized study page that shuffles questions and answer options.
- Show or hide answers using interactive buttons.
- Highlight correct answers in green when answers are revealed.
- Display answer explanations and available question images.
- Generate additional study pages in batches of 20 questions when the dataset contains more than 20 questions.
- Automate the complete workflow using a single Python script.
- Open the full static and randomized study pages automatically in Brave Browser.

## Technologies

- Python 3
- BeautifulSoup 4
- JSON and regular expressions
- HTML, CSS, and JavaScript
- Git and GitHub

## Project Structure

```text
examprepper-extractor/
├── saved_pages/          # Saved source HTML pages
├── main.py               # Runs the complete workflow
├── html_to_json.py       # Extracts questions into JSON
├── check_duplicates.py   # Detects duplicate questions
├── generate_static.py    # Generates static study pages
├── generate_random.py    # Generates randomized study pages
├── requirements.txt      # Python dependencies
├── .gitignore
└── README.md
```

Generated files include:

- `questions.json` — extracted question dataset.
- `questions_static.html` — full static study page.
- `questions_random.html` — full randomized study page.
- `static_pages/` — static batches when there are more than 20 questions.
- `random_pages/` — randomized batches when there are more than 20 questions.

## Requirements

- Python 3
- Brave Browser, if you want the script to open the generated pages automatically.

Install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

## Usage

### 1. Prepare the source HTML files

Place your saved HTML pages inside the `saved_pages/` directory.

### 2. Run the workflow

From the project directory, execute:

```bash
python main.py
```

The script runs the following steps:

1. Extract questions from the saved HTML files.
2. Detect duplicate questions.
3. Generate the static study page.
4. Generate the randomized study page.
5. Open both full study pages in Brave Browser.

### 3. Study the questions

Open either generated HTML page.

- Select **Show Answer** to reveal the answer and explanation.
- Select **Hide Answer** to hide them again.
- Correct options are highlighted in green when revealed.
- Use **Shuffle Again** on the randomized page to reshuffle questions and answer options.

## Batch Generation

The batch size is 20 questions per page.

- **20 questions or fewer:** only the full static and randomized pages are generated.
- **More than 20 questions:** the full pages are generated along with additional static and randomized batch pages.

The static batches preserve question order. The randomized batches shuffle question and answer-option order.

## Version Control

The `.gitignore` file is configured to exclude saved source HTML files and generated study data and pages from version control by default. Review `.gitignore` before committing changes to ensure that only the intended project files are uploaded to GitHub.

## Responsible Use

Use only exam content you are authorized to access and store. Respect the website's terms and applicable copyright restrictions, especially when sharing extracted questions or redistributing them publicly.

This project is intended for personal study and educational purposes.
