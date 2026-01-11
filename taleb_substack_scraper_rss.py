"""
Substack Scraper for Nassim Taleb's Articles (RSS Feed Approach)
Uses RSS feed to get article list, then scrapes individual articles
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import xml.etree.ElementTree as ET

class SubstackRSSScraper:
    def __init__(self, author_username):
        self.author_username = author_username
        self.base_url = f"https://{author_username}.substack.com"
        self.rss_url = f"{self.base_url}/feed"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        self.articles = []

    def get_rss_feed(self):
        """Fetch the RSS feed"""
        print(f"Fetching RSS feed from: {self.rss_url}")

        try:
            response = requests.get(self.rss_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching RSS feed: {e}")
            return None

    def parse_rss_feed(self, rss_content):
        """Parse RSS feed and extract article information"""
        try:
            root = ET.fromstring(rss_content)
            items = []

            # RSS feeds use different namespaces
            for item in root.findall('.//item'):
                article_info = {
                    'title': '',
                    'url': '',
                    'date': '',
                    'description': ''
                }

                # Extract title
                title_elem = item.find('title')
                if title_elem is not None:
                    article_info['title'] = title_elem.text or ''

                # Extract link
                link_elem = item.find('link')
                if link_elem is not None:
                    article_info['url'] = link_elem.text or ''

                # Extract publication date
                pubdate_elem = item.find('pubDate')
                if pubdate_elem is not None:
                    article_info['date'] = pubdate_elem.text or ''

                # Extract description/content
                description_elem = item.find('description')
                if description_elem is not None:
                    article_info['description'] = description_elem.text or ''

                # Also check for content:encoded (common in RSS)
                content_elem = item.find('{http://purl.org/rss/1.0/modules/content/}encoded')
                if content_elem is not None and content_elem.text:
                    article_info['description'] = content_elem.text

                items.append(article_info)

            print(f"Found {len(items)} articles in RSS feed")
            return items

        except ET.ParseError as e:
            print(f"Error parsing RSS feed: {e}")
            return []

    def scrape_article_content(self, url):
        """Scrape full article content from URL"""
        print(f"Scraping content from: {url}")

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

            # Try to find the main content
            content_elem = soup.find('div', class_='available-content') or \
                          soup.find('div', class_='body') or \
                          soup.find('article') or \
                          soup.find('div', class_='post-content')

            if content_elem:
                # Get all paragraphs
                paragraphs = content_elem.find_all('p')
                content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                return content

            return ""

        except requests.exceptions.RequestException as e:
            print(f"Error scraping article content: {e}")
            return ""

    def scrape_all_articles(self, max_articles=None, skip_full_content=False):
        """Scrape all articles from RSS feed"""
        # Get RSS feed
        rss_content = self.get_rss_feed()
        if not rss_content:
            print("Failed to fetch RSS feed")
            return []

        # Parse RSS feed
        articles_info = self.parse_rss_feed(rss_content)

        if max_articles:
            articles_info = articles_info[:max_articles]

        # Process each article
        for i, article_info in enumerate(articles_info, 1):
            print(f"\nProcessing article {i}/{len(articles_info)}")

            article_data = {
                'title': article_info['title'],
                'url': article_info['url'],
                'date': article_info['date'],
                'content': ''
            }

            # Get description from RSS (which might have some content)
            if article_info['description']:
                # Clean HTML from description
                desc_soup = BeautifulSoup(article_info['description'], 'lxml')
                article_data['content'] = desc_soup.get_text(separator='\n', strip=True)

            # Optionally scrape full content from article page
            if not skip_full_content and article_info['url']:
                full_content = self.scrape_article_content(article_info['url'])
                if full_content:
                    article_data['content'] = full_content

                # Be respectful - wait between requests
                if i < len(articles_info):
                    time.sleep(2)

            self.articles.append(article_data)

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
    print("Nassim Taleb Substack Scraper (RSS Feed)")
    print("=" * 60)

    # Initialize scraper
    scraper = SubstackRSSScraper('nntaleb')

    # Scrape articles
    # Set skip_full_content=True to only use RSS feed content (faster, avoids 403 errors)
    # Set skip_full_content=False to attempt to scrape full article content
    articles = scraper.scrape_all_articles(skip_full_content=True)

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
        print(f"URL: {articles[0].get('url', 'N/A')}")
        content_preview = articles[0].get('content', '')[:300]
        print(f"Content preview: {content_preview}...")
        print(f"Content length: {len(articles[0].get('content', ''))} characters")


if __name__ == "__main__":
    main()
