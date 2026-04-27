import csv
import argparse

# Mapping of keywords to categories
KEYWORD_TO_CATEGORY = {
    "fashion": "Fashion",
    "ootd": "Fashion",
    "style": "Fashion",
    "designer": "Fashion",
    "luxury": "Fashion",
    "fitness": "Fitness",
    "gym": "Fitness",
    "workout": "Fitness",
    "health": "Fitness",
    "bodybuilding": "Fitness",
    "fitnessmotivation": "Fitness",
    "food": "Food",
    "cooking": "Food",
    "recipe": "Food",
    "restaurant": "Food",
    "delicious": "Food",
    "foodblogger": "Food",
    "travel": "Travel",
    "wanderlust": "Travel",
    "adventure": "Travel",
    "explore": "Travel",
    "destination": "Travel",
    "entertainment": "Entertainment",
    "movies": "Entertainment",
    "music": "Entertainment",
    "comedy": "Entertainment",
    "artist": "Entertainment",
    "business": "Business",
    "entrepreneur": "Business",
    "startup": "Business",
    "marketing": "Business",
    "success": "Business",
    "tech": "Tech",
    "coding": "Tech",
    "ai": "Tech",
    "innovation": "Tech",
    "technology": "Tech",
    "education": "Education",
    "learning": "Education",
    "courses": "Education",
    "knowledge": "Education",
    "study": "Education",
    "facts": "Education",
}

# Known influencers and their correct categories and full names
KNOWN_INFLUENCERS = {
    "virat.kohli": ("Fitness", "Virat Kohli"),
    "cristiano": ("Fitness", "Cristiano Ronaldo"),
    "nasa": ("Education", "NASA"),
    "netflix": ("Entertainment", "Netflix"),
    "instagram": ("Tech", "Instagram"),
    "selenagomez": ("Entertainment", "Selena Gomez"),
    "therock": ("Fitness", "Dwayne Johnson"),
    "khloekardashian": ("Entertainment", "Khloe Kardashian"),
    "arianagrande": ("Entertainment", "Ariana Grande"),
    "beyonce": ("Entertainment", "Beyoncé"),
    "justinbieber": ("Entertainment", "Justin Bieber"),
    "kimkardashian": ("Fashion", "Kim Kardashian"),
    "kylijenner": ("Fashion", "Kylie Jenner"),
    "oprah": ("Business", "Oprah Winfrey"),
    "billgates": ("Business", "Bill Gates"),
    "elonmusk": ("Tech", "Elon Musk"),
    "jeffbezos": ("Business", "Jeff Bezos"),
    "markzuckerberg": ("Tech", "Mark Zuckerberg"),
    "paddypower": ("Business", "Paddy Power"),
    "nike": ("Business", "Nike"),
    "redbull": ("Business", "Red Bull"),
    "google": ("Tech", "Google"),
    "techcrunch": ("Tech", "TechCrunch"),
    "wired": ("Tech", "Wired"),
    "vogue": ("Fashion", "Vogue"),
    "natgeo": ("Travel", "National Geographic"),
    "bbc": ("Education", "BBC"),
}

def determine_details(username, full_name, hashtags):
    category = "Business"  # default
    corrected_full_name = full_name
    
    # Override for known influencers
    if username in KNOWN_INFLUENCERS:
        category, corrected_full_name = KNOWN_INFLUENCERS[username]
        return category, corrected_full_name
    
    # Check username and full_name for keywords
    text = f"{username} {full_name}".lower()
    for keyword, cat in KEYWORD_TO_CATEGORY.items():
        if keyword in text:
            category = cat
            break
    
    # Determine from hashtags
    hashtags_lower = hashtags.lower()
    for keyword, cat in KEYWORD_TO_CATEGORY.items():
        if keyword in hashtags_lower:
            category = cat
            break
    
    return category, corrected_full_name

def correct_categories(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    for row in rows:
        hashtags = row['top_hashtags']
        username = row['username']
        full_name = row['full_name']
        correct_category, correct_full_name = determine_details(username, full_name, hashtags)
        row['category'] = correct_category
        row['full_name'] = correct_full_name
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Corrected categories saved to {output_file}")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Correct categories in influencer CSV data.')
    parser.add_argument(
        'input_file',
        nargs='?',
        default='influencers_2000_profiles_final.csv',
        help='Path to the input CSV file to correct.',
    )
    parser.add_argument(
        'output_file',
        nargs='?',
        default='influencers_2000_profiles_final_corrected.csv',
        help='Path to the output corrected CSV file.',
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    correct_categories(args.input_file, args.output_file)