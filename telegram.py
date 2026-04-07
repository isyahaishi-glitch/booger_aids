from telethon import TelegramClient
from dotenv import load_dotenv
import os
load_dotenv()
tapiid = int(os.getenv("tapiid"))
Thash = os.getenv("Thash")

api_id = tapiid
api_hash = Thash

client = TelegramClient("session", api_id, api_hash)

async def main():
    messages = await client.get_messages("somechannel", limit=10)
    
    for msg in messages:
        print(msg.text)

with client:
    client.loop.run_until_complete(main())