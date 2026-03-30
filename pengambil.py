import asyncio
import os
import random
from pyrogram import Client, errors

# --- [ KONFIGURASI ] ---
# Di Easypanel, pastikan Anda sudah mengisi Environment Variables ini
API_ID = int(os.getenv("API_ID", 32005133))
API_HASH = os.getenv("API_HASH", "d14bb5b27de14d96aebc9103c99f43af")
SESSION_STRING = os.getenv("SESSION_STRING") 
SOURCE_CHAT = -1002337008596 # ID VVIP SUPER MALAY
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
        print("   USERBOT SCRAPER V3 - ANTI PEER INVALID   ")
        print("="*50)
        
        # 1. MEKANISME SINKRONISASI ID (FIX VALUEERROR)
        print(f"[*] Mencoba mengenali ID: {SOURCE_CHAT}...")
        try:
            # Paksa ambil info chat agar session mengenali peer ID ini
            target = await app.get_chat(SOURCE_CHAT)
            print(f"[V] Berhasil Terhubung ke: {target.title}")
        except Exception as e:
            print(f"[!] Gagal resolve ID secara langsung: {e}")
            print("[*] Mencoba pancingan via get_messages...")
            try:
                # Ambil 1 pesan terakhir sebagai pancingan database session
                async for _ in app.get_chat_history(SOURCE_CHAT, limit=1):
                    break
                print("[V] Sinkronisasi ID berhasil via history pancingan.")
            except Exception as e2:
                print(f"[X] Gagal Total: {e2}")
                print("[?] Pastikan akun Anda sudah JOIN di channel tersebut!")
                return

        # 2. PERSIAPAN FOLDER DOWNLOAD
        # Folder ini harus di-mount ke Volume di Easypanel (/app/downloads)
        download_path = "downloads"
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        # 3. PROSES PENGAMBILAN MEDIA
        print("[*] Memulai pemindaian media (Baru -> Lama)...\n")
        
        success_count = 0
        batch_limit = 5 # Download 5 file lalu istirahat

        async for message in app.get_chat_history(SOURCE_CHAT):
            # Hanya ambil Video atau Dokumen (Video sering dikirim sebagai Dokumen)
            if message.video or message.document:
                msg_id = message.id
                file_ext = ".mp4" # Asumsi default video
                file_name = f"{download_path}/media_{msg_id}{file_ext}"

                # Cek jika file sudah ada (Auto-Resume)
                if os.path.exists(file_name):
                    continue

                try:
                    media = message.video or message.document
                    size_mb = media.file_size / (1024 * 1024)

                    print(f"[*] [{msg_id}] Mengunduh {round(size_mb, 2)} MB...")
                    
                    # Proses Download ke Folder Volume
                    await message.download(file_name=file_name)
                    
                    success_count += 1
                    print(f"[OK] Tersimpan: media_{msg_id}.mp4")

                    # JEDA DINAMIS (Agar tidak kena ban/flood)
                    if success_count % batch_limit == 0:
                        wait = random.randint(300, 600) # Istirahat 5-10 menit tiap 5 file
                        print(f"\n--- Batch Selesai. Istirahat {wait} detik (Safety) ---\n")
                    else:
                        wait = random.randint(60, 120) # Jeda antar file 1-2 menit
                        print(f"--- Menunggu {wait} detik ---")
                    
                    await asyncio.sleep(wait)

                except errors.FloodWait as e:
                    print(f"[!] Terlalu Cepat! Telegram meminta istirahat {e.value} detik.")
                    await asyncio.sleep(e.value)
                except Exception as e:
                    print(f"[!] Gagal mengunduh ID {msg_id}: {e}")

        print("\n" + "="*50)
        print(f" SELESAI: Berhasil mengamankan {success_count} file.")
        print("="*50)

if __name__ == "__main__":
    try:
        app.run(main())
    except Exception as e:
        print(f"[FATAL] Script berhenti: {e}")
