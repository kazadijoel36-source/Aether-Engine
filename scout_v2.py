import requests
import time
import random

# ================= CONFIGURATION =================
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1499810972012122132/99EgCU9XCmqq7PUf4nisursx2ACNy51NnX0WfZgb52TdwS5fvEajStDYJarcEpvEhIZx"

# The keywords that equal R1k/month leads
KEYWORDS = [
    "convert png", "png to jpg", "pdf to docx", "text to pdf", 
    "convert file", "assignment pdf", "homework pdf", "edit pdf", 
    "pdf editor", "pdf converter", "jpg to png", "pdf to word", 
    "pdf merge", "pdf split", "pdf compress"
]

SUBREDDITS = ["techsupport", "software", "students", "school", "editing"]

MY_APP_URL = "https://aether-engine.up.railway.app/"
# =================================================

def alert_discord(title, reddit_url):
    # Rotating human-sounding templates
    templates = [
        f"Hey! I'm an IT student and I actually built a free tool for this since I hate ads. Check it out: {MY_APP_URL}",
        f"I had this exact issue last week. I made a quick web app to solve it, it's free and works in-browser: {MY_APP_URL}",
        f"If you're still looking for a way to do this, I built a 'tactical' tool for my portfolio that handles this: {MY_APP_URL}",
        f"I actually developed a site that does this for free because I needed it for my own assignments. Hope it helps! {MY_APP_URL}"
    ]
    
    suggested_reply = random.choice(templates)
    
    payload = {
        "content": (
            f"🚀 **AETHER LEAD DETECTED**\n"
            f"**Issue:** {title}\n"
            f"**Link:** https://reddit.com{reddit_url}\n\n"
            f"**📋 COPY & PASTE THIS REPLY:**\n"
            f"```{suggested_reply}```"
        )
    }
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Discord Webhook Error: {e}")

def run_digest():
    print(f"\n[{time.strftime('%H:%M:%S')}] Aether Engine: Generating 24-Hour Lead Digest...")
    
    # We use a set to avoid sending the same post twice if it appears in different searches
    seen_in_this_run = set()

    for sub in SUBREDDITS:
        try:
            # We search for our keywords using the 'OR' operator to get everything at once
            query = " OR ".join(f'"{key}"' for key in KEYWORDS)
            url = f"https://www.reddit.com/r/{sub}/search.json?q={query}&restrict_sr=on&t=day&sort=new&limit=25"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept': 'application/json'
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                posts = data['data']['children']
                
                if not posts:
                    print(f" -> No new matches in r/{sub}")
                    continue

                for post in posts:
                    pdata = post['data']
                    pid = pdata['id']
                    
                    if pid not in seen_in_this_run:
                        print(f" [+] Match found in r/{sub}: {pdata['title']}")
                        alert_discord(pdata['title'], pdata['permalink'])
                        seen_in_this_run.add(pid)
                        time.sleep(1) # Small delay to avoid Discord spam
            else:
                print(f" [!] Reddit blocked r/{sub} (Status {response.status_code})")

        except Exception as e:
            print(f" [X] Error scanning r/{sub}: {e}")
            
        time.sleep(3) # Stay under the radar between subreddits

    print(f"[{time.strftime('%H:%M:%S')}] Digest complete. Sleeping for 1 hour...")

if __name__ == "__main__":
    while True:
        run_digest()
        # We wait 1 hour between "Deep Searches" to keep the IP safe
        time.sleep(3600)

        from ntscraper import Nitter

def scan_x():
    print(f"[{time.strftime('%H:%M:%S')}] Aether Engine: Scouting X (Twitter) for leads...")
    scraper = Nitter()
    
    # We pick one high-value term at a time to stay under the radar
    search_term = "convert pdf help" 
    
    try:
        # 'term' is the search, 'mode' is trend/hashtag/term, 'number' is how many tweets
        tweets = scraper.get_tweets(search_term, mode='term', number=5)
        
        for tweet in tweets['tweets']:
            link = tweet['link']
            text = tweet['text']
            
            # Check if any of your keywords are in the tweet
            if any(key in text.lower() for key in KEYWORDS):
                print(f" [+] X Match found: {text[:50]}...")
                alert_discord(f"X LEAD: {text[:100]}", link)
                
    except Exception as e:
        print(f" [X] X Scouting Error: {e}")