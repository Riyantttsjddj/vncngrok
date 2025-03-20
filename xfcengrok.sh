#!/bin/bash

# Konfigurasi
VNC_USER="riyan"
VNC_PASS="saputra"
NGROK_TOKEN="1rhrziKSSbVXG9AqYLBvQFwD1CL_538mPmakKPzrn2jiYHRWX"

# 1️⃣ Update & Install XFCE, VNC Server, dan dependensi
echo "🛠️ Menginstal XFCE Desktop dan VNC Server..."
apt update -y && apt install -y xfce4 xfce4-goodies tightvncserver dbus-x11 wget unzip curl jq

# 2️⃣ Install Browser (Google Chrome & Firefox)
echo "🌍 Menginstal Google Chrome dan Firefox..."
apt install -y firefox
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list
apt update -y && apt install -y google-chrome-stable

# 3️⃣ Tambahkan user baru untuk VNC
echo "👤 Menambahkan user VNC: $VNC_USER..."
useradd -m $VNC_USER || echo "User $VNC_USER sudah ada"
echo "$VNC_USER:$VNC_PASS" | chpasswd

# 4️⃣ Konfigurasi VNC Server
echo "🔧 Mengonfigurasi VNC Server..."
VNC_DIR="/home/$VNC_USER/.vnc"
mkdir -p $VNC_DIR
echo -e "#!/bin/bash\nxrdb \$HOME/.Xresources\nstartxfce4 &" > $VNC_DIR/xstartup
chmod +x $VNC_DIR/xstartup
chown -R $VNC_USER:$VNC_USER $VNC_DIR

# 5️⃣ Set password VNC
echo "🔑 Mengatur password VNC..."
su - $VNC_USER -c "mkdir -p ~/.vnc && echo $VNC_PASS | vncpasswd -f > ~/.vnc/passwd && chmod 600 ~/.vnc/passwd"

# 6️⃣ Mulai ulang VNC Server
echo "🚀 Menjalankan VNC Server..."
su - $VNC_USER -c "vncserver -kill :1 || echo 'VNC belum berjalan'"
su - $VNC_USER -c "nohup vncserver :1 -geometry 1280x720 -depth 24 > /dev/null 2>&1 &"

# 7️⃣ Instalasi Ngrok terbaru
echo "🛠️ Menginstal Ngrok..."
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list
apt update && apt install ngrok -y

# 8️⃣ Login ke Ngrok dengan token
echo "🔑 Login ke Ngrok..."
ngrok config add-authtoken $NGROK_TOKEN

# 9️⃣ Jalankan Ngrok untuk VNC (Port 5901)
echo "🌍 Menjalankan Ngrok untuk VNC..."
nohup ngrok tcp 5901 > /dev/null 2>&1 &

# 🔟 Tunggu Ngrok aktif dan ambil URL
echo "⏳ Menunggu Ngrok aktif..."
sleep 10

NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url')

if [ -n "$NGROK_URL" ]; then
    echo "✅ VNC Server berjalan!"
    echo "📌 Akses VNC di: $NGROK_URL"
    echo "👤 Username: $VNC_USER"
    echo "🔑 Password: $VNC_PASS"
    echo "🖥️ Desktop: XFCE"
    echo "🌍 Browser: Google Chrome & Firefox sudah terinstal"
else
    echo "❌ Gagal mendapatkan URL Ngrok! Pastikan Ngrok berjalan dengan benar."
fi
