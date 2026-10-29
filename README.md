# Exam Question Extraction and Study Automation Tool

A Python-based tool that processes saved HTML pages, extracts exam questions, converts them into structured JSON, detects duplicates, and generates interactive HTML study pages.

## Features

- Extract question data from saved HTML pages using BeautifulSoup.
- Convert extracted content into structured JSON.
- Detect duplicate questions.
- Generate a static HTML study page with questions and options in alphabetical order.
- Generate a randomized HTML study page for practice.
- Reveal and hide answers, highlight correct options, and display explanations.
- Automate the entire workflow through a single Python script.
- Open the generated study pages in Brave automatically.

## Technologies

- Python
- BeautifulSoup
- JSON
- Regular expressions
- HTML, CSS, and JavaScript
- Git and GitHub

## Project Structure

```text
examprepper-extractor/
├── main.py
├── html_to_json.py
├── check_duplicates.py
├── generate_static.py
├── generate_random.py
├── .gitignore
└── README.md
```

## Requirements

- Python 3
- BeautifulSoup 4
- Brave Browser (for automatic browser launch)

Install the Python dependency:

```bash
python -m pip install beautifulsoup4
```

## Usage

1. Save the HTML pages you want to process in the project folder.
2. Run the workflow:

```bash
python main.py
```

3. The script extracts the questions, checks for duplicates, generates the static and randomized study pages, and opens them in Brave.

## Notes

The saved HTML pages, extracted question dataset, and generated study pages are excluded from version control by default. Use only content you have permission to access and redistribute.

This project is intended for personal study and educational purposes.