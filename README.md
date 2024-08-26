# URL Parameter Crawler

A simple Python tool to crawl a specified domain and extract URL parameters from the pages found. This tool can be useful for web scraping, SEO analysis, or understanding the structure of a website's URLs.

## Features

- Crawls a specified domain and extracts unique URL parameters.
- Handles both absolute and relative URLs.
- Outputs the number of unique parameters found.
- Debug output for tracking the crawling process.

## Requirements

This tool requires the following Python libraries:

- `requests`: For making HTTP requests.
- `beautifulsoup4`: For parsing HTML content.
- `tldextract`: For extracting the domain from URLs.

## Installation

1. Clone the repository or download the script.

2. Navigate to the directory containing the script.

3. Install the required libraries using pip. You can do this by running:

   ```bash
   pip install -r requirements.txt
   
## Uasge
python3 AdvCrawl.py example.com --max-pages 500
