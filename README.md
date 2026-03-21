# LinkedIn Executive Lead Generator (Python/Selenium)

A professional automation tool designed to find LinkedIn profiles of company executives (CEO, Founder, Owner) using Google search dorks.

## ✨ Features
- **Smart  Search:** Combines multiple executive titles (CEO OR Founder OR Owner) for better results.
- **Bot-Detection Bypass:** Implemented custom User-Agents and Javascript manipulation to avoid being flagged as a bot.
- **Adaptive Delays:** Uses randomized sleep intervals to mimic human behavior and prevent IP blocks.
- **Data Integrity:** Automatically parses and cleans names and job titles before exporting to CSV.

## 🛠 Tech Stack
- **Language:** Python 3
- **Automation:** Selenium WebDriver
- **Package Management:** ChromeDriverManager

## 🚀 How to use
1. Add company names to `companies.txt`.
2. Run `example.py`.
3. Results will be saved in `ceos_with_links.csv`.
   [demo_screenshot_before](demo_screenshot_before.png)
