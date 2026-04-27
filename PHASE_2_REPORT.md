# Phase 2: Smart Analysis & Ranking Report

This report summarizes the findings from the AI/ML-driven analysis of 2000+ influencer profiles.

## AI/ML Insights

### 1. Engagement Prediction
We trained a Linear Regression model to predict "Expected Engagement" based on follower count and posting frequency. 
- **Average Predicted Engagement**: 5.31%
- **Insights**: Profiles significantly exceeding their predicted engagement (Variance > 5%) were flagged for further authenticity checks.

### 2. NLP Caption Analysis
Using `TextBlob`, we analyzed `top_hashtags` to derive a **Sentiment Score**.
- This helps identify influencers who maintain a positive, brand-safe tone.
- High-performing influencers often have hashtags with high positive sentiment (e.g., #inspiration, #fitnessgoals).

### 3. Authenticity & Automation
A multi-factor **Authenticity Score** was calculated:
- **Heuristics**: Penalties applied for "Automation Likely" flags.
- **Data Quality**: Penalties for low interaction quality (very low comments relative to likes).
- **Outlier Detection**: Unusually high engagement relative to the follower base without corresponding content quality.

---

## Top 10 Ranked Influencers (Snapshot)

| Rank | Username | Score (0-100) | Category | Followers | Engagement |
|------|----------|---------------|----------|-----------|------------|
| 1 | ravi_desai | 98.27 | Fitness | 10.2M | 8.46% |
| 2 | tanvi_verma_online8 | 96.98 | Education | 6.8M | 8.43% |
| 3 | nisha_singh_journal23 | 96.45 | Entertainment | 3.5M | 8.40% |
| 4 | meera_mishra_vibes | 96.08 | Food | 2.4M | 8.25% |
| 5 | raghav_thakur_stories | 95.60 | Food | 11.7M | 8.09% |
| 6 | isha_bose_tips31 | 95.51 | Entertainment | 167K | 8.45% |
| 7 | aakash_saxena_world84 | 95.13 | Education | 8.0M | 8.41% |
| 8 | netflix | 95.05 | Entertainment | 5.7M | 8.45% |
| 9 | arjun_singh_diaries | 94.98 | Fashion | 502K | 8.37% |
| 10 | manish_saxena_life | 94.97 | Entertainment | 10.6M | 7.94% |

---

## Category Performance

| Category | Avg. Performance Score | Top Performer |
|----------|------------------------|---------------|
| **Travel** | 77.25 | mahi_mishra_world28 |
| **Business** | 77.01 | ananya_reddy |
| **Tech** | 76.90 | karan_verma_vibes62 |
| **Education** | 76.62 | tanvi_verma_online8 |
| **Fitness** | 76.50 | ravi_desai |

---

## Automation Detection Summary

- **Total Profiles Analyzed**: 2000
- **Automation Impact**: 
  - Manual Average Score: **79.0**
  - Automated Average Score: **56.7** (Significant drop due to authenticity penalties)

---

## Files Created in Phase 2:
- `smart_analysis.py` - AI/ML logic
- `ranked_influencers.csv` - Full ranked dataset
- `dashboard.html` - Interactive Dashboard
- `PHASE_2_REPORT.md` - This report
