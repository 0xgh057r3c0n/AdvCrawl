import requests
from bs4 import BeautifulSoup
import tldextract
import argparse
import random
from urllib.parse import urlparse, parse_qs, urljoin
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Color palette for random output (excluding RESET/BLACK for visibility)
COLOR_PALETTE = [
    Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE,
    Fore.MAGENTA, Fore.CYAN, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX,
    Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX
]

# Fixed color banner
banner = f"""
{Fore.LIGHTCYAN_EX}
  ___      _       _____                    _ 
 / _ \\    | |     /  __ \\                  | |
/ /_\\ \\ __| |_   _| /  \\/_ __ __ ___      _| |
|  _  |/ _` \\ \\ / / |   | '__/ _` \\ \\ /\\ / / |
| | | | (_| |\\ V /| \\__/\\ | | (_| |\\ V  V /| |
\\_| |_/\\__,_| \\_/  \\____/_|  \\__,_| \\_/\\_/ |_|
                     Version: 1.0
                     Author: G4UR4V007
{Style.RESET_ALL}
"""

def random_color(text):
    return f"{random.choice(COLOR_PALETTE)}{text}{Style.RESET_ALL}"

def extract_parameters(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return list(query_params.keys())

def crawl_domain(domain, max_pages=100):
    visited = set()
    to_crawl = [f"https://{domain}"]
    parameters = set()

    target = tldextract.extract(domain)
    target_domain = f"{target.domain}.{target.suffix}"

    while to_crawl and len(visited) < max_pages:
        full_url = to_crawl.pop(0)

        if full_url in visited:
            continue

        print(random_color(f"[+] Crawling: {full_url}"))
        visited.add(full_url)

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; AdvancedCrawler/1.0)"
            }
            response = requests.get(full_url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(random_color(f"[!] Error accessing {full_url}: {e}"))
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)

        for link in links:
            href = urljoin(full_url, link["href"])
            extracted = tldextract.extract(href)
            href_domain = f"{extracted.domain}.{extracted.suffix}"

            if href_domain == target_domain and href not in visited:
                print(random_color(f"[+] Found link: {href}"))
                to_crawl.append(href)

        # Extract parameters from current page
        params = extract_parameters(full_url)
        if params:
            for param in params:
                parameters.add(param)

    return parameters

if __name__ == "__main__":
    print(banner)

    parser = argparse.ArgumentParser(description="Crawl URL parameters from a given domain.")
    parser.add_argument("domain", help="The domain to crawl.")
    parser.add_argument("--max-pages", type=int, default=100, help="Maximum number of pages to crawl.")
    args = parser.parse_args()

    parameters = crawl_domain(args.domain, args.max_pages)

    print(random_color(f"\n[+] Found {len(parameters)} unique parameter(s):"))
    for param in parameters:
        print(random_color(f" - {param}"))
    print(random_color("[+] Crawling Complete!"))
