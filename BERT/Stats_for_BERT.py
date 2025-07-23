import pandas as pd
import numpy as np

# Assuming your CSV has columns: tweet_id, user_id, misinformation_score, engagement_metrics

# Load your data
df = pd.read_csv("bert_misinformation_results.csv")

# Basic community metrics
community_metrics = {
    "mean_misinfo_score": df["misinformation_score"].mean(),
    "median_misinfo_score": df["misinformation_score"].median(),
    "high_misinfo_percentage": (df["misinformation_score"] > 0.7).mean() * 100,  # % above threshold
    "std_dev": df["misinformation_score"].std(),
    
    # Engagement weighted
    "weighted_misinfo_score": np.average(
        df["misinformation_score"], 
        weights=df["retweet_count"] + df["like_count"] + 1
    ),
    
    # User-level analysis
    "user_avg_misinfo": df.groupby("user_id")["misinformation_score"].mean().mean(),
    
    # Volume metrics
    "misinfo_tweet_density": (df["misinformation_score"] > 0.5).sum() / len(df)
}