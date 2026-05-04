#!/usr/bin/env python3
"""
SocialSnap – Termux OSINT Facial Recognition Tool
Created by Tanaka Mucheke | Ethical Use Only
"""

import os
import sys
import json
import time
import csv
import subprocess
import tempfile
import shutil
import argparse
from datetime import datetime
from pathlib import Path

try:
    import cv2
    import numpy as np
    from colorama import init, Fore, Style
    import requests
    from PIL import Image
    import pickle
    import re
    from urllib.parse import urlparse

    init(autoreset=True)
except ImportError as e:
    print(f"Error: Missing required module. Run: pip install opencv-python-headless numpy colorama requests Pillow")
    sys.exit(1)


# ---------- ASCII Banner ----------
BANNER = f"""
{Fore.CYAN}{Style.BRIGHT}
   ███████╗ ██████╗  ██████╗██╗ █████╗ ██╗     ███████╗███╗   ██╗ █████╗ ██████╗ 
   ██╔════╝██╔═══██╗██╔════╝██║██╔══██╗██║     ██╔════╝████╗  ██║██╔══██╗██╔══██╗
   ███████╗██║   ██║██║     ██║███████║██║     █████╗  ██╔██╗ ██║███████║██████╔╝
   ╚════██║██║   ██║██║     ██║██╔══██║██║     ██╔══╝  ██║╚██╗██║██╔══██║██╔═══╝ 
   ███████║╚██████╔╝╚██████╗██║██║  ██║███████╗███████╗██║ ╚████║██║  ██║██║     
   ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     
{Style.RESET_ALL}
{Fore.YELLOW}      OSINT Facial Recognition Tool - Created by Tanaka Mucheke{Style.RESET_ALL}
{Fore.RED}[!] For educational/ethical use only. Do not use without explicit consent.{Style.RESET_ALL}
"""


# ---------- Configuration ----------
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "google_api_key": "",
    "google_cx": "",
    "use_api": False,
    "output_dir": "output"
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


# ---------- Helper Functions ----------
def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def print_progress(message):
    print(f"{Fore.GREEN}[*] {message}{Style.RESET_ALL}")

def print_success(message):
    print(f"{Fore.CYAN}[+] {message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}[-] {message}{Style.RESET_ALL}")


# ---------- 1. Image Upload & Face Detection ----------
def select_image():
    """Allow user to select image from Termux shared storage."""
    print_progress("Selecting image from gallery...")

    # Create a temporary HTML file for gallery picking
    html = """
    <!DOCTYPE html>
    <html>
    <body>
        <input type="file" id="fileInput" accept="image/*" />
        <script>
            document.getElementById('fileInput').addEventListener('change', function(e) {
                var file = e.target.files[0];
                var reader = new FileReader();
                reader.onload = function(event) {
                    var img = new Image();
                    img.onload = function() {
                        var canvas = document.createElement('canvas');
                        canvas.width = img.width;
                        canvas.height = img.height;
                        var ctx = canvas.getContext('2d');
                        ctx.drawImage(img, 0, 0);
                        var dataUrl = canvas.toDataURL('image/jpeg', 0.9);
                        var link = document.createElement('a');
                        link.download = 'selected_image.jpg';
                        link.href = dataUrl;
                        link.click();
                        setTimeout(function() {
                            window.close();
                        }, 1000);
                    };
                    img.src = event.target.result;
                };
                reader.readAsDataURL(file);
            });
        </script>
    </body>
    </html>
    """

    temp_html = "/sdcard/pick_image.html"
    temp_img = "/sdcard/selected_image.jpg"

    with open(temp_html, "w") as f:
        f.write(html)

    # Open in browser using termux-open
    subprocess.run(["termux-open", temp_html], check=False)
    input(f"{Fore.YELLOW}Select an image from your gallery, then press Enter to continue...{Style.RESET_ALL}")

    if os.path.exists(temp_img):
        image_path = temp_img
        print_success(f"Image saved to {image_path}")
        return image_path
    else:
        print_error("No image selected or file not found.")
        return None

def detect_faces(image_path):
    """Detect faces in an image using OpenCV's Haar Cascade."""
    print_progress("Detecting faces in the image...")

    # Load pre-trained Haar Cascade for face detection
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # Read image
    img = cv2.imread(image_path)
    if img is None:
        print_error("Could not read image. File may be corrupted.")
        return None, None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        print_error("No faces detected in the image.")
        return None, None

    print_success(f"Detected {len(faces)} face(s). Processing the first face...")

    # Extract the first face
    (x, y, w, h) = faces[0]
    face_img = img[y:y+h, x:x+w]

    # Save face image
    output_dir = "face_extracts"
    os.makedirs(output_dir, exist_ok=True)
    face_path = os.path.join(output_dir, f"face_{int(time.time())}.jpg")
    cv2.imwrite(face_path, face_img)

    return face_path, faces

def upload_to_imgur(image_path):
    """Upload image to Imgur and return URL."""
    print_progress("Uploading face to Imgur for reverse search...")

    client_id = "546c25a59c58ad7"  # Public test Client ID
    url = "https://api.imgur.com/3/upload"

    headers = {"Authorization": f"Client-ID {client_id}"}
    with open(image_path, "rb") as img_file:
        files = {"image": img_file}
        try:
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()
            data = response.json()
            return data["data"]["link"]
        except Exception as e:
            print_error(f"Failed to upload: {e}")
            return None


# ---------- 2. Reverse Image Search ----------
def google_reverse_search(image_url):
    """Perform reverse image search using Google's reverse image search."""
    print_progress("Performing reverse image search...")

    search_url = "https://www.google.com/searchbyimage?image_url={}&safe=off".format(image_url)

    # Use requests to fetch search results
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
    }
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        # Extract potential page URLs (simplified example)
        page_content = response.text
        # Find https://www.instagram.com/ p=re. URLs
        social_urls = re.findall(r'(https?://(?:www\.)?(?:instagram|facebook|twitter|x|linkedin|tiktok)\.com/[^\s"\']+)', page_content)
        unique_urls = list(set(social_urls))
        if unique_urls:
            print_success(f"Found {len(unique_urls)} potential social URLs.")
            return unique_urls
        else:
            print_error("No social URLs found.")
            return []
    except Exception as e:
        print_error(f"Reverse image search failed: {e}")
        return []

def extract_username_from_url(url):
    """Extract username from social media URL."""
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    parts = path.split("/")
    if "instagram.com" in url:
        # Instagram usernames are typically after /p/ or directly
        if parts and len(parts) > 0:
            return parts[0]
    elif "facebook.com" in url:
        if parts and len(parts) > 0:
            return parts[0]
    elif "twitter.com" in url or "x.com" in url:
        if parts and len(parts) > 0:
            return parts[0]
    elif "linkedin.com" in url:
        if parts and len(parts) > 0:
            return parts[0]
    elif "tiktok.com" in url:
        if parts and len(parts) > 0:
            return parts[0]
    return None


# ---------- 3. Social Media Lookup ----------
def get_social_accounts_email(username):
    """Attempt to find social accounts using holehe (if available)."""
    try:
        import holehe
        emails = holehe.check_email(f"{username}@example.com")  # Not ideal, but placeholder
        # We'll need a better approach
        return []
    except ImportError:
        print_error("holehe not installed. Install with: pip install holehe")
        return []

def get_social_data_instagram(username):
    """Placeholder for Instagram data extraction."""
    print_progress(f"Fetching Instagram data for {username}...")
    # Use instagram-scraper if available
    # For now, return mock data
    return {
        "username": username,
        "full_name": "Unknown",
        "bio": "No bio found",
        "followers": "N/A",
        "following": "N/A",
        "profile_pic_url": "",
        "external_url": "",
        "location": ""
    }

def search_email_profiles(email):
    """Search for profiles by email using holehe."""
    print_progress(f"Searching for email {email} across platforms...")
    try:
        import holehe
        modules = holehe.core.get_modules()
        results = {}
        for module in modules:
            print(f"Checking {module.__name__}...")
            out = holehe.check_email(email, module)
            if out.get("rateLimit") is False and out.get("exists") is True:
                results[module.__name__] = out
        return results
    except ImportError:
        print_error("holehe not installed for email search.")
        return {}


# ---------- 4. Data Export ----------
def export_json(data, filename="output.json"):
    """Export collected data to JSON."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print_success(f"Data exported to {filename}")

def export_csv(data, filename="output.csv"):
    """Export collected data to CSV."""
    if not data:
        return
    keys = data[0].keys() if isinstance(data, list) else data.keys()
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        if isinstance(data, list):
            writer.writerows(data)
        else:
            writer.writerow(data)
    print_success(f"Data exported to {filename}")


# ---------- 5. CLI & Main ----------
def main():
    clear_screen()
    print(BANNER)
    config = load_config()

    print(f"{Fore.WHITE}Main Menu:{Style.RESET_ALL}")
    print("  1. Scan image for social profiles")
    print("  2. Search by email")
    print("  3. Config")
    print("  4. Exit")
    choice = input(f"{Fore.YELLOW}Select option: {Style.RESET_ALL}").strip()

    if choice == "1":
        image_path = select_image()
        if not image_path:
            return
        face_path, faces = detect_faces(image_path)
        if not face_path:
            return
        # Upload for reverse search
        img_url = upload_to_imgur(face_path)
        if not img_url:
            return
        social_urls = google_reverse_search(img_url)
        # Extract usernames from URLs
        usernames = []
        for url in social_urls:
            username = extract_username_from_url(url)
            if username:
                usernames.append(username)
        if usernames:
            print_success(f"Extracted usernames: {', '.join(usernames)}")
            # Fetch data for each username (simplified)
            all_data = []
            for uname in usernames:
                data = get_social_data_instagram(uname)
                all_data.append(data)
            export_data = all_data
            export_json(export_data)
            export_csv(export_data)
        else:
            print_error("No usernames found.")
    elif choice == "2":
        email = input("Enter email: ").strip()
        if email:
            results = search_email_profiles(email)
            export_json(results)
        else:
            print_error("Invalid email.")
    elif choice == "3":
        print(f"Config file: {CONFIG_FILE}")
        print("Edit it manually to add API keys.")
    elif choice == "4":
        sys.exit(0)
    else:
        print_error("Invalid choice.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\nInterrupted.")
        sys.exit(0)