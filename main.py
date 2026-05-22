import discord
import requests
from discord.ext import tasks

TOKEN = "YOUR_BOT_TOKEN"

SOURCES = [
    {"url": "https://api.example1.com/random", "channel_id": 123456789},
]

posted_urls = set()
intents = discord.Intents.default()
client = discord.Client(intents=intents)

def fetch_media(api_url):
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        url = (
            data.get("file_url") or
            data.get("large_file_url") or
            data.get("url")
        )
        return url
    except:
        return None

@tasks.loop(minutes=30)
async def post_media():
    for source in SOURCES:
        attempts = 0
        while attempts < 5:
            media_url = fetch_media(source["url"])
            if media_url and media_url not in posted_urls:
                posted_urls.add(media_url)
                channel = client.get_channel(source["channel_id"])
                if channel:
                    await channel.send(media_url)
                break
            attempts += 1

@client.event
async def on_ready():
    print(f"✅ Online: {client.user}")
    post_media.start()

client.run(TOKEN)
