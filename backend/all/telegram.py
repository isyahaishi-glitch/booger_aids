from telethon import TelegramClient
from dotenv import load_dotenv
import asyncio
import os
from URL import channels
load_dotenv()
from flask import Flask,jsonify
from flask_cors import CORS
import threading
from telethon.errors import SessionPasswordNeededError

app = Flask(__name__)
CORS(app)
tapiid = os.getenv("tapiid")
Thash = os.getenv("Thash")
notelp = os.getenv("notelp")
api_id = int(tapiid)
client = TelegramClient("userbot", api_id, Thash)
last_seen = {ch: None for ch in channels}
latest_messages : dict[str, dict] = {}

os.makedirs("downloads", exist_ok=True)


async def poll(interval: int = 60):
    print(f"Polling every {interval}s …")

    while True:
        for ch in channels:
            try:
                messages = await client.get_messages(ch, limit=1)
                for msg in reversed(messages):
                    if last_seen[ch] is not None and msg.id <= last_seen[ch]:
                        continue
                    if msg.text:
                        print(f"[{ch}] {msg.text}\n")

                    latest_messages[ch] = {
                        "text": msg.text,
                        "date": str(msg.date),
                        "id": msg.id,
                        "channel": ch
                    }

                    # if msg.photo:
                    #     file_path = await msg.download_media(file=f"downloads/{ch}_")
                    #     print(f"[{ch}] Photo saved: {file_path}\n")

                    # Update the last seen ID
                    if last_seen[ch] is None or msg.id > last_seen[ch]:
                        last_seen[ch] = msg.id

            except Exception as e:
                print(f"[{ch}] Error: {e}")

        await asyncio.sleep(interval)


async def telegram_main(phone: str):
    while True:
        try:
            await client.start(phone=phone)

            # ✅ Fix 4: handle accounts protected by a password (2FA)
            if not await client.is_user_authorized():
                raise RuntimeError("Client not authorized after start()")

        except SessionPasswordNeededError:
            password = input("2FA password: ")
            await client.sign_in(password=password)

        try:
            await poll(interval=60)
        except (ConnectionError, OSError) as e:
            print(f"Connection lost: {e} — reconnecting in 5 s…")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}")
            break



def start_telegram_thread():
    """Run the asyncio event loop for Telethon in a separate thread."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(telegram_main(notelp))


@app.route("/telegram")
def route_telegram():
    return jsonify(list(latest_messages.values()))


if __name__ == "__main__":
    t = threading.Thread(target=start_telegram_thread , daemon=True)
    t.start()
    app.run(debug=False, port=5002)