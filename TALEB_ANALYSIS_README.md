# Nassim Taleb Substack Analysis Project

Complete web scraping and sentiment analysis pipeline for analyzing Nassim Taleb's Substack articles.

## Project Overview

This project scrapes articles from Nassim Taleb's Substack, performs comprehensive writing style analysis, conducts sentiment analysis (optimism/pessimism scoring), and visualizes the results over time.

## Files in This Project

### Scraping Scripts
- **`taleb_substack_scraper.py`** - Main scraper using direct HTTP requests
- **`taleb_substack_scraper_rss.py`** - Alternative scraper using RSS feed approach
- **`create_sample_data.py`** - Creates sample Taleb-style articles for testing

### Analysis Scripts
- **`analyze_taleb_articles.py`** - Complete analysis pipeline including:
  - Writing style analysis
  - Sentiment analysis (optimism/pessimism)
  - Visualization generation

### Data Files
- **`taleb_articles.json`** - Scraped articles in JSON format
- **`taleb_analysis_results.csv`** - Detailed analysis results
- **`taleb_sentiment_analysis.png`** - Sentiment visualization graph

## Requirements

Install required packages:
```bash
pip3 install requests beautifulsoup4 selenium pandas matplotlib vaderSentiment lxml
```

## Usage

### Option 1: Use Sample Data (No Network Required)
```bash
# Generate sample Taleb-style articles
python3 create_sample_data.py

# Run complete analysis
python3 analyze_taleb_articles.py
```

### Option 2: Scrape Real Articles (Requires Network Access)

Due to network restrictions in some environments, you may need to run the scraper on your local machine:

```bash
# Try RSS feed approach first (more reliable)
python3 taleb_substack_scraper_rss.py

# Or use direct HTTP approach
python3 taleb_substack_scraper.py

# Then run analysis
python3 analyze_taleb_articles.py
```

## Features

### Writing Style Analysis
- Total articles and word count
- Average sentence length
- Vocabulary richness
- Most frequent content words
- Thematic analysis (risk, probability, systems, etc.)
- Paragraph structure analysis

### Sentiment Analysis
- VADER sentiment scoring
- Optimism/pessimism classification
- Compound scores ranging from -1.0 (most pessimistic) to +1.0 (most optimistic)
- Time-series analysis of sentiment trends

### Visualizations
- **Sentiment over time graph**: Line plot showing sentiment evolution
- **Distribution histogram**: Shows distribution of sentiment scores
- Color-coded regions for optimistic (green) and pessimistic (red) content

## Analysis Results (Sample Data)

### Key Findings
- **Average Sentiment Score**: -0.526 (leaning pessimistic)
- **Total Articles Analyzed**: 12
- **Sentiment Distribution**:
  - Very Pessimistic: 9 articles (75%)
  - Optimistic: 1 article (8%)
  - Very Optimistic: 2 articles (17%)

### Most Pessimistic Articles
1. "The Virtue of Paranoia" (-0.989)
2. "On Intellectual Arrogance" (-0.985)
3. "The Fragility of Modern Systems" (-0.985)

### Most Optimistic Articles
1. "Why I Love the Mediterranean" (0.889)
2. "Against Linear Thinking" (0.880)
3. "On Hope and Resilience" (0.137)

### Writing Style Characteristics
- **Average Article Length**: 142 words
- **Average Sentence Length**: 8.1 words
- **Vocabulary Richness**: 0.420

### Key Themes
- Risk & Fragility: 33 mentions
- Systems & Complexity: 29 mentions
- Critique & Problems: 30 mentions
- Institutional Criticism: 17 mentions
- Probability: 12 mentions
- Positive/Hope: 11 mentions

## Customization

### Modify Scraping
Edit the scraper files to:
- Change the author username
- Adjust rate limiting (default: 2 seconds between requests)
- Modify content extraction patterns

### Adjust Analysis
Edit `analyze_taleb_articles.py` to:
- Modify sentiment thresholds
- Add custom themes for analysis
- Change visualization styles
- Add additional metrics

## Network Restrictions

If you encounter 403 errors when scraping:

1. **Run locally**: Execute scripts on your local machine instead of a restricted environment
2. **Use RSS feed**: The RSS approach is often less restricted
3. **Use sample data**: Test the analysis pipeline with generated sample data
4. **Manual import**: Save articles manually and import to JSON format

## Output Files

After running the analysis, you'll get:

1. **taleb_sentiment_analysis.png** - Comprehensive visualization showing:
   - Sentiment scores over time
   - Distribution of sentiment across articles

2. **taleb_analysis_results.csv** - Detailed CSV with:
   - Article titles and dates
   - Word counts
   - Sentiment scores (compound, positive, negative, neutral)
   - Sentiment labels
   - URLs

3. **Console output** - Detailed analysis including:
   - Writing style statistics
   - Sentiment summary
   - Most common words
   - Thematic breakdowns

## Technical Details

### Sentiment Analysis
Uses VADER (Valence Aware Dictionary and sEntiment Reasoner):
- Specially designed for social media and short texts
- Provides compound scores from -1 to +1
- Includes positive, negative, and neutral components

### Web Scraping
- Respects rate limits (2-second delays)
- Handles multiple URL patterns
- Extracts: title, date, content, URL
- Saves in JSON format for portability

## Future Enhancements

Potential improvements:
- Add more sophisticated NLP analysis (topic modeling, entity extraction)
- Compare with other authors
- Track sentiment trends over longer periods
- Add interactive visualizations (Plotly)
- Implement caching for faster re-analysis
- Add support for other Substack authors

## License

This is an educational project for learning web scraping and sentiment analysis.

## Notes

- Always respect website terms of service when scraping
- Implement appropriate rate limiting
- Store data responsibly
- Use for educational and research purposes

---

**Created**: 2026-01-11
**Author**: Claude Code Analysis Pipeline
