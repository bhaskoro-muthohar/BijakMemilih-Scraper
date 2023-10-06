# Web Scraping Project for Political Parties

## Introduction

This project aims to scrape data from various political parties' profiles. It uses Python, Selenium, and BeautifulSoup to scrape and parse data.

## Prerequisites

- Python 3.x
- Pandas
- Selenium
- BeautifulSoup
- ChromeDriver

## Installation

1. Clone this repository.
    ```bash
    git clone <repository_url>
    ```
    
2. Navigate to the project directory.
    ```bash
    cd <project_directory>
    ```
    
3. Install the required Python packages.
    ```bash
    pip install -r requirements.txt
    ```
   Note: Create a `requirements.txt` file with the following content if you haven't already:
    ```
    pandas
    selenium
    beautifulsoup4
    ```

## Usage

1. Add your data to `raw_data/partai_list.csv`.

2. Run the script.
    ```bash
    python <script_name>.py
    ```

3. The scraped data will be saved in `raw_data/scraped_data.csv`.

## Features

- Reads party profile links from a CSV file.
- Utilizes Selenium for browser automation to scroll and click on the page.
- Extracts relevant sections using CSS selectors.
- Saves the scraped data as a CSV file.

## Contributing

If you want to contribute to this project, please fork the repository and use a feature branch. Pull requests are warmly welcome.

---

Feel free to add or modify any sections as you see fit for your project. Save this content in a file named `README.md` at the root of your project directory.