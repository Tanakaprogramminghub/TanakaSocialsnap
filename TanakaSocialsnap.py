#!/usr/bin/env python3
"""
Tanaka Social Snap – Simple OSINT Face Tool
Created by Tanaka Mucheke | Use only with permission
"""

import os
import sys
import json
import time
import subprocess
import re
from urllib.parse import urlparse
from datetime import datetime

try:
    import cv2
    from colorama import init, Fore, Style
    import requests

    init(autoreset=True)
except ImportError as e:
    print("ERROR: Run this command first: pip install opencv-python-headless colorama requests")
    sys.exit(1)

# ---------- ASCII Banner ----------
BANNER = f"""
{Fore.RED}{Style.BRIGHT}
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║   ████████╗ █████╗ ███╗   ██╗ █████╗ ██╗  ██╗ █████╗                           ║
║   ╚══██╔══╝██╔══██╗████╗  ██║██╔══██╗██║ ██╔╝██╔══██╗                          ║
║      ██║   ███████║██╔██╗ ██║███████║█████╔╝ ███████║                          ║
║      ██║   ██╔══██║██║╚██╗██║██╔══██║██╔═██╗ ██╔══██║                          ║
║      ██║   ██║  ██║██║ ╚████║██║  ██║██║  ██╗██║  ██║                          ║
║      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝                          ║
║                                                                                ║
║   ███████╗ ██████╗  ██████╗██╗ █████╗ ██╗     ███████╗                         ║
║   ██╔════╝██╔═══██╗██╔════╝██║██╔══██╗██║     ██╔════╝                         ║
║   ███████╗██║   ██║██║     ██║███████║██║     █████╗                           ║
║   ╚════██║██║   ██║██║     ██║██╔══██║██║     ██╔══╝                           ║
║   ███████║╚██████╔╝╚██████╗██║██║  ██║███████╗███████╗                         ║
║   ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝╚══════╝                         ║
║                                                                                ║
║   {Fore.CYAN}{Style.BRIGHT}███████╗███╗   ██╗ █████╗ ██████╗{Fore.RED}{Style.BRIGHT}                                         ║
║   {Fore.CYAN}{Style.BRIGHT}██╔════╝████╗  ██║██╔══██╗██╔══██╗{Fore.RED}{Style.BRIGHT}                                        ║
║   {Fore.CYAN}{Style.BRIGHT}███████╗██╔██╗ ██║███████║██████╔╝{Fore.RED}{Style.BRIGHT}                                        ║
║   {Fore.CYAN}{Style.BRIGHT}╚════██║██║╚██╗██║██╔══██║██╔═══╝{Fore.RED}{Style.BRIGHT}                                         ║
║   {Fore.CYAN}{Style.BRIGHT}███████║██║ ╚████║██║  ██║██║{Fore.RED}{Style.BRIGHT}                                             ║
║   {Fore.CYAN}{Style.BRIGHT}╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝{Fore.RED}{Style.BRIGHT}                                             ║
║                                                                                ║
╠════════════════════════════════════════════════════════════════════════════════╣
║                  Created by Tanaka Mucheke                                      ║
╠════════════════════════════════════════════════════════════════════════════════╣
║         🔴 USE ONLY WITH EXPLICIT PERMISSION 🔴                                 ║
║         ⚠️  UNAUTHORIZED TRACKING IS ILLEGAL  ⚠️                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""

# ---------- Loading Animation ----------
def loading_animation(message, duration=2):
    """Display a spinning animation with Tanaka Mucheke name."""
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{Fore.CYAN}{spinner[i % len(spinner)]} {message} {Fore.MAGENTA}Tanaka Mucheke{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()

def animated_dots(message, duration=1.5):
    """Show animated dots with name."""
    end_time = time.time() + duration
    dots = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{Fore.GREEN}{message}{'.' * (dots % 4)}{' ' * (3 - (dots % 4))} {Fore.MAGENTA}Tanaka Mucheke{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.3)
        dots += 1
    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()

# ---------- Helper Functions ----------
def press_enter(message="👋 Press ENTER to continue..."):
    input(f"{Fore.CYAN}{message}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}✨ Tanaka Mucheke - Tanaka Social Snap ✨{Style.RESET_ALL}")

def clear():
    os.system("clear" if os.name == "posix" else "cls")

# ---------- Step 1: Get the Image ----------
def get_image_path():
    print(f"\n{Fore.GREEN}📸 STEP 1: TELL ME WHERE YOUR PHOTO IS{Style.RESET_ALL}")
    print("Choose a way:")
    print("  1️⃣ I will type the full path (easy with examples)")
    print("  2️⃣ I will copy the photo to this folder and just type its name")
    choice = input(f"{Fore.CYAN}👉 Type 1 or 2: {Style.RESET_ALL}").strip()

    if choice == "1":
        print("\n📂 Examples of full paths on Android:")
        print("   /sdcard/DCIM/Camera/IMG_20240501.jpg")
        print("   /sdcard/Download/selfie.png")
        print("   /sdcard/Pictures/myface.jpg\n")
        path = input("👉 Now type your full path: ").strip()
        if os.path.exists(path):
            return path
        else:
            print(f"{Fore.RED}❌ File not found. Check the path.{Style.RESET_ALL}")
            press_enter("👉 Press ENTER to go back...")
            return None

    elif choice == "2":
        print(f"\n📁 Current folder: {os.getcwd()}")
        print("👉 Copy your photo here, then type its name (e.g., myface.jpg)")
        name = input("👉 Filename: ").strip()
        full = os.path.join(os.getcwd(), name)
        if os.path.exists(full):
            return full
        else:
            print(f"{Fore.RED}❌ '{name}' not in this folder.{Style.RESET_ALL}")
            press_enter("👉 Press ENTER to go back...")
            return None
    else:
        print(f"{Fore.RED}❌ Invalid choice.{Style.RESET_ALL}")
        press_enter("👉 Press ENTER to go back...")
        return None

# ---------- Step 2: Find the Face ----------
def find_face(image_path):
    print(f"\n{Fore.GREEN}🔍 STEP 2: LOOKING FOR A FACE...{Style.RESET_ALL}")

    cascade_file = "haarcascade_frontalface_default.xml"
    if not os.path.exists(cascade_file):
        animated_dots("📥 Downloading face detector", 2)
        url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
        try:
            r = requests.get(url)
            with open(cascade_file, "wb") as f:
                f.write(r.content)
        except:
            print(f"{Fore.RED}❌ No internet. Can't download detector.{Style.RESET_ALL}")
            press_enter()
            return None

    face_cascade = cv2.CascadeClassifier(cascade_file)
    img = cv2.imread(image_path)
    if img is None:
        print(f"{Fore.RED}❌ Can't read that image. Is it a valid photo?{Style.RESET_ALL}")
        press_enter()
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Animate while detecting
    loading_animation("🔎 Scanning for faces", 1.5)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    if len(faces) == 0:
        print(f"{Fore.RED}❌ No face found. Pick a clear, front-facing photo.{Style.RESET_ALL}")
        press_enter()
        return None

    print(f"{Fore.GREEN}✅ Found {len(faces)} face(s)! Using the first one.{Style.RESET_ALL}")
    x, y, w, h = faces[0]
    face_img = img[y:y+h, x:x+w]

    os.makedirs("faces", exist_ok=True)
    face_path = os.path.join("faces", f"face_{int(time.time())}.jpg")
    cv2.imwrite(face_path, face_img)
    return face_path

# ---------- Step 3: Upload to Imgur ----------
def upload_face(face_path):
    print(f"\n{Fore.GREEN}☁️ STEP 3: UPLOADING FACE TO THE WEB...{Style.RESET_ALL}")
    client_id = "546c25a59c58ad7"
    url = "https://api.imgur.com/3/upload"
    headers = {"Authorization": f"Client-ID {client_id}"}
    with open(face_path, "rb") as f:
        files = {"image": f}
        try:
            # Animated upload
            animated_dots("📤 Uploading to Imgur", 2)
            resp = requests.post(url, headers=headers, files=files, timeout=30)
            data = resp.json()
            return data["data"]["link"]
        except:
            print(f"{Fore.RED}❌ Upload failed. Check your internet.{Style.RESET_ALL}")
            press_enter()
            return None

# ---------- Step 4: Open Browser & Ask for Social Links ----------
def get_social_links(imgur_url):
    print(f"\n{Fore.GREEN}🌐 STEP 4: TIME TO SEARCH GOOGLE{Style.RESET_ALL}")
    print(f"Your face is now online at: {Fore.CYAN}{imgur_url}{Style.RESET_ALL}")
    press_enter("👉 Press ENTER to open this link in your browser...")

    # Try to open with termux-open-url, fallback to manual instruction
    try:
        subprocess.run(["termux-open-url", imgur_url], check=False)
    except FileNotFoundError:
        print(f"{Fore.YELLOW}⚠️ 'termux-open-url' not found. Please install termux-api (pkg install termux-api){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}👉 Manually open this URL in your browser: {imgur_url}{Style.RESET_ALL}")

    print(f"""
{Fore.YELLOW}📖 NOW FOLLOW THESE INSTRUCTIONS EXACTLY:{Style.RESET_ALL}
1️⃣ Go to Google Images: https://images.google.com
2️⃣ Click the CAMERA ICON 🔍
3️⃣ Choose "Paste image URL"
4️⃣ Paste the link that I gave you above
5️⃣ Press Search
6️⃣ Look for social media links (Instagram, Facebook, Twitter, TikTok, LinkedIn)

{Fore.CYAN}👉 When you find any social profile URLs, paste them here (one or more, separated by spaces).
👉 If you didn't find any, just press ENTER.{Style.RESET_ALL}
""")
    user_input = input("📎 Paste URLs here: ").strip()
    if not user_input:
        return []
    return user_input.split()

# ---------- Step 5: Extract Usernames ----------
def extract_usernames(urls):
    usernames = []
    for url in urls:
        parts = urlparse(url).path.strip("/").split("/")
        if "instagram.com" in url and parts:
            usernames.append(parts[0])
        elif "facebook.com" in url and parts:
            if parts[0] not in ["profile.php", "people"]:
                usernames.append(parts[0])
        elif "twitter.com" in url or "x.com" in url:
            if parts and parts[0] not in ["i", "home"]:
                usernames.append(parts[0])
        elif "tiktok.com" in url and parts:
            usernames.append(parts[0])
    return list(set(usernames))

# ---------- Step 6: Save Results ----------
def save_results(data):
    os.makedirs("results", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = f"results/tanaka_social_snap_{timestamp}.json"
    with open(json_file, "w") as f:
        json.dump(data, f, indent=4)
    print(f"{Fore.GREEN}✅ Saved report to {json_file}{Style.RESET_ALL}")
    return json_file

# ---------- Main Program with Loop and Animations ----------
def main():
    clear()
    print(BANNER)
    press_enter("👉 Press ENTER to start...")

    while True:
        clear()
        print(BANNER)
        print(f"\n{Fore.WHITE}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📌 MAIN MENU{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}1.{Style.RESET_ALL} Scan image for social profiles")
        print(f"  {Fore.CYAN}2.{Style.RESET_ALL} Exit")
        print(f"{Fore.WHITE}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        choice = input(f"{Fore.GREEN}👉 Select option (1 or 2): {Style.RESET_ALL}").strip()

        if choice == "1":
            img_path = get_image_path()
            if not img_path:
                continue

            face_path = find_face(img_path)
            if not face_path:
                continue

            imgur_url = upload_face(face_path)
            if not imgur_url:
                continue

            social_urls = get_social_links(imgur_url)
            usernames = extract_usernames(social_urls)

            result = {
                "timestamp": datetime.now().isoformat(),
                "original_image": img_path,
                "face_crop": face_path,
                "imgur_url": imgur_url,
                "found_urls": social_urls,
                "usernames": usernames
            }
            save_results(result)

            print(f"\n{Fore.GREEN}🎉 SCAN COMPLETE! 🎉{Style.RESET_ALL}")
            if usernames:
                print(f"📢 Found usernames: {', '.join(usernames)}")
            else:
                print("😕 No usernames found. Maybe the face is not online.")
            print("\n💾 The full report is saved in the 'results' folder.")
            press_enter("👉 Press ENTER to return to menu...")

        elif choice == "2":
            print(f"\n{Fore.YELLOW}👋 Thank you for using Tanaka Social Snap. Goodbye!{Style.RESET_ALL}")
            sys.exit(0)

        else:
            print(f"{Fore.RED}❌ Invalid choice. Please enter 1 or 2.{Style.RESET_ALL}")
            press_enter("👉 Press ENTER to try again...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Exited by user. Goodbye!{Style.RESET_ALL}")
        sys.exit(0)
