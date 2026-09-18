print("Mini URL Shortener")
print("Program started successfully!")

import json
import os
import random
import string
import webbrowser
from datetime import datetime
from urllib.parse import urlparse

DATA_FILE = "urls.json"
def load_data():
        """Load the mapping dict from the JSON file.
          Returns {} if file missing/corrupt."""

        if not os.path.exists(DATA_FILE):
              return {}

        try:
             with open(DATA_FILE, "r", encoding="utf-8") as file:
                   return json.load(file)
        except (json.JSONDecodeError, OSError):
             print("Warning: Could not read stored data.")
             return {}

def save_data(data): 
    """Save URL mappings to the JSON file."""
    try: 
        with open(DATA_FILE, "w", encoding="utf-8") as file:
             json.dump(data, file, indent=4)
    except OSError:
          print("Error: Could not save data.")
    
    

#We don't want someone to enter:hello
def is_valid_url(url): 
     """Check whether a URL has a valid HTTP/HTTPS scheme and hostname."""
     try: 
          parsed = urlparse(url)
          return ( parsed.scheme in ("http", "https") and parsed.netloc != "" ) 
     except ValueError:
          return False

#We want https://www.google.com to become something like:aB72xQ

def generate_code(data, length=6):
    characters = string.ascii_letters + string.digits

    while True:
        code = "".join(random.choices(characters, k=length))

        if code not in data:
            return code    

def find_url(data, url):
    for code, info in data.items():
        if info["url"] == url:
            return code

    return None

def shorten_url(data, url, alias=None):
    """Shorten a URL and store it."""

    if not is_valid_url(url):
        print("Error: Invalid URL.")
        print("Please use a URL starting with http:// or https://")
        return

    if alias:
        if alias in data:
            print(f"Error: Alias '{alias}' already exists.")
            return

        code = alias

    else:
        code = generate_code(data)

    data[code] = {
        "url": url,
        "clicks": 0
    }

    save_data(data)

    print(f"Short URL code: {code}")

 

    #We need resolve abc123 to give:https://www.google.com   

def resolve_url(data, code):
    if code not in data:
        print(f"Error: Short code '{code}' does not exist.")
        return

    data[code]["clicks"] += 1
    save_data(data)

    print(f"Original URL: {data[code]['url']}")
    print(f"Clicks: {data[code]['clicks']}")

    #list required to display all mapping

def list_urls(data):
    if not data:
        print("No shortened URLs found.")
        return

    print("\nStored URLs")
    print("-" * 60)

    for code, info in data.items():
        print(f"{code} -> {info['url']} (Clicks: {info.get('clicks', 0)})")

    print("-" * 60)
    print(f"Total URLs: {len(data)}")
    # create the browser opening

def open_url(data, code):
    if code not in data:
        print(f"Error: Short code '{code}' does not exist.")
        return

    url = data[code]["url"]

    print("Opening URL...")
    webbrowser.open(url)

    #help menu
def print_help():
    print("""
Commands:
shorten <url> -  Shorten a URL.
resolve <code> - Find the original URL.
open <code> -  Open the original URL in a browser.
list - Show all shortened URLs.
help - Show this help menu.
 exit - Exit the program.
""")

def main():
    data = load_data()

    print("=" * 50)
    print("       MINI URL SHORTENER")
    print("=" * 50)

    print("Type 'help' for commands.")
    print("Type 'exit' to quit.")

    while True:
        command = input("\nurl-shortener> ").strip()

        if not command:
            continue

        parts = command.split()
        action = parts[0].lower()

        if action == "exit":
            print("Goodbye!")
            break

        elif action == "help":
            print_help()

        elif action == "list":
            list_urls(data)

        elif action == "shorten":
            if len(parts) != 2:
                print("Usage: shorten <url>")
                continue

            shorten_url(data, parts[1])

        elif action == "resolve":
            if len(parts) != 2:
                print("Usage: resolve <code>")
                continue

            resolve_url(data, parts[1])

        elif action == "open":
            if len(parts) != 2:
                print("Usage: open <code>")
                continue

            open_url(data, parts[1])

        else:
            print("Unknown command.")
            print("Type 'help' for available commands.")

if __name__ == "__main__":
    main()
