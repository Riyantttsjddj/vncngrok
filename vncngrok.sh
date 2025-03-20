#!/bin/bash

# 1️⃣ Update sistem & install XFCE + VNC Server
export DEBIAN_FRONTEND=noninteractive
apt update -y && apt install -y xfce4 xfce4-goodies tightvncserver wget unzip curl jq

# 2️⃣ Konfigurasi VNC Server
mkdir -p ~/.vnc
echo -e "#!/bin/bash\nxrdb \$HOME/.Xresources\nstartxfce4 &" > ~/.vnc/xstartup
chmod +x ~/.vnc/xstartup

# 3️⃣ Set password VNC (default: 123456)
echo -e "123456\n123456\nn" | tightvncserver :1 -geometry 1280x720 -depth 24

# 4️⃣ Restart VNC Server
tightvncserver -kill :1
sleep 2
tightvncserver :1 -geometry 1280x720 -depth 24

# 5️⃣ Download & install Ngrok terbaru
rm -f /usr/local/bin/ngrok
wget -O ngrok.zip "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip"
unzip ngrok.zip
chmod +x ngrok
mv ngrok /usr/local/bin/

# 6️⃣ Login ke Ngrok (Ganti dengan token Anda)
ngrok authtoken YOUR_NGROK_AUTH_TOKEN

# 7️⃣ Jalankan Ngrok untuk VNC (Port 5901)
nohup ngrok tcp 5901 > /dev/null 2>&1 &

# 8️⃣ Tunggu Ngrok aktif dan ambil URL
sleep 10
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url')

# 9️⃣ Tampilkan URL Ngrok
echo "✅ VNC Server berjalan di port 5901"
echo "🔗 URL Akses VNC: $NGROK_URL"
