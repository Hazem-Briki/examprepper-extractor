# Exam Question Extraction and Study Automation Tool

A Python-based tool that extracts exam questions from saved HTML pages, converts them into structured JSON, detects duplicate questions, and generates interactive HTML study pages for exam preparation.

## Features

- Extract question data from saved HTML pages using BeautifulSoup.
- Convert extracted questions into a structured JSON dataset.
- Detect duplicate questions.
- Generate static study pages that preserve question order and sort answer options alphabetically.
- Generate randomized study pages that shuffle questions and answer options.
- Generate cumulative progressive random pages for extended practice.
- Show or hide answers using interactive buttons.
- Highlight correct answers in green when answers are revealed.
- Display answer explanations and available question images.
- Generate study pages in batches of 20 questions.
- Generate cumulative pages containing progressively larger question sets.
- Include a Back to Top button on study pages.
- Automate the complete workflow using a single Python script.
- Open the full study pages and first batch pages automatically in Brave Browser.

## Technologies

- Python 3
- BeautifulSoup 4
- JSON and regular expressions
- HTML, CSS, and JavaScript
- Git and GitHub

## Project Structure

```text
examprepper-extractor/
├── saved_pages/                  # Saved source HTML pages
├── exam_pages/                   # Generated batch study pages
│   ├── page_01/
│   │   ├── p_01_static.html
│   │   └── p_01_random.html
│   ├── page_02/
│   │   ├── p_02_static.html
│   │   ├── p_02_random.html
│   │   └── p_02_progressive.html
│   ├── ...
│   └── page_16/
│       ├── p_16_static.html
│       ├── p_16_random.html
│       └── p_16_progressive.html
├── main.py                       # Runs the complete workflow
├── html_to_json.py               # Extracts questions into JSON
├── check_duplicates.py           # Detects duplicate questions
├── generate_static.py            # Generates static study pages
├── generate_random.py            # Generates randomized study pages
├── generate_progressive_random.py # Generates cumulative random pages
├── requirements.txt              # Python dependencies
├── .gitignore
└── README.md
```

### Main generated files

- `questions.json` — extracted question dataset.
- `questions_static.html` — complete static study page.
- `questions_random.html` — complete randomized study page.
- `exam_pages/` — contains all generated batch study pages.

## Requirements

- Python 3
- Brave Browser, if you want the script to open generated pages automatically.

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

1. Extract questions from the saved HTML files and generate JSON.
2. Detect duplicate questions.
3. Generate static study pages.
4. Generate randomized study pages.
5. Generate cumulative progressive random pages.

After successful generation, the script automatically opens the complete static and randomized pages, along with the first static and randomized batch pages, in Brave Browser.

### 3. Study the questions

Open any generated HTML study page.

- Select **Show Answer** to reveal the answer and explanation.
- Select **Hide Answer** to hide them again.
- Correct options are highlighted in green when revealed.
- Use **Shuffle Again** on randomized pages to reshuffle questions and answer options.
- Use the **Back to Top** button to return to the beginning of a page.

## Batch Generation

The batch size is 20 questions per page.

Three types of batch pages are generated:

### 1. Static pages

- Preserve the original question order.
- Preserve alphabetical answer-option order.
- Each page contains up to 20 questions.

### 2. Random pages

- Use the same question membership as the corresponding static batch.
- Shuffle the question order.
- Shuffle the answer-option order.
- Include a Shuffle Again button for additional randomization.

### 3. Progressive random pages

- Contain cumulative question sets.
- Start with the first 40 questions in `page_02`.
- Add another 20 questions with each subsequent page.
- Randomize the question order.
- The final page includes all available questions.

For example, with 319 questions:

| Folder | Static / Random | Progressive |
|---|---:|---:|
| `page_01` | 20 questions | — |
| `page_02` | 20 questions | 40 questions |
| `page_03` | 20 questions | 60 questions |
| `...` | `...` | `...` |
| `page_16` | 19 questions | 319 questions |

The final incomplete batch is generated with the remaining questions rather than discarded.

## Version Control

The `.gitignore` file is configured to exclude saved source HTML files and generated study data and pages from version control by default.

Review `.gitignore` before committing changes to ensure that only the intended project files are uploaded to GitHub.

## Responsible Use

Use only exam content you are authorized to access and store. Respect the website's terms and applicable copyright restrictions, especially when sharing extracted questions or redistributing them publicly.

This project is intended for personal study and educational purposes.