from telethon import TelegramClient
from dotenv import load_dotenv
import os
load_dotenv()
tapiid = os.getenv("tapiid")
Thash = os.getenv("Thash")

api_id = int(tapiid)
api_hash = Thash

client = TelegramClient("session", api_id, api_hash)


async def main():
    channels = [
        "warmonitors",
        "DDGeopolitics",
        "FinancialJuice",
        "medmannews",
        "intelslava",
        "boris_rozhin",
        "nexta_live",
        "rnintel",
        "TheIslanderNews",
        "Slavyangrad",
        "geopolitics_prime",
        "worldpravda"
]

    for ch in channels:
        messages = await client.get_messages(ch, limit=1)
        for msg in messages:
            print(f"[{ch}] {msg.text}")
with client:
    client.loop.run_until_complete(main())