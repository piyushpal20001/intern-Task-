import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from textblob import TextBlob
import json
import os

# Download NLTK data if needed
try:
    import nltk
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    pass

class SmartInfluencerAnalyzer:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)
        self.prepare_data()

    def prepare_data(self):
        """Clean and prepare numeric data."""
        # Ensure numeric types
        self.df['followers'] = pd.to_numeric(self.df['followers'], errors='coerce').fillna(0)
        self.df['engagement_rate (%)'] = pd.to_numeric(self.df['engagement_rate (%)'], errors='coerce').fillna(0)
        self.df['posting_frequency_days'] = pd.to_numeric(self.df['posting_frequency_days'], errors='coerce').fillna(7)
        self.df['likes'] = pd.to_numeric(self.df['likes'], errors='coerce').fillna(0)
        self.df['comments'] = pd.to_numeric(self.df['comments'], errors='coerce').fillna(0)
        
    def predict_engagement(self):
        """Train a model to predict engagement rate based on followers and frequency."""
        print("Training Engagement Prediction Model...")
        
        # Features: Followers (log scale for better normalization), Posting Frequency
        X = self.df[['followers', 'posting_frequency_days']].copy()
        X['followers_log'] = np.log1p(X['followers'])
        X = X[['followers_log', 'posting_frequency_days']]
        
        y = self.df['engagement_rate (%)']
        
        # Simple Linear Regression
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict
        self.df['predicted_engagement_rate'] = model.predict(X)
        self.df['engagement_variance'] = self.df['engagement_rate (%)'] - self.df['predicted_engagement_rate']
        
        print(f"Model trained. Average Prediction: {self.df['predicted_engagement_rate'].mean():.2f}%")

    def analyze_sentiment(self):
        """Analyze hashtags for sentiment/quality."""
        print("Analyzing Hashtag Sentiment (NLP)...")
        
        def get_sentiment(text):
            if pd.isna(text) or text == "":
                return 0.5 # Neutral
            # TextBlob sentiment ranges from -1 to 1, we normalize to 0 to 1
            analysis = TextBlob(str(text))
            return (analysis.sentiment.polarity + 1) / 2

        self.df['sentiment_score'] = self.df['top_hashtags'].apply(get_sentiment)
        print("Sentiment analysis complete.")

    def calculate_authenticity(self):
        """Calculate an authenticity score (0-1)."""
        print("Calculating Authenticity Scores...")
        
        # Logic: High engagement variance (outliers) and high automation flag reduce authenticity
        # We also look at comment/like ratio (bots often have very few comments relative to likes)
        
        self.df['comment_like_ratio'] = self.df['comments'] / (self.df['likes'] + 1)
        avg_ratio = self.df['comment_like_ratio'].mean()
        
        def score_authenticity(row):
            score = 1.0
            
            # Penalty for automation likely
            if row['automation_likely'] == 'Yes':
                score -= 0.3
            
            # Penalty for suspicious engagement (too high relative to predicted)
            if row['engagement_variance'] > 5: # 5% higher than predicted is sus
                score -= 0.2
                
            # Penalty for low interaction quality (comments vs likes)
            if row['comment_like_ratio'] < (avg_ratio * 0.5):
                score -= 0.2
                
            return max(0.1, min(1.0, score))

        self.df['authenticity_score'] = self.df.apply(score_authenticity, axis=1)

    def rank_influencers(self):
        """Rank influencers based on weighted scores."""
        print("Ranking Influencers...")
        
        # Normalize metrics to 0-1
        max_followers = np.log1p(self.df['followers'].max())
        self.df['norm_reach'] = np.log1p(self.df['followers']) / max_followers
        
        # Engagement (relative to max in dataset)
        max_eng = self.df['engagement_rate (%)'].max()
        self.df['norm_eng'] = self.df['engagement_rate (%)'] / (max_eng if max_eng > 0 else 1)
        
        # Consistency (Lower days between posts is better, we cap at 14 days)
        self.df['norm_consistency'] = 1 - (self.df['posting_frequency_days'].clip(1, 14) / 14)

        # Final Weighted Score (0-100)
        # Engagement: 40, Authenticity: 30, Consistency: 20, Reach: 10
        self.df['performance_score'] = (
            self.df['norm_eng'] * 40 +
            self.df['authenticity_score'] * 30 +
            self.df['norm_consistency'] * 20 +
            self.df['norm_reach'] * 10
        ).round(2)
        
        # Sort and Rank
        self.df = self.df.sort_values(by='performance_score', ascending=False)
        self.df['rank'] = range(1, len(self.df) + 1)
        
        print("Ranking complete.")

    def save_results(self, output_csv, report_path):
        """Export results to CSV and JSON for dashboard."""
        self.df.to_csv(output_csv, index=False)
        print(f"Ranked data saved to {output_csv}")
        
        # Save JSON for Dashboard (top 100 for performance)
        dashboard_data = self.df.head(100).replace({np.nan: None}).to_dict(orient='records')
        with open('dashboard_data.json', 'w') as f:
            json.dump(dashboard_data, f, indent=4)
            
        # Generate summary for report
        summary = {
            "total": len(self.df),
            "avg_score": self.df['performance_score'].mean(),
            "top_categories": self.df.groupby('category')['performance_score'].mean().sort_values(ascending=False).to_dict(),
            "automation_impact": self.df.groupby('automation_likely')['performance_score'].mean().to_dict()
        }
        
        with open('analysis_summary.json', 'w') as f:
            json.dump(summary, f, indent=4)

if __name__ == "__main__":
    input_file = "influencers_2000_profiles_final_corrected.csv"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
    else:
        analyzer = SmartInfluencerAnalyzer(input_file)
        analyzer.predict_engagement()
        analyzer.analyze_sentiment()
        analyzer.calculate_authenticity()
        analyzer.rank_influencers()
        analyzer.save_results("ranked_influencers.csv", "PHASE_2_REPORT.md")
        print("\nPhase 2 Smart Analysis Successful!")
