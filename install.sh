#!/data/data/com.termux/files/usr/bin/bash
# SocialSnap Installer for Termux
# Created by Tanaka Mucheke

echo "================================"
echo "  SocialSnap - Termux Installer"
echo "================================"

# Update packages
pkg update -y && pkg upgrade -y

# Install dependencies
pkg install -y python git termux-api opencv

# Install Python modules
pip install opencv-python-headless numpy colorama requests pillow

# Clone the repo if not already present (optional)
if [ ! -f "TanakaSocialsnap.py" ]; then
    git clone https://github.com/Tanakaprogramminghub/TanakaSocialsnap.git .
fi

echo "Installation complete. Run 'python TanakaSocialsnap.py' to start."
