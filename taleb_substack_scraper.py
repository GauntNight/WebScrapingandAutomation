"""
Substack Scraper for Nassim Taleb's Articles
Scrapes all articles from nntaleb's Substack
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import re

class SubstackScraper:
    def __init__(self, author_username):
        self.author_username = author_username
        self.base_url = f"https://{author_username}.substack.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.articles = []

    def get_archive_page(self):
        """Fetch the archive page with all posts"""
        archive_url = f"{self.base_url}/archive?sort=new"
        print(f"Fetching archive from: {archive_url}")

        try:
            response = requests.get(archive_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching archive: {e}")
            return None

    def extract_article_links(self, html_content):
        """Extract all article links from the archive page"""
        soup = BeautifulSoup(html_content, 'lxml')
        article_links = []

        # Find all article links (Substack uses different patterns)
        # Looking for links that point to posts
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Match Substack post URLs
            if '/p/' in href and self.author_username in href:
                if href not in article_links:
                    article_links.append(href)
            # Also check for relative URLs
            elif href.startswith('/p/'):
                full_url = self.base_url + href
                if full_url not in article_links:
                    article_links.append(full_url)

        print(f"Found {len(article_links)} article links")
        return article_links

    def scrape_article(self, url):
        """Scrape a single article"""
        print(f"Scraping: {url}")

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

            # Extract article data
            article_data = {
                'url': url,
                'title': '',
                'date': '',
                'content': '',
                'subtitle': ''
            }

            # Title - multiple possible selectors
            title_elem = soup.find('h1', class_='post-title') or \
                        soup.find('h1', class_='heading') or \
                        soup.find('h1')
            if title_elem:
                article_data['title'] = title_elem.get_text(strip=True)

            # Subtitle
            subtitle_elem = soup.find('h3', class_='subtitle')
            if subtitle_elem:
                article_data['subtitle'] = subtitle_elem.get_text(strip=True)

            # Date - try multiple selectors
            date_elem = soup.find('time') or \
                       soup.find('span', class_='post-date')
            if date_elem:
                date_text = date_elem.get('datetime') or date_elem.get_text(strip=True)
                article_data['date'] = date_text

            # Content - get the main article body
            # Substack typically uses class 'body' or 'available-content'
            content_elem = soup.find('div', class_='available-content') or \
                          soup.find('div', class_='body') or \
                          soup.find('article')

            if content_elem:
                # Get all paragraphs
                paragraphs = content_elem.find_all('p')
                article_data['content'] = '\n\n'.join([p.get_text(strip=True) for p in paragraphs])

            # If no content found, try alternative approach
            if not article_data['content']:
                # Get all text content from the page
                body = soup.find('body')
                if body:
                    # Filter out scripts, styles, etc.
                    for script in body(["script", "style", "nav", "footer", "header"]):
                        script.decompose()
                    article_data['content'] = body.get_text(separator='\n', strip=True)

            return article_data

        except requests.exceptions.RequestException as e:
            print(f"Error scraping article {url}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error scraping {url}: {e}")
            return None

    def scrape_all_articles(self, max_articles=None):
        """Scrape all articles from the Substack"""
        # Get archive page
        archive_html = self.get_archive_page()
        if not archive_html:
            print("Failed to fetch archive page")
            return []

        # Extract article links
        article_links = self.extract_article_links(archive_html)

        if max_articles:
            article_links = article_links[:max_articles]

        # Scrape each article
        for i, link in enumerate(article_links, 1):
            print(f"\nProcessing article {i}/{len(article_links)}")
            article_data = self.scrape_article(link)

            if article_data:
                self.articles.append(article_data)

            # Be respectful - wait between requests
            if i < len(article_links):
                time.sleep(2)  # 2 second delay between requests

        return self.articles

    def save_to_json(self, filename='taleb_articles.json'):
        """Save scraped articles to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.articles, f, indent=2, ensure_ascii=False)
        print(f"\nSaved {len(self.articles)} articles to {filename}")

    def get_article_count(self):
        """Return the number of articles scraped"""
        return len(self.articles)


def main():
    print("=" * 60)
    print("Nassim Taleb Substack Scraper")
    print("=" * 60)

    # Initialize scraper
    scraper = SubstackScraper('nntaleb')

    # Scrape all articles (remove max_articles parameter to get all)
    articles = scraper.scrape_all_articles()

    # Save to JSON
    scraper.save_to_json('taleb_articles.json')

    # Print summary
    print("\n" + "=" * 60)
    print(f"Scraping complete!")
    print(f"Total articles scraped: {scraper.get_article_count()}")
    print("=" * 60)

    # Show sample of first article
    if articles:
        print("\nSample - First Article:")
        print(f"Title: {articles[0].get('title', 'N/A')}")
        print(f"Date: {articles[0].get('date', 'N/A')}")
        print(f"Content preview: {articles[0].get('content', '')[:200]}...")


if __name__ == "__main__":
    main()
