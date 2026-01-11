"""
Comprehensive Analysis of Nassim Taleb's Articles
- Writing style analysis
- Sentiment analysis (optimism/pessimism scoring)
- Visualization of sentiment over time
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
from collections import Counter
import numpy as np

class TalebArticleAnalyzer:
    def __init__(self, json_file='taleb_articles.json'):
        """Initialize the analyzer with article data"""
        with open(json_file, 'r', encoding='utf-8') as f:
            self.articles = json.load(f)

        self.analyzer = SentimentIntensityAnalyzer()
        self.df = None

    def load_to_dataframe(self):
        """Convert articles to pandas DataFrame"""
        data = []
        for article in self.articles:
            # Parse date
            try:
                date = pd.to_datetime(article['date'])
            except:
                date = pd.NaT

            data.append({
                'title': article.get('title', ''),
                'date': date,
                'url': article.get('url', ''),
                'content': article.get('content', ''),
                'word_count': len(article.get('content', '').split())
            })

        self.df = pd.DataFrame(data)
        self.df = self.df.sort_values('date')
        return self.df

    def analyze_writing_style(self):
        """Analyze the writing style of articles"""
        if self.df is None:
            self.load_to_dataframe()

        print("\n" + "=" * 60)
        print("WRITING STYLE ANALYSIS")
        print("=" * 60)

        # Overall statistics
        total_articles = len(self.df)
        total_words = self.df['word_count'].sum()
        avg_words = self.df['word_count'].mean()

        print(f"\nGeneral Statistics:")
        print(f"  Total articles: {total_articles}")
        print(f"  Total words: {total_words:,}")
        print(f"  Average words per article: {avg_words:.0f}")
        print(f"  Shortest article: {self.df['word_count'].min()} words")
        print(f"  Longest article: {self.df['word_count'].max()} words")

        # Combine all content for analysis
        all_text = ' '.join(self.df['content'].tolist())

        # Sentence analysis
        sentences = [s.strip() for s in re.split(r'[.!?]+', all_text) if s.strip()]
        avg_sentence_length = np.mean([len(s.split()) for s in sentences])

        print(f"\nSentence Structure:")
        print(f"  Total sentences: {len(sentences)}")
        print(f"  Average sentence length: {avg_sentence_length:.1f} words")

        # Vocabulary analysis
        words = re.findall(r'\b[a-z]+\b', all_text.lower())
        unique_words = set(words)
        vocabulary_richness = len(unique_words) / len(words) if words else 0

        print(f"\nVocabulary:")
        print(f"  Total words: {len(words):,}")
        print(f"  Unique words: {len(unique_words):,}")
        print(f"  Vocabulary richness: {vocabulary_richness:.3f}")

        # Most common words (excluding very common ones)
        common_stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                           'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been',
                           'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                           'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
                           'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who',
                           'when', 'where', 'why', 'how', 'not', 'no', 'yes'}

        content_words = [w for w in words if w not in common_stopwords and len(w) > 3]
        word_freq = Counter(content_words)
        most_common = word_freq.most_common(20)

        print(f"\nMost Frequent Content Words:")
        for word, count in most_common[:10]:
            print(f"  {word}: {count}")

        # Key themes (specific to Taleb's typical topics)
        themes = {
            'risk': ['risk', 'risks', 'risky', 'ruin', 'fragile', 'fragility', 'robust', 'resilient', 'resilience'],
            'probability': ['probability', 'probabilistic', 'random', 'uncertainty', 'uncertain', 'stochastic'],
            'systems': ['system', 'systems', 'complex', 'complexity', 'nonlinear', 'nonlinearity'],
            'institutional_criticism': ['academic', 'academics', 'expert', 'experts', 'institution', 'institutions', 'bureaucrat'],
            'nassim_concepts': ['antifragile', 'fragility', 'optionality', 'convex', 'concave', 'barbell', 'lindy'],
            'critique': ['wrong', 'mistake', 'fail', 'failure', 'failed', 'problem', 'problems', 'dangerous', 'disaster'],
            'positive': ['hope', 'optimistic', 'optimism', 'better', 'improve', 'improvement', 'solution', 'thrive']
        }

        print(f"\nThematic Analysis:")
        all_text_lower = all_text.lower()
        for theme, keywords in themes.items():
            count = sum(all_text_lower.count(keyword) for keyword in keywords)
            print(f"  {theme.replace('_', ' ').title()}: {count} mentions")

        # Paragraph structure
        paragraphs = [p.strip() for p in all_text.split('\n\n') if p.strip()]
        avg_para_length = np.mean([len(p.split()) for p in paragraphs])

        print(f"\nParagraph Structure:")
        print(f"  Total paragraphs: {len(paragraphs)}")
        print(f"  Average paragraph length: {avg_para_length:.1f} words")

        return {
            'total_articles': total_articles,
            'total_words': total_words,
            'avg_words_per_article': avg_words,
            'avg_sentence_length': avg_sentence_length,
            'vocabulary_richness': vocabulary_richness,
            'most_common_words': most_common,
            'theme_counts': {theme: sum(all_text_lower.count(kw) for kw in keywords)
                           for theme, keywords in themes.items()}
        }

    def analyze_sentiment(self):
        """Analyze sentiment (optimism/pessimism) for each article"""
        if self.df is None:
            self.load_to_dataframe()

        print("\n" + "=" * 60)
        print("SENTIMENT ANALYSIS (OPTIMISM/PESSIMISM)")
        print("=" * 60)

        sentiments = []

        for idx, row in self.df.iterrows():
            content = row['content']

            # Get VADER sentiment scores
            vader_scores = self.analyzer.polarity_scores(content)

            # VADER provides: neg, neu, pos, compound
            # compound score ranges from -1 (most negative) to +1 (most positive)

            sentiments.append({
                'negative': vader_scores['neg'],
                'neutral': vader_scores['neu'],
                'positive': vader_scores['pos'],
                'compound': vader_scores['compound']
            })

        # Add sentiments to dataframe (only add new columns)
        sentiment_df = pd.DataFrame(sentiments)
        for col in sentiment_df.columns:
            self.df[col] = sentiment_df[col].values

        # Print summary
        print(f"\nOverall Sentiment Summary:")
        print(f"  Average Compound Score: {self.df['compound'].mean():.3f}")
        print(f"  (Range: -1.0 = most pessimistic, +1.0 = most optimistic)")
        print(f"\nScore Distribution:")
        print(f"  Most pessimistic: {self.df['compound'].min():.3f}")
        print(f"  Most optimistic: {self.df['compound'].max():.3f}")
        print(f"  Standard deviation: {self.df['compound'].std():.3f}")

        # Classify articles
        very_pessimistic = (self.df['compound'] < -0.5).sum()
        pessimistic = ((self.df['compound'] >= -0.5) & (self.df['compound'] < -0.05)).sum()
        neutral = ((self.df['compound'] >= -0.05) & (self.df['compound'] <= 0.05)).sum()
        optimistic = ((self.df['compound'] > 0.05) & (self.df['compound'] <= 0.5)).sum()
        very_optimistic = (self.df['compound'] > 0.5).sum()

        print(f"\nSentiment Classification:")
        print(f"  Very Pessimistic (< -0.5): {very_pessimistic} articles")
        print(f"  Pessimistic (-0.5 to -0.05): {pessimistic} articles")
        print(f"  Neutral (-0.05 to 0.05): {neutral} articles")
        print(f"  Optimistic (0.05 to 0.5): {optimistic} articles")
        print(f"  Very Optimistic (> 0.5): {very_optimistic} articles")

        # Show most pessimistic and optimistic articles
        print(f"\nMost Pessimistic Articles:")
        most_pessimistic = self.df.nsmallest(3, 'compound')[['title', 'date', 'compound']]
        for _, row in most_pessimistic.iterrows():
            print(f"  {row['compound']:.3f} - {row['title']}")

        print(f"\nMost Optimistic Articles:")
        most_optimistic = self.df.nlargest(3, 'compound')[['title', 'date', 'compound']]
        for _, row in most_optimistic.iterrows():
            print(f"  {row['compound']:.3f} - {row['title']}")

        return self.df

    def visualize_sentiment_over_time(self, output_file='taleb_sentiment_analysis.png'):
        """Create visualization of sentiment over time"""
        if self.df is None or 'compound' not in self.df.columns:
            self.analyze_sentiment()

        print(f"\n" + "=" * 60)
        print("CREATING VISUALIZATION")
        print("=" * 60)

        # Create figure with subplots
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))

        # Remove rows with NaT dates for plotting
        plot_df = self.df.dropna(subset=['date']).copy()
        plot_df = plot_df.sort_values('date').reset_index(drop=True)

        # Extract arrays for plotting
        dates = plot_df['date'].values
        compound = plot_df['compound'].values

        # Plot 1: Sentiment over time (line plot with markers)
        ax1 = axes[0]
        ax1.plot(dates, compound, marker='o', linestyle='-',
                linewidth=2, markersize=8, color='#2E86AB', label='Sentiment Score')

        # Add horizontal reference lines
        ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5, label='Neutral')
        ax1.axhline(y=0.5, color='green', linestyle=':', alpha=0.3, label='Very Optimistic')
        ax1.axhline(y=-0.5, color='red', linestyle=':', alpha=0.3, label='Very Pessimistic')

        # Fill areas
        ax1.fill_between(dates, compound, 0,
                        where=(compound > 0), alpha=0.3, color='green',
                        interpolate=True, label='Optimistic')
        ax1.fill_between(dates, compound, 0,
                        where=(compound < 0), alpha=0.3, color='red',
                        interpolate=True, label='Pessimistic')

        ax1.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Sentiment Score', fontsize=12, fontweight='bold')
        ax1.set_title('Nassim Taleb - Sentiment Over Time\n(Optimism/Pessimism Analysis)',
                     fontsize=14, fontweight='bold')
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(-1.0, 1.0)

        # Rotate date labels
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

        # Plot 2: Sentiment distribution (histogram)
        ax2 = axes[1]
        ax2.hist(plot_df['compound'], bins=20, color='#A23B72', alpha=0.7, edgecolor='black')
        ax2.axvline(x=0, color='gray', linestyle='--', linewidth=2, label='Neutral')
        ax2.axvline(x=plot_df['compound'].mean(), color='orange', linestyle='-',
                   linewidth=2, label=f'Mean: {plot_df["compound"].mean():.3f}')

        ax2.set_xlabel('Sentiment Score', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Number of Articles', fontsize=12, fontweight='bold')
        ax2.set_title('Distribution of Sentiment Scores', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')

        # Adjust layout
        plt.tight_layout()

        # Save figure
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\nVisualization saved to: {output_file}")

        return output_file

    def save_results(self, output_file='taleb_analysis_results.csv'):
        """Save analysis results to CSV"""
        if self.df is None:
            self.load_to_dataframe()

        # Select relevant columns
        results_df = self.df[[
            'date', 'title', 'word_count', 'compound',
            'positive', 'negative', 'neutral', 'url'
        ]].copy()

        # Add sentiment label
        def classify_sentiment(score):
            if score < -0.5:
                return 'Very Pessimistic'
            elif score < -0.05:
                return 'Pessimistic'
            elif score <= 0.05:
                return 'Neutral'
            elif score <= 0.5:
                return 'Optimistic'
            else:
                return 'Very Optimistic'

        results_df['sentiment_label'] = results_df['compound'].apply(classify_sentiment)

        # Save to CSV
        results_df.to_csv(output_file, index=False)
        print(f"\nDetailed results saved to: {output_file}")

        return output_file

    def generate_full_report(self):
        """Generate complete analysis report"""
        print("\n" + "=" * 60)
        print("NASSIM TALEB ARTICLE ANALYSIS")
        print("Complete Writing Style & Sentiment Analysis")
        print("=" * 60)

        # Load data
        self.load_to_dataframe()

        # Run all analyses
        writing_stats = self.analyze_writing_style()
        sentiment_df = self.analyze_sentiment()
        viz_file = self.visualize_sentiment_over_time()
        csv_file = self.save_results()

        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)
        print(f"\nGenerated files:")
        print(f"  1. {viz_file} - Sentiment visualization")
        print(f"  2. {csv_file} - Detailed results (CSV)")

        return {
            'writing_stats': writing_stats,
            'visualization': viz_file,
            'csv_results': csv_file
        }


def main():
    """Run the complete analysis"""
    analyzer = TalebArticleAnalyzer('taleb_articles.json')
    results = analyzer.generate_full_report()

    print("\n" + "=" * 60)
    print("SUCCESS!")
    print("=" * 60)
    print("\nYour analysis is complete. Check the generated files for results.")


if __name__ == "__main__":
    main()
