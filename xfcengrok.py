import os
import time
import json
import requests
import subprocess

# Konfigurasi
VNC_USER = "riyan"
VNC_PASS = "saputra"
NGROK_TOKEN = "1rhrziKSSbVXG9AqYLBvQFwD1CL_538mPmakKPzrn2jiYHRWX"

# Fungsi untuk mengeksekusi perintah shell
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✅ {command}\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {command}\n{e.stderr}")

# 1️⃣ Update & Install XFCE, VNC Server, dan dependensi
print("🛠️ Menginstal XFCE Desktop dan VNC Server...")
run_command("apt update -y && apt install -y xfce4 xfce4-goodies tightvncserver dbus-x11 wget unzip curl jq sudo firefox")

# 2️⃣ Install Browser (Google Chrome)
print("🌍 Menginstal Google Chrome...")
run_command("wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -")
run_command('echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list')
run_command("apt update -y && apt install -y google-chrome-stable")

# 3️⃣ Tambahkan user baru untuk VNC (Superuser dengan Password)
print(f"👤 Menambahkan user VNC: {VNC_USER}...")
run_command(f"useradd -m -G sudo {VNC_USER}")
run_command(f"echo '{VNC_USER}:{VNC_PASS}' | chpasswd")

# 4️⃣ Konfigurasi VNC Server
print(f"🔧 Mengonfigurasi VNC Server untuk {VNC_USER}...")
VNC_DIR = f"/home/{VNC_USER}/.vnc"
run_command(f"mkdir -p {VNC_DIR}")
run_command(f'echo -e "#!/bin/bash\nxrdb $HOME/.Xresources\nstartxfce4 &" > {VNC_DIR}/xstartup')
run_command(f"chmod +x {VNC_DIR}/xstartup")
run_command(f"chown -R {VNC_USER}:{VNC_USER} {VNC_DIR}")

# 5️⃣ Set password VNC
print("🔑 Mengatur password VNC...")
run_command(f"su - {VNC_USER} -c 'echo {VNC_PASS} | vncpasswd -f > ~/.vnc/passwd && chmod 600 ~/.vnc/passwd'")

# 6️⃣ Mulai ulang VNC Server
print("🚀 Menjalankan VNC Server...")
run_command(f"su - {VNC_USER} -c 'vncserver -kill :1 || echo VNC belum berjalan'")
run_command(f"su - {VNC_USER} -c 'nohup vncserver :1 -geometry 1280x720 -depth 24 > /dev/null 2>&1 &'")

# 7️⃣ Instalasi Ngrok terbaru
print("🛠️ Menginstal Ngrok...")
run_command("curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null")
run_command('echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list')
run_command("apt update && apt install ngrok -y")

# 8️⃣ Login ke Ngrok dengan token
print("🔑 Login ke Ngrok...")
run_command(f"ngrok config add-authtoken {NGROK_TOKEN}")

# 9️⃣ Jalankan Ngrok untuk VNC (Port 5901)
print("🌍 Menjalankan Ngrok untuk VNC...")
run_command("nohup ngrok tcp 5901 > /dev/null 2>&1 &")

# 🔟 Tunggu Ngrok aktif dan ambil URL
print("⏳ Menunggu Ngrok aktif...")
time.sleep(10)

# Ambil URL Ngrok
try:
    response = requests.get("http://127.0.0.1:4040/api/tunnels")
    ngrok_data = json.loads(response.text)
    ngrok_url = ngrok_data["tunnels"][0]["public_url"]
    print(f"✅ VNC Server berjalan di port 5901 dengan username '{VNC_USER}' dan password '{VNC_PASS}'")
    print(f"🔗 URL Akses VNC: {ngrok_url}")
except Exception as e:
    print(f"❌ Gagal mendapatkan URL Ngrok! Pastikan Ngrok berjalan dengan benar. {str(e)}")
