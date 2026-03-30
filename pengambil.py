import asyncio
import os
import random
from pyrogram import Client, errors

# --- [ KONFIGURASI ] ---
API_ID = int(os.getenv("API_ID", 32005133))
API_HASH = os.getenv("API_HASH", "d14bb5b27de14d96aebc9103c99f43af")
SESSION_STRING = os.getenv("SESSION_STRING") 
TARGET_ID = -1002337008596 
# -----------------------

app = Client(
    "userbot_scraper",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

async def main():
    async with app:
        print("\n" + "="*50)
        print("   USERBOT V4 - DIALOG DISCOVERY MODE   ")
        print("="*50)
        
        target_chat = None

        # 1. SEARCHING VIA DIALOGS (METODE PALING AMPUH UNTUK USERBOT)
        print("[*] Mencari channel di daftar chat akun Anda...")
        try:
            async for dialog in app.get_dialogs():
                if dialog.chat.id == TARGET_ID:
                    target_chat = dialog.chat
                    print(f"[V] Channel Ditemukan: {target_chat.title}")
                    break
            
            if not target_chat:
                print("[!] ID tidak ditemukan di daftar chat. Mencoba akses langsung...")
                target_chat = await app.get_chat(TARGET_ID)
                print(f"[V] Berhasil akses via get_chat: {target_chat.title}")

        except Exception as e:
            print(f"[X] Gagal sinkronisasi: {e}")
            print("[?] Pastikan akun sudah JOIN dan scroll history di HP dulu.")
            return

        # 2. PERSIAPAN FOLDER
        download_path = "downloads"
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        # 3. DOWNLOAD MEDIA
        print(f"[*] Memulai pengambilan dari {target_chat.title}...\n")
        
        success_count = 0
        async for message in app.get_chat_history(target_chat.id):
            if message.video or message.document:
                msg_id = message.id
                file_name = f"{download_path}/media_{msg_id}.mp4"

                if os.path.exists(file_name):
                    continue

                try:
                    media = message.video or message.document
                    # Lewati jika ukuran file tidak wajar (opsional)
                    if not media: continue
                    
                    size_mb = media.file_size / (1024 * 1024)
                    print(f"[*] [{msg_id}] Mengunduh {round(size_mb, 2)} MB...")
                    
                    await message.download(file_name=file_name)
                    
                    success_count += 1
                    print(f"[OK] Tersimpan: media_{msg_id}.mp4")

                    # Jeda Keamanan (Batch 5 file)
                    if success_count % 5 == 0:
                        wait = random.randint(300, 600)
                        print(f"\n--- Batch Selesai. Istirahat {wait} detik ---\n")
                    else:
                        wait = random.randint(60, 120)
                        print(f"--- Jeda: {wait} detik ---")
                    
                    await asyncio.sleep(wait)

                except errors.FloodWait as e:
                    print(f"[!] FloodWait: Tidur {e.value} detik.")
                    await asyncio.sleep(e.value)
                except Exception as e:
                    print(f"[!] Error ID {msg_id}: {e}")

        print(f"\n--- Selesai! Berhasil mengamankan {success_count} file ---")

if __name__ == "__main__":
    app.run(main())
