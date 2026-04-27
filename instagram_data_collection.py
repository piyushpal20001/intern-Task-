import argparse
import csv
import re
import statistics
import sys
from datetime import datetime
from typing import Dict, List, Optional

import instaloader

CATEGORY_KEYWORDS = {
    "Tech": ["tech", "technology", "gadgets", "software", "hardware", "ai", "ml", "programming", "coding", "startup"],
    "Fitness": ["fitness", "workout", "gym", "health", "wellness", "nutrition", "yoga", "trainer", "bodybuilding"],
    "Fashion": ["fashion", "style", "ootd", "beauty", "designer", "makeup"],
    "Food": ["food", "cooking", "recipes", "chef", "restaurant", "baking", "nutrition"],
    "Travel": ["travel", "tour", "vacation", "adventure", "wanderlust", "destination"],
    "Entertainment": ["music", "movies", "comedy", "dance", "actor", "artist", "show"],
    "Business": ["business", "entrepreneur", "marketing", "sales", "finance", "investing", "startup"],
    "Education": ["education", "learning", "study", "teacher", "tutorial", "course"],
}

HASHTAG_PATTERN = re.compile(r"#([A-Za-z0-9_]+)")
EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_PATTERN = re.compile(r"(?:\+?\d[\d \-()]{6,}\d)")


def guess_category(text: str) -> str:
    text_lower = text.lower()
    scores = {category: 0 for category in CATEGORY_KEYWORDS}
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                scores[category] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Other"


def extract_hashtags(text: str) -> List[str]:
    return [match.group(1).lower() for match in HASHTAG_PATTERN.finditer(text)]


def extract_contact_info(text: str) -> str:
    contacts = []
    emails = EMAIL_PATTERN.findall(text)
    phones = PHONE_PATTERN.findall(text)
    if emails:
        contacts.extend(sorted(set(emails)))
    if phones:
        contacts.extend(sorted(set(phones)))
    return ", ".join(contacts)


def compute_posting_frequency(dates: List[datetime]) -> Optional[float]:
    if len(dates) < 2:
        return None
    differences = [
        (dates[i - 1] - dates[i]).days
        for i in range(1, len(dates))
        if dates[i - 1] > dates[i]
    ]
    if not differences:
        return None
    return round(statistics.mean(differences), 2)


def compute_engagement_rate(likes: int, comments: int, followers: int) -> Optional[float]:
    if followers <= 0:
        return None
    return round(((likes + comments) / followers) * 100, 2)


def detect_automation(profile: instaloader.Profile, posts: List[instaloader.Post]) -> str:
    clues = []
    bio = profile.biography.lower()
    if any(term in bio for term in ["scheduler", "scheduled", "auto", "later", "buffer", "hootsuite", "planoly", "zapier"]):
        clues.append("bio mentions automation")
    if len(posts) >= 5:
        intervals = [
            (posts[i - 1].date_utc - posts[i].date_utc).total_seconds() / 3600
            for i in range(1, len(posts))
            if posts[i - 1].date_utc > posts[i].date_utc
        ]
        if intervals:
            avg_hours = sum(intervals) / len(intervals)
            if 20 < avg_hours < 28 and all(abs(interval - avg_hours) < 6 for interval in intervals):
                clues.append("consistent hourly posting")
    return "Yes" if clues else "No"


def profile_to_row(profile: instaloader.Profile, posts_to_analyze: int = 12) -> Dict[str, Optional[str]]:
    bio_text = profile.biography or ""
    category = guess_category(profile.full_name + " " + bio_text)
    contact = extract_contact_info(bio_text) or profile.external_url or ""

    posts: List[instaloader.Post] = []
    for count, post in enumerate(profile.get_posts(), start=1):
        posts.append(post)
        if count >= posts_to_analyze:
            break

    total_likes = sum(post.likes for post in posts)
    total_comments = sum(post.comments for post in posts)
    post_dates = [post.date_utc for post in posts]
    hashtags = []
    for post in posts:
        hashtags.extend(extract_hashtags(post.caption or ""))

    engagement_rate = compute_engagement_rate(total_likes, total_comments, profile.followers)
    posting_frequency = compute_posting_frequency(post_dates)
    automation = detect_automation(profile, posts)

    return {
        "username": profile.username,
        "full_name": profile.full_name,
        "followers": profile.followers,
        "category": category,
        "engagement_rate (%)": engagement_rate,
        "posting_frequency_days": posting_frequency,
        "top_hashtags": ", ".join(sorted(set(hashtags), key=hashtags.index))[:1000],
        "contact_details": contact,
        "automation_likely": automation,
        "profile_url": f"https://instagram.com/{profile.username}",
    }


def load_usernames(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def write_csv(rows: List[Dict[str, Optional[str]]], output_file: str) -> None:
    if not rows:
        return
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="Instagram influencer data collector")
    parser.add_argument("--usernames", required=True, help="Path to a file with one Instagram username per line")
    parser.add_argument("--output", required=True, help="Output CSV file path")
    parser.add_argument("--login", help="Instagram username for login")
    parser.add_argument("--password", help="Instagram password for login")
    parser.add_argument("--sessionfile", help="Path to an Instaloader session file to reuse a login session")
    parser.add_argument("--posts", type=int, default=12, help="Number of recent posts to analyze")
    args = parser.parse_args()

    loader = instaloader.Instaloader(sleep=True, quiet=True)
    if args.sessionfile:
        if not args.login:
            print("Session file loading requires --login <username> to identify the saved session.")
            sys.exit(1)
        try:
            loader.load_session_from_file(args.login, filename=args.sessionfile)
        except FileNotFoundError:
            print(f"Session file not found: {args.sessionfile}")
            sys.exit(1)
        except Exception as exc:
            print(f"Failed to load session file: {exc}")
            sys.exit(1)
    elif args.login and args.password:
        try:
            loader.login(args.login, args.password)
        except instaloader.exceptions.LoginException as exc:
            print(f"Login failed: {exc}")
            print("Use valid Instagram credentials or omit --login/--password for public profile access.")
            sys.exit(1)
    elif args.login or args.password:
        print("Both --login and --password are required to log in. Omit both for public access.")
        sys.exit(1)

    try:
        usernames = load_usernames(args.usernames)
    except FileNotFoundError as exc:
        print(exc)
        sys.exit(1)
    rows = []
    for username in usernames:
        try:
            profile = instaloader.Profile.from_username(loader.context, username)
        except Exception as exc:
            message = str(exc).lower()
            if "does not exist" in message or "not found" in message:
                print(f"Profile not found: {username}. Verify the username in {args.usernames}.")
                continue
            if "403" in message or "graphql" in message or "forbidden" in message:
                print(f"Access blocked for {username}. Try logging in with --login/--password or using --sessionfile.")
                continue
            print(f"Error processing {username}: {exc}")
            continue

        if profile.followers > 1_000_000:
            print(f"Skipping {username}: more than 1M followers")
            continue
        rows.append(profile_to_row(profile, posts_to_analyze=args.posts))
        print(f"Collected data for {username}")

    write_csv(rows, args.output)
    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
