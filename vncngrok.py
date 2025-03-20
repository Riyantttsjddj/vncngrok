import os
import time
import json
import requests
import subprocess

# Username dan Password untuk VNC
VNC_USER = "riyan"
VNC_PASS = "saputra"

# 1️⃣ Update & Install GNOME, VNC Server, dan dependensi
os.system("apt update -y && apt install -y ubuntu-desktop tightvncserver dbus-x11 wget unzip curl jq expect gnome-terminal")

# 2️⃣ Install Browser (Google Chrome & Firefox)
os.system("apt install -y firefox")  # Install Firefox
os.system("wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -")
os.system("echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list")
os.system("apt update -y && apt install -y google-chrome-stable")  # Install Google Chrome

# 3️⃣ Tambahkan user baru untuk VNC
os.system(f"useradd -m {VNC_USER} || echo 'User {VNC_USER} sudah ada'")
os.system(f"echo '{VNC_USER}:{VNC_PASS}' | chpasswd")

# 4️⃣ Konfigurasi VNC Server
vnc_dir = f"/home/{VNC_USER}/.vnc"
os.system(f"mkdir -p {vnc_dir}")
xstartup_path = f"{vnc_dir}/xstartup"

# Buat file xstartup agar GNOME berjalan dengan benar
xstartup_script = """#!/bin/bash
xrdb $HOME/.Xresources
gnome-session &
"""
with open(xstartup_path, "w") as f:
    f.write(xstartup_script)

os.system(f"chmod +x {xstartup_path}")
os.system(f"chown -R {VNC_USER}:{VNC_USER} {vnc_dir}")

# 5️⃣ Set password VNC menggunakan expect agar otomatis
expect_script = f"""
spawn su - {VNC_USER} -c "vncpasswd"
expect "Password:"
send "{VNC_PASS}\\r"
expect "Verify:"
send "{VNC_PASS}\\r"
expect "Would you like to enter a view-only password (y/n)?"
send "n\\r"
expect eof
"""
with open("/tmp/vnc_passwd.exp", "w") as f:
    f.write(expect_script)

os.system("chmod +x /tmp/vnc_passwd.exp")
os.system("expect /tmp/vnc_passwd.exp")
os.system("rm -f /tmp/vnc_passwd.exp")

# 6️⃣ Hentikan VNC jika berjalan sebelumnya, lalu jalankan ulang
os.system(f'su - {VNC_USER} -c "vncserver -kill :1 || echo VNC belum berjalan"')
os.system(f'su - {VNC_USER} -c "nohup vncserver :1 -geometry 1280x720 -depth 24 > /dev/null 2>&1 &"')

# 7️⃣ Instalasi Ngrok terbaru
os.system("""
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null &&
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list &&
apt update &&
apt install ngrok -y
""")

# 8️⃣ Login ke Ngrok menggunakan config terbaru
os.system("ngrok config add-authtoken 1rhrziKSSbVXG9AqYLBvQFwD1CL_538mPmakKPzrn2jiYHRWX")

# 9️⃣ Jalankan Ngrok untuk VNC (Port 5901)
os.system("nohup ngrok tcp 5901 > /dev/null 2>&1 &")

# 🔟 Tunggu Ngrok aktif dan ambil URL
time.sleep(10)

try:
    response = requests.get("http://127.0.0.1:4040/api/tunnels")
    ngrok_data = json.loads(response.text)
    ngrok_url = ngrok_data["tunnels"][0]["public_url"]
    print(f"✅ VNC Server berjalan di port 5901 dengan username '{VNC_USER}' dan password '{VNC_PASS}'")
    print(f"🔗 URL Akses VNC: {ngrok_url}")
    print("🖥️ Desktop: GNOME (Ubuntu Desktop)")
    print("🌍 Browser: Google Chrome & Firefox terinstal")
except:
    print("❌ Gagal mendapatkan URL Ngrok! Pastikan Ngrok berjalan dengan benar.")
