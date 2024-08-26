#Tool  for Advanced Crawling
import requests
from bs4 import BeautifulSoup
import tldextract
import argparse
from urllib.parse import urlparse, parse_qs, urljoin

# Banner and version information
banner = r"""
  ___      _       _____                    _ 
 / _ \    | |     /  __ \                  | |
/ /_\ \ __| |_   _| /  \/_ __ __ ___      _| |
|  _  |/ _` \ \ / / |   | '__/ _` \ \ /\ / / |
| | | | (_| |\ V /| \__/\ | | (_| |\ V  V /| |
\_| |_/\__,_| \_/  \____/_|  \__,_| \_/\_/ |_| 
                     Version: 1.0
                     Author: G4UR4V007
"""

def extract_parameters(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return list(query_params.keys())

def crawl_domain(domain, max_pages=100):
    visited = set()
    to_crawl = [(f"https://{domain}", "/")]
    parameters = set()

    while to_crawl and len(visited) < max_pages:
        url, path = to_crawl.pop(0)
        full_url = urljoin(url, path)  # Use urljoin to construct the full URL

        print(f"Crawling: {full_url}")  # Debug output

        try:
            response = requests.get(full_url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error accessing {full_url}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)

        for link in links:
            href = link["href"]
            # Ensure href is a valid URL
            if href.startswith("http://") or href.startswith("https://"):
                extracted = tldextract.extract(href)
                # Check if the extracted domain matches the target domain
                if extracted.domain == domain and href not in visited:
                    print(f"Found link: {href}")  # Debug output
                    to_crawl.append((extracted.domain, extracted.path))
                    visited.add(href)
            elif href.startswith("//"):  # Relative URL with leading double slash
                href = f"https:{href}"  # Prepend https for protocol-relative URLs
                if href not in visited:
                    print(f"Found link: {href}")  # Debug output
                    to_crawl.append((domain, urljoin(url, href)))
                    visited.add(href)
            elif href.startswith("/"):  # Relative URL
                href = urljoin(url, href)  # Use urljoin for relative URLs
                if href not in visited:
                    print(f"Found link: {href}")  # Debug output
                    to_crawl.append((domain, href))
                    visited.add(href)

        params = extract_parameters(full_url)
        if params:
            parameters.update(params)

    return parameters

if __name__ == "__main__":
    print(banner)
    
    parser = argparse.ArgumentParser(description="Crawl URL parameters from a given domain.")
    parser.add_argument("domain", help="The domain to crawl.")
    parser.add_argument("--max-pages", type=int, default=100, help="Maximum number of pages to crawl.")

    args = parser.parse_args()

    parameters = crawl_domain(args.domain, args.max_pages)

    print(f"\nFound {len(parameters)} unique parameters:")
    for param in parameters:
        print(param)