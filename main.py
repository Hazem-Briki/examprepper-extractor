
import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    ("1/4 - Extract HTML pages and generate JSON", "html_to_json.py"),
    ("2/4 - Check duplicate questions", "check_duplicates.py"),
    ("3/4 - Generate static HTML", "generate_static.py"),
    ("4/4 - Generate random HTML", "generate_random.py"),
]

HTML_FILES = [
    "questions_static.html",
    "questions_random.html",
]


def run_script(script_name, description):
    script_path = PROJECT_DIR / script_name

    if not script_path.exists():
        raise FileNotFoundError(
            f"Required script not found: {script_path}"
        )

    print(f"\n{'=' * 60}")
    print(description)
    print(f"{'=' * 60}")

    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_DIR,
        check=True,
    )

    print(f"Completed: {script_name}")


def find_brave():
    possible_paths = [
        Path(sys.environ["PROGRAMFILES"]) / "BraveSoftware"
        / "Brave-Browser" / "Application" / "brave.exe"
        if hasattr(sys, "environ") else None,
        Path.home() / "AppData" / "Local" / "BraveSoftware"
        / "Brave-Browser" / "Application" / "brave.exe",
    ]

    # Also check the usual Program Files location.
    possible_paths.append(
        Path("C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe")
    )

    for path in possible_paths:
        if path and path.exists():
            return path

    return None


def open_html_files():
    brave_path = find_brave()

    if not brave_path:
        raise FileNotFoundError(
            "Brave was not found in its usual installation folders."
        )

    for filename in HTML_FILES:
        html_path = PROJECT_DIR / filename

        if not html_path.exists():
            raise FileNotFoundError(
                f"Generated HTML file not found: {html_path}"
            )

        subprocess.Popen([str(brave_path), str(html_path)])
        print(f"Opened in Brave: {filename}")


def main():
    print("EXAM QUESTION EXTRACTION WORKFLOW")
    print(f"Project folder: {PROJECT_DIR}")

    try:
        for description, script_name in SCRIPTS:
            run_script(script_name, description)

        print("\nAll generation steps completed successfully.")

        open_html_files()

        print("\nWorkflow completed successfully!")

    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        print(f"\nWorkflow stopped: {error}")
        print("Fix the error before running the workflow again.")
        sys.exit(1)


if __name__ == "__main__":
    main()