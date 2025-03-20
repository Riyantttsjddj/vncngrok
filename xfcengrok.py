import os
import time
import json
import requests

# Konfigurasi
VNC_USER = "riyan"
VNC_PASS = "saputra"
NGROK_TOKEN = "1rhrziKSSbVXG9AqYLBvQFwD1CL_538mPmakKPzrn2jiYHRWX"

# 1️⃣ Update & Install XFCE, VNC Server, dan dependensi
print("🛠️ Menginstal XFCE Desktop dan VNC Server...")
os.system("apt update -y && apt install -y xfce4 xfce4-goodies tightvncserver dbus-x11 wget unzip curl jq")

# 2️⃣ Install Browser (Google Chrome & Firefox)
print("🌍 Menginstal Google Chrome dan Firefox...")
os.system("apt install -y firefox")
os.system("wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -")
os.system("echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list")
os.system("apt update -y && apt install -y google-chrome-stable")

# 3️⃣ Tambahkan user baru untuk VNC
print(f"👤 Menambahkan user VNC: {VNC_USER}...")
os.system(f"useradd -m {VNC_USER} || echo 'User {VNC_USER} sudah ada'")
os.system(f"echo '{VNC_USER}:{VNC_PASS}' | chpasswd")

# 4️⃣ Konfigurasi VNC Server
print("🔧 Mengonfigurasi VNC Server...")
vnc_dir = f"/home/{VNC_USER}/.vnc"
os.system(f"mkdir -p {vnc_dir}")
with open(f"{vnc_dir}/xstartup", "w") as f:
    f.write("#!/bin/bash\nxrdb $HOME/.Xresources\nstartxfce4 &\n")
os.system(f"chmod +x {vnc_dir}/xstartup")
os.system(f"chown -R {VNC_USER}:{VNC_USER} {vnc_dir}")

# 5️⃣ Set password VNC secara manual tanpa pexpect
print("🔑 Mengatur password VNC...")
os.system(f'su - {VNC_USER} -c "mkdir -p ~/.vnc && echo {VNC_PASS} | vncpasswd -f > ~/.vnc/passwd && chmod 600 ~/.vnc/passwd"')

# 6️⃣ Mulai ulang VNC Server
print("🚀 Menjalankan VNC Server...")
os.system(f"su - {VNC_USER} -c 'vncserver -kill :1 || echo \"VNC belum berjalan\"'")
os.system(f"su - {VNC_USER} -c 'nohup vncserver :1 -geometry 1280x720 -depth 24 > /dev/null 2>&1 &'")

# 7️⃣ Instalasi Ngrok terbaru
print("🛠️ Menginstal Ngrok...")
os.system("""
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null &&
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list &&
apt update && apt install ngrok -y
""")

# 8️⃣ Login ke Ngrok dengan token
print("🔑 Login ke Ngrok...")
os.system(f"ngrok config add-authtoken {NGROK_TOKEN}")

# 9️⃣ Jalankan Ngrok untuk VNC (Port 5901)
print("🌍 Menjalankan Ngrok untuk VNC...")
os.system("nohup ngrok tcp 5901 > /dev/null 2>&1 &")

# 🔟 Tunggu Ngrok aktif dan ambil URL
print("⏳ Menunggu Ngrok aktif...")
time.sleep(10)

try:
    response = requests.get("http://127.0.0.1:4040/api/tunnels")
    ngrok_data = json.loads(response.text)
    ngrok_url = ngrok_data["tunnels"][0]["public_url"]
    print(f"✅ VNC Server berjalan!")
    print(f"📌 Akses VNC di: {ngrok_url}")
    print(f"👤 Username: {VNC_USER}")
    print(f"🔑 Password: {VNC_PASS}")
    print("🖥️ Desktop: XFCE")
    print("🌍 Browser: Google Chrome & Firefox sudah terinstal")
except:
    print("❌ Gagal mendapatkan URL Ngrok! Pastikan Ngrok berjalan dengan benar.")
