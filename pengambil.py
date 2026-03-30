import asyncio
import os
import random
from pyrogram import Client, errors

# --- [ KONFIGURASI ] ---
# Masukkan detail API Anda di sini
API_ID = 32005133
API_HASH = "d14bb5b27de14d96aebc9103c99f43af"
SOURCE_CHAT = -1002337008596
# -----------------------

# Nama session harus sama dengan file .session yang Anda punya
app = Client("userbot_turbo_session", api_id=API_ID, api_hash=API_HASH)

async def main():
    async with app:
        print("\n[*] Menghubungkan ke Akun Admin...")
        
        # Folder download di dalam container
        download_path = "downloads"
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        batch_count = 0
        print("[*] Memulai pemindaian media di VVIP SUPER MALAY...\n")

        async for message in app.get_chat_history(SOURCE_CHAT):
            if message.video or message.document:
                msg_id = message.id
                file_name = f"{download_path}/media_{msg_id}.mp4"

                if os.path.exists(file_name):
                    continue

                try:
                    print(f"[*] [{msg_id}] Sedang mengunduh...")
                    await message.download(file_name=file_name)
                    print(f"[OK] Berhasil disimpan: media_{msg_id}.mp4")
                    
                    batch_count += 1
                    
                    # Jeda Dinamis (5 file cepat, lalu istirahat)
                    if batch_count % 5 == 0:
                        wait = random.randint(180, 300) # Istirahat 3-5 menit
                        print(f"--- Batch Selesai. Istirahat {wait} detik ---")
                    else:
                        wait = random.randint(45, 90) # Jeda antar file 45-90 detik
                        print(f"--- Jeda: {wait} detik ---")
                    
                    await asyncio.sleep(wait)

                except errors.FloodWait as e:
                    print(f"[!] FloodWait: Harus menunggu {e.value} detik.")
                    await asyncio.sleep(e.value)
                except Exception as e:
                    print(f"[!] Error pada ID {msg_id}: {e}")

if __name__ == "__main__":
    app.run(main())
