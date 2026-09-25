# E-Commerce Test Automation Framework
### Selenium (Unittest + PyTest + POM) with API-Hybrid Enhancements

📄 **Project Report:** see `project-report/`
🖼️ **Output Screenshots:** see `screenshots/`
🎥 **Demo Video:** see `demo-video/` (add your recording or a link here)

A scalable Python test automation framework for the [Tutorials Ninja OpenCart Demo](https://tutorialsninja.com/demo/), built to demonstrate both fundamental (Unittest) and scalable (PyTest + POM) automation design, plus API-assisted testing patterns used in real-world hybrid frameworks.

---

## Why this design?

| Component | Why it's here |
|---|---|
| **Page Object Model (POM)** | Separates page structure/locators from test logic. If the UI changes, only the page class needs updating — tests stay untouched. |
| **Unittest suite** | Demonstrates core, dependency-free testing fundamentals (`setUp`/`tearDown`, `assert*`). |
| **PyTest suite** | Demonstrates scalable framework design — fixtures, `conftest.py`, `parametrize`, plugin ecosystem (`pytest-html`, `allure-pytest`). |
| **API-assisted setup** (`utils/api_client.py`) | Instead of repeating slow UI login for every test, we call the login flow via `requests` and inject the session where possible — a common pattern in hybrid frameworks to cut down flaky, repetitive UI steps. |
| **Standalone API suite** (`tests/api/`) | Shows the framework isn't UI-only — same fixtures/config/reporting power a pure API test suite against a public REST API. |
| **CSV test data** | Data-driven testing — same test logic runs against multiple data sets without code duplication. |
| **Screenshot on failure** | Immediate visual proof + debugging context when a test fails, captured automatically via a PyTest hook. |
| **Config management** | Base URL, browser choice, and credentials live in `config/config.ini` — never hardcoded, so the suite is portable across environments. |
| **Reporting (pytest-html / Allure)** | Human-readable execution reports for stakeholders, not just console output. |

---

## Project Structure

```
capstone2_framework/
├── config/config.ini
├── pages/              # Page Object classes
├── utils/              # Driver factory, screenshots, API client, logger
├── data/test_data.csv  # Data-driven test inputs
├── tests/
│   ├── unittest_suite/ # Core Unittest tests
│   ├── pytest_suite/   # PyTest + POM + fixtures
│   └── api/            # Standalone API tests (jsonplaceholder)
├── reports/            # Generated HTML/Allure reports
└── requirements.txt
```

---

## Setup

> Run all commands below from inside this `Folder 2 - Capstone Project/` directory.

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Chrome + matching ChromeDriver are handled automatically via `webdriver-manager`.

---

## Running the tests

**Unittest suite:**
```bash
python -m unittest discover -s tests/unittest_suite -v
```

**PyTest UI suite (with HTML report):**
```bash
pytest tests/pytest_suite --html=reports/report.html --self-contained-html -v
```

**PyTest API suite:**
```bash
pytest tests/api -v
```

**All PyTest tests with Allure:**
```bash
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results
```
> Allure requires the Allure commandline tool installed separately (`npm install -g allure-commandline` or via Scoop/Homebrew).

---

## Scenario Automated

1. Launch browser
2. Login (UI-based, and API-assisted variant)
3. Search product
4. Add product to cart
5. Verify cart (UI + API cross-check where applicable)
6. Screenshot on failure
7. Data-driven inputs from CSV
8. HTML / Allure execution report

---

## Notes

- Target application: `https://tutorialsninja.com/demo/` (public OpenCart demo — no real credentials/data used)
- API suite target: `https://jsonplaceholder.typicode.com/` (public fake REST API)
- This is a portfolio/learning project; no real user data or credentials are involved.


---


## Known Limitations

- `test_valid_login` depends on a real registered account existing on a shared public demo site, which could be reset without notice. Not auto-registering a fresh account in a fixture was a deliberate time tradeoff, not an oversight.
- Screenshot-on-failure in the Unittest suite relies on `TestCase._outcome`, a private/internal unittest attribute. It's verified working on the Python version this was tested on, but being a private API, it isn't guaranteed stable across all future Python versions the way the PyTest suite's public hook-based approach is.
