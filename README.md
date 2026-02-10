# Steam Price Checker

A simple Python automation project built with Selenium that checks the prices of a Steam game based on its store ID.

## What it does
- Opens a Steam game page in headless (invisible) browser mode
- Handles age-verification (age gate) when required
- Extracts prices for all available editions
- Validates expected behavior using assertions
- Prints the results to the console

## Technologies
- Python
- Selenium

## How to run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
2. Run the script:
    ```bash
    python main.py
    
## Executable version
- Built using PyInstaller
- Requires Google Chrome installed
- Tested on Windows
