import asyncio
import os
import random
from pyrogram import Client, errors

# --- [ KONFIGURASI ] ---
API_ID = int(os.getenv("API_ID", 32005133))
API_HASH = os.getenv("API_HASH", "d14bb5b27de14d96aebc9103c99f43af")
SESSION_STRING = os.getenv("SESSION_STRING") # Diambil dari Easypanel Config
SOURCE_CHAT = -1002337008596
# -----------------------

# Inisialisasi menggunakan String, bukan File
app = Client(
    "userbot_scraper",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

async def main():
    async with app:
        print("\n[*] Userbot Berhasil Login via Session String...")
        
        download_path = "downloads"
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        batch_count = 0
        async for message in app.get_chat_history(SOURCE_CHAT):
            if message.video or message.document:
                msg_id = message.id
                file_name = f"{download_path}/media_{msg_id}.mp4"

                if os.path.exists(file_name):
                    continue

                try:
                    print(f"[*] [{msg_id}] Mengunduh...")
                    await message.download(file_name=file_name)
                    print(f"[OK] Berhasil: media_{msg_id}.mp4")
                    
                    batch_count += 1
                    
                    # Jeda Dinamis (Mode Turbo Terukur)
                    if batch_count % 5 == 0:
                        wait = random.randint(180, 300)
                        print(f"--- Batch Selesai. Istirahat {wait} detik ---")
                    else:
                        wait = random.randint(45, 90)
                        print(f"--- Jeda: {wait} detik ---")
                    
                    await asyncio.sleep(wait)

                except errors.FloodWait as e:
                    print(f"[!] FloodWait: {e.value} detik.")
                    await asyncio.sleep(e.value)
                except Exception as e:
                    print(f"[!] Error ID {msg_id}: {e}")

if __name__ == "__main__":
    app.run(main())
