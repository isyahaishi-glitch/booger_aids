from telethon import TelegramClient
from dotenv import load_dotenv
import asyncio
import os
from URL import channels
load_dotenv()

tapiid = os.getenv("tapiid")
Thash = os.getenv("Thash")
notelp = os.getenv("notelp")
api_id = int(tapiid)

client = TelegramClient("userbot", api_id, Thash)



last_seen = {ch: None for ch in channels}

os.makedirs("downloads", exist_ok=True)


async def poll(interval: int = 60):
    """Fetch new messages from all channels every `interval` seconds."""
    print("Bot started. Polling every", interval, "seconds...")

    while True:
        for ch in channels:
            try:
                messages = await client.get_messages(ch, limit=1)

                # Reverse so we process oldest-first
                for msg in reversed(messages):
                    # Skip already-seen messages
                    if last_seen[ch] is not None and msg.id <= last_seen[ch]:
                        continue

                    if msg.text:
                        print(f"[{ch}] {msg.text}\n")

                    if msg.photo:
                        file_path = await msg.download_media(file=f"downloads/{ch}_")
                        print(f"[{ch}] Photo saved: {file_path}\n")

                    # Update the last seen ID
                    if last_seen[ch] is None or msg.id > last_seen[ch]:
                        last_seen[ch] = msg.id

            except Exception as e:
                print(f"[{ch}] Error: {e}")

        await asyncio.sleep(interval)


async def main(notelp):
    while True:
        try:
            await client.start(phone=notelp)
            await poll(interval=60)
        except (ConnectionError, OSError) as e:
            print(f"Connection lost: {e} — reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}")
            break


asyncio.run(main(notelp))