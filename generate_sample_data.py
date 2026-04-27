import csv
import random
from datetime import datetime, timedelta

# Sample data generator - creates realistic influencer data for demonstration
CATEGORIES = ["Tech", "Fitness", "Fashion", "Food", "Travel", "Entertainment", "Business", "Education"]
SAMPLE_HASHTAGS = {
    "Tech": ["technology", "startup", "coding", "ai", "innovation"],
    "Fitness": ["fitnessmotivation", "gym", "workout", "health", "bodybuilding"],
    "Fashion": ["fashionblogger", "ootd", "style", "designer", "luxury"],
    "Food": ["foodblogger", "cooking", "recipe", "restaurant", "delicious"],
    "Travel": ["wanderlust", "adventure", "travel", "explore", "destination"],
    "Entertainment": ["entertainment", "movies", "music", "comedy", "artist"],
    "Business": ["entrepreneur", "startup", "business", "marketing", "success"],
    "Education": ["learning", "education", "courses", "knowledge", "study"],
}

KNOWN_INFLUENCERS = [
    ("virat.kohli", "Virat Kohli"),
    ("cristiano", "Cristiano Ronaldo"),
    ("nasa", "NASA"),
    ("netflix", "Netflix"),
    ("instagram", "Instagram"),
    ("selenagomez", "Selena Gomez"),
    ("therock", "Dwayne Johnson"),
    ("khloekardashian", "Khloe Kardashian"),
    ("arianagrande", "Ariana Grande"),
    ("beyonce", "Beyoncé"),
    ("justinbieber", "Justin Bieber"),
    ("kimkardashian", "Kim Kardashian"),
    ("kylijenner", "Kylie Jenner"),
    ("oprah", "Oprah Winfrey"),
    ("billgates", "Bill Gates"),
    ("elonmusk", "Elon Musk"),
    ("jeffbezos", "Jeff Bezos"),
    ("markzuckerberg", "Mark Zuckerberg"),
    ("paddypower", "Paddy Power"),
    ("nike", "Nike"),
    ("redbull", "Red Bull"),
    ("google", "Google"),
    ("techcrunch", "TechCrunch"),
    ("wired", "Wired"),
    ("vogue", "Vogue"),
    ("natgeo", "National Geographic"),
    ("bbc", "BBC"),
]

FIRST_NAMES = [
    "Aarav", "Ananya", "Riya", "Rahul", "Priya", "Amit", "Mira", "Karan", "Divya", "Deepak",
    "Sara", "Neha", "Aakash", "Anjali", "Rohan", "Sneha", "Aditya", "Pooja", "Vikram", "Tarun",
    "Nisha", "Manish", "Kabir", "Ishita", "Ritu", "Shreya", "Arjun", "Meera", "Tanvi", "Aisha",
    "Ibrahim", "Kavya", "Nikhil", "Pranav", "Simran", "Tanya", "Vivek", "Anika", "Ravi", "Kriti",
    "Sidharth", "Mahi", "Raghav", "Kajal", "Neeraj", "Anushka", "Kunal", "Raina", "Isha", "Rohit",
]

LAST_NAMES = [
    "Sharma", "Patel", "Singh", "Kumar", "Gupta", "Mehta", "Joshi", "Kapoor", "Verma", "Chopra",
    "Nair", "Reddy", "Desai", "Jain", "Bajaj", "Agarwal", "Malhotra", "Bose", "Mishra", "Roy",
    "Bhattacharya", "Iyer", "Bhat", "Thakur", "Sinha", "Choudhary", "Rathi", "Saxena", "Walia", "Lal",
]

USERNAME_SUFFIXES = [
    "official", "daily", "world", "hub", "studio", "trends", "vibes", "zone", "diaries", "stories",
    "media", "talks", "guide", "tips", "channel", "life", "journal", "gram", "online", "now",
]


def build_username(full_name: str) -> str:
    base = full_name.lower().replace(" ", "_").replace(".", "")
    suffix = random.choice(USERNAME_SUFFIXES) if random.random() > 0.4 else ""
    username = f"{base}_{suffix}" if suffix else base
    if random.random() > 0.6:
        username = f"{username}{random.randint(1,99)}"
    return username


def build_influencer_pool(total: int = 2000) -> list:
    influencers = KNOWN_INFLUENCERS.copy()
    seen = {username for username, _ in influencers}
    while len(influencers) < total:
        full_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        username = build_username(full_name)
        if username in seen:
            continue
        seen.add(username)
        influencers.append((username, full_name))
    return influencers


def get_followers_by_tier() -> int:
    tier = random.choices(
        ["Nano", "Micro", "Mid", "Macro", "Mega"],
        weights=[18, 40, 22, 12, 8],
        k=1,
    )[0]
    if tier == "Nano":
        return random.randint(10_000, 50_000)
    if tier == "Micro":
        return random.randint(50_001, 250_000)
    if tier == "Mid":
        return random.randint(250_001, 750_000)
    if tier == "Macro":
        return random.randint(750_001, 2_500_000)
    return random.randint(2_500_001, 12_000_000)


def get_engagement_stats(followers: int) -> tuple[int, int, float]:
    engagement_rate = round(random.uniform(2.0, 8.5), 2)
    likes = max(50, int(followers * engagement_rate / 100 * random.uniform(0.45, 0.7)))
    comments = max(5, int(likes * random.uniform(0.08, 0.15)))
    return likes, comments, engagement_rate


def generate_sample_data(count: int = 50) -> list:
    """Generate realistic sample influencer data."""
    rows = []
    influencers = build_influencer_pool(count)
    
    for i, (username, full_name) in enumerate(influencers):
        category = random.choice(CATEGORIES)
        followers = get_followers_by_tier()
        likes, comments, engagement_rate = get_engagement_stats(followers)
        
        # Random posting frequency (days between posts)
        posting_frequency = round(random.uniform(1, 6), 2)
        
        # Top hashtags
        category_hashtags = SAMPLE_HASHTAGS.get(category, ["instagram", "viral"])
        top_hashtags = ", ".join(random.sample(category_hashtags, min(3, len(category_hashtags))))
        
        # Contact details (simulated - many influencers share email or DM info)
        contact = ""
        if random.random() > 0.55:
            contact = f"contact@{username}.com"
        elif random.random() > 0.8:
            contact = f"{username}@gmail.com"
        
        automation = "Yes" if engagement_rate < 3.5 and random.random() > 0.5 else "No"
        
        rows.append({
            "username": username,
            "full_name": full_name,
            "followers": followers,
            "category": category,
            "engagement_rate (%)": engagement_rate,
            "likes": likes,
            "comments": comments,
            "posting_frequency_days": posting_frequency,
            "top_hashtags": top_hashtags,
            "contact_details": contact,
            "automation_likely": automation,
            "profile_url": f"https://instagram.com/{username}",
        })
    
    return rows

def main():
    print("Generating sample Instagram influencer data (2000+ profiles)...")
    rows = generate_sample_data(count=2000)
    
    output_file = "influencers_2000_profiles_final.csv"
    if not rows:
        print("No data generated.")
        return
    
    try:
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
    except PermissionError:
        fallback_name = f"influencers_2000_profiles_{datetime.now():%Y%m%d_%H%M%S}.csv"
        output_file = fallback_name
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        print(f"⚠️ Original file was locked, so data was saved to {output_file}.")
    
    print(f"✓ Sample data generated: {output_file}")
    print(f"  Records: {len(rows)}")
    print(f"\nColumns: {', '.join(list(rows[0].keys()))}")
    print(f"\nOpen {output_file} in Excel or view the data.")

if __name__ == "__main__":
    main()
