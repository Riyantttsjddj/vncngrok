import os
import time
import json
import requests

# 1️⃣ Install XFCE4, VNC Server, dan dependensi
os.system("apt update -y && apt install -y xfce4 xfce4-goodies tightvncserver wget unzip curl jq")

# 2️⃣ Konfigurasi VNC Server
os.system("mkdir -p ~/.vnc")
os.system('echo -e "#!/bin/bash\nxrdb $HOME/.Xresources\nstartxfce4 &" > ~/.vnc/xstartup')
os.system("chmod +x ~/.vnc/xstartup")

# 3️⃣ Set password VNC (default: 123456)
os.system('echo -e "123456\n123456\nn" | tightvncserver :1 -geometry 1280x720 -depth 24')

# 4️⃣ Restart VNC Server
os.system("tightvncserver -kill :1")
time.sleep(2)
os.system("tightvncserver :1 -geometry 1280x720 -depth 24")

# 5️⃣ Download & install Ngrok terbaru
os.system("rm -f /usr/local/bin/ngrok")
os.system('wget -O ngrok.zip "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip"')
os.system("unzip ngrok.zip")
os.system("chmod +x ngrok")
os.system("mv ngrok /usr/local/bin/")

# 6️⃣ Login ke Ngrok (Ganti dengan token Anda)
NGROK_TOKEN = "YOUR_NGROK_AUTH_TOKEN"
os.system(f"ngrok authtoken {NGROK_TOKEN}")

# 7️⃣ Jalankan Ngrok untuk VNC (Port 5901)
os.system("nohup ngrok tcp 5901 > /dev/null 2>&1 &")

# 8️⃣ Tunggu Ngrok aktif dan ambil URL
time.sleep(10)

try:
    response = requests.get("http://127.0.0.1:4040/api/tunnels")
    ngrok_data = json.loads(response.text)
    ngrok_url = ngrok_data["tunnels"][0]["public_url"]
    print(f"✅ VNC Server berjalan di port 5901")
    print(f"🔗 URL Akses VNC: {ngrok_url}")
except:
    print("❌ Gagal mendapatkan URL Ngrok! Pastikan Ngrok berjalan dengan benar.")
