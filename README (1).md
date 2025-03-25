# Playwright with Python and Pytest

This guide explains how to set up, use, and generate HTML reports using Playwright with Python and Pytest.

## Installation

### 1. Install Python (if not installed)
Ensure you have Python installed. You can check by running:
```sh
python --version
```
If not installed, download it from [python.org](https://www.python.org/downloads/).

### 2. Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate    # Windows
```

### 3. Install Required Dependencies
```sh
pip install pytest pytest-playwright pytest-html
```

### 4. Install Playwright Browsers
```sh
playwright install
```
This will download necessary browser binaries.

---

## Writing a Playwright Test
Create a test file, e.g., `test_example.py`:

```python
import pytest
from playwright.sync_api import sync_playwright


def test_google_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.google.com")
        assert "Google" in page.title()
        browser.close()
```

---

## Running Playwright Tests with Pytest

### Run All Tests
```sh
pytest
```


---

## Generating HTML Test Report

### Run Tests with HTML Report
```sh
pytest --html=report.html --self-contained-html
```

### Open Report
For Windows:
```sh
start report.html
```
For macOS:
```sh
open report.html
```
For Linux:
```sh
xdg-open report.html
```

---

## Debugging

### Run with Verbose Output
```sh
pytest -v
```

### Stop Execution on First Failure
```sh
pytest -x
```

## Conclusion
This guide helps you **set up Playwright with Python**, run tests using **Pytest**, and generate **detailed HTML reports**. Happy Testing! 🚀

