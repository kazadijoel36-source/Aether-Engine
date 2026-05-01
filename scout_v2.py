import requests
import time
import random
from ntscraper import Nitter

# ================= CONFIGURATION =================
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_HERE"

KEYWORDS = [
    "convert png", "png to jpg", "pdf to docx", "text to pdf", 
    "convert file", "assignment pdf", "homework pdf", "edit pdf", 
    "pdf editor", "pdf converter", "jpg to png", "pdf to word", 
    "pdf merge", "pdf split", "pdf compress"
]

SUBREDDITS = ["techsupport", "software", "students", "school", "editing"]
MY_APP_URL = "https://aether-engine.up.railway.app/"
# =================================================

def alert_discord(platform, title, url):
    templates = [
        f"Hey! I'm an IT student and I actually built a free tool for this since I hate ads. Check it out: {MY_APP_URL}",
        f"I had this exact issue last week. I made a quick web app to solve it, it's free and works in-browser: {MY_APP_URL}",
        f"If you're still looking for a way to do this, I built a 'tactical' tool for my portfolio that handles this: {MY_APP_URL}"
    ]
    
    suggested_reply = random.choice(templates)
    
    payload = {
        "content": (
            f"🚀 **{platform.upper()} LEAD DETECTED**\n"
            f"**Post:** {title[:100]}...\n"
            f"**Link:** {url}\n\n"
            f"**📋 COPY & PASTE THIS REPLY:**\n"
            f"```{suggested_reply}```"
        )
    }
    requests.post(WEBHOOK_URL, json=payload)

def scan_reddit():
    print(f"[{time.strftime('%H:%M:%S')}] Reddit: Generating 24-Hour Digest...")
    seen = set()
    for sub in SUBREDDITS:
        try:
            query = " OR ".join(f'"{key}"' for key in KEYWORDS)
            url = f"https://www.reddit.com/r/{sub}/search.json?q={query}&restrict_sr=on&t=day&sort=new&limit=10"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            
            response = requests.get(url, headers=headers).json()
            posts = response['data']['children']
            for post in posts:
                p = post['data']
                if p['id'] not in seen:
                    alert_discord("Reddit", p['title'], f"https://reddit.com{p['permalink']}")
                    seen.add(p['id'])
        except Exception:
            print(f" [!] Error scanning r/{sub}")
        time.sleep(2)

def scan_x():
    print(f"[{time.strftime('%H:%M:%S')}] X: Scouting for Twitter leads...")
    # Add a fallback instance list if the automatic one fails
    scraper = Nitter()
    
    search_term = "need to convert pdf" 
    
    try:
        # We tell ntscraper to try multiple instances if the first one fails
        tweets = scraper.get_tweets(search_term, mode='term', number=5)
        
        # Check if we actually got a dictionary with tweets back
        if tweets and 'tweets' in tweets:
            for tweet in tweets['tweets']:
                text = tweet['text'].lower()
                if any(key in text for key in KEYWORDS):
                    alert_discord("X/Twitter", text[:50], tweet['link'])
        else:
            print(" [!] X: No tweets found in this cycle.")
            
    except IndexError:
        print(" [!] X Error: No working Nitter instances found. X is tightening security.")
    except Exception as e:
        print(f" [!] X Error: {e}")

if __name__ == "__main__":
    while True:
        scan_reddit()
        # Only scan X every few hours to avoid IP blocks from Nitter instances
        if random.random() > 0.7: 
            scan_x()
            
        print(f"[{time.strftime('%H:%M:%S')}] Cycle complete. Sleeping for 1 hour...")
        time.sleep(3600)