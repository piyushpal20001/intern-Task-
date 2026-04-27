# Instagram Influencer Data Collection

This project contains a Python script to collect influencer/page data from Instagram profiles with less than 1M followers.

## What it collects
- Username
- Followers
- Category (guessed from bio and profile text)
- Engagement rate (likes + comments / followers)
- Posting frequency (average days between recent posts)
- Hashtags used in recent posts
- Contact details found in bio or external URL
- Automation likelihood based on bio clues and posting cadence

## Setup
1. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a file `usernames.txt` with one Instagram username per line.
   - The sample file is only placeholder data; replace it with actual Instagram handles.

## Usage
```bash
python instagram_data_collection.py --usernames usernames.txt --output influencers.csv
```

Optional login for better profile access:
```bash
python instagram_data_collection.py --usernames usernames.txt --output influencers.csv --login YOUR_INSTAGRAM_USERNAME --password YOUR_PASSWORD
```

Optional session reuse with a previously saved session file:
```bash
python instagram_data_collection.py --usernames usernames.txt --output influencers.csv --login YOUR_INSTAGRAM_USERNAME --sessionfile sessionfile.txt
```

> If you see "Profile not found", the username is invalid. If you see a 403 or graphql error, try logging in or using a session file.

## Notes
- The script does not directly collect 2000+ profiles by itself. You need to provide the list of usernames.
- For public Instagram data collection, respect Instagram terms of service and privacy rules.
- Automation detection is heuristic and may be inaccurate.
