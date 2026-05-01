import requests
import time

# YOUR DISCORD WEBHOOK
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1499810972012122132/99EgCU9XCmqq7PUf4nisursx2ACNy51NnX0WfZgb52TdwS5fvEajStDYJarcEpvEhIZx"

# The keywords that equal R1k/month leads
KEYWORDS = ["convert png", "png to jpg", "pdf to docx", "text to pdf", "convert file", "assignment pdf", "homework pdf", "edit pdf", "pdf editor", "pdf converter", "jpg to png", "jpeg to png", "png to jpeg", "pdf to word", "txt to pdf", "thesis pdf", "research paper pdf", "essay pdf", "report pdf", "pdf formatting", "pdf layout", "pdf to doc", "doc to pdf", "pdf to text", "text to pdf", "pdf merge", "pdf split", "pdf compress", "pdf resize",]

# List of subreddits to monitor
SUBREDDITS = ["techsupport", "software", "students", "school", "editing"]

def alert_discord(title, reddit_url):
    # CHANGE THIS TO YOUR NEW RAILWAY URL
    my_app_url = "https://aether-engine.up.railway.app/" 
    
    payload = {
        "content": f"🚀 **AETHER LEAD DETECTED**\n**Issue:** {title}\n**Link:** https://reddit.com{reddit_url}\n**Send them here:** {my_app_url}"
    }
    requests.post(WEBHOOK_URL, json=payload)

def scan_reddit():
    print("Aether Scout V2 (Keyless) is scanning for digital matter...")
    seen_posts = set()

    while True:
        for sub in SUBREDDITS:
            try:
                url = f"https://www.reddit.com/r/{sub}/new.json?limit=10"
                # This expanded header mimics a real Chrome browser on Windows
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'application/json',
                    'Accept-Language': 'en-US,en;q=0.5',
                }
                
                response = requests.get(url, headers=headers)
                
                # Add this check to see exactly what Reddit is saying
                if response.status_code != 200:
                    print(f"Reddit blocked r/{sub} with Status: {response.status_code}")
                    continue

                data = response.json()
                posts = data['data']['children']
                # ... rest of your code ...
                
                for post in posts:
                    post_data = post['data']
                    post_id = post_data['id']
                    title = post_data['title'].lower()
                    permalink = post_data['permalink']

                    if post_id not in seen_posts:
                        if any(key in title for key in KEYWORDS):
                            print(f"Match found in r/{sub}: {post_data['title']}")
                            alert_discord(post_data['title'], permalink)
                        seen_posts.add(post_id)

            except Exception as e:
                print(f"Connection glitch on r/{sub}: {e}")
            
            # Brief pause between subreddits to stay under the radar
            time.sleep(5) 
        
        print("Cycle complete. Cooling down for 60 seconds...")
        time.sleep(60) # Scan every minute

if __name__ == "__main__":
    scan_reddit()