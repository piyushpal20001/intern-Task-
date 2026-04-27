import instaloader
import sys

def save_instagram_session(username: str, password: str, session_filename: str = "instagram_session.txt") -> None:
    """Save an Instagram session to a file for reuse."""
    loader = instaloader.Instaloader(sleep=True, quiet=True)
    
    try:
        print(f"Logging in as {username}...")
        loader.login(username, password)
        loader.save_session_to_file(filename=session_filename)
        print(f"✓ Session saved to {session_filename}")
        print(f"Now run:")
        print(f"  python instagram_data_collection.py --usernames usernames.txt --output influencers.csv --login {username} --sessionfile {session_filename}")
    except instaloader.exceptions.LoginException as exc:
        print(f"Login failed: {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"Error saving session: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python save_session.py <instagram_username> <instagram_password>")
        print("\nExample:")
        print("  python save_session.py piyush piyushpal123")
        print("\nReplace 'piyush' with your real Instagram username")
        print("Replace 'piyushpal123' with your real Instagram password")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    
    if username == "your_instagram_username" or password == "your_password":
        print("ERROR: You must replace the placeholder values with your actual Instagram credentials!")
        print("\nUsage: python save_session.py <your_real_username> <your_real_password>")
        print("\nExample (use YOUR credentials):")
        print("  python save_session.py piyush piyushpal123")
        sys.exit(1)
    
    save_instagram_session(username, password)
