
# 📸 Tanaka Social Snap – OSINT Face Tool

**Created by Tanaka Mucheke**  
*For ethical OSINT research only – always obtain explicit permission.*

![Termux](https://img.shields.io/badge/Termux-Android-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue)

> ⚠️ **WARNING** – Unauthorised facial recognition or tracking may violate privacy laws. Use only on your own photos or with written consent.

## 🔍 What does this tool do?

- Takes any photo from your Android gallery (or copied to Termux)
- **Detects and crops the first face** using OpenCV
- **Uploads the cropped face to Imgur** (public but anonymous)
- **Opens the link in your browser** (requires Termux:API) or gives you the URL
- **Guides you to perform a reverse image search** on Google Images
- **Lets you paste any discovered social media URLs** (Instagram, Facebook, Twitter, TikTok, LinkedIn)
- **Extracts usernames** and saves everything to a JSON report

> 📌 **Why manual search?** Google blocks automated reverse image searches. The tool automates the hard parts (face detection, cropping, upload) and leaves the final search to you – the only reliable method on Termux.

## 📦 Installation (One-time setup)

Open **Termux** and run these commands **one by one**:

```bash
# 1. Update packages
pkg update && pkg upgrade -y

# 2. Install required system packages
pkg install -y python git termux-api opencv

# 3. Clone the repository
git clone https://github.com/Tanakaprogramminghub/TanakaSocialsnap.git

# 4. Enter the folder
cd TanakaSocialsnap

# 5. Install Python dependencies
pip install opencv-python-headless colorama requests

# 6. Make the script executable
chmod +x TanakaSocialsnap.py
```

✅ Installation done. Now you can run the tool anytime with python TanakaSocialsnap.py.

💡 Optional but recommended: Run termux-setup-storage once to grant access to your phone’s storage (needed if you use full paths like /sdcard/DCIM/...).

🚀 How to use – Step by step

Start the tool

```bash
python TanakaSocialsnap.py
```

You’ll see a large ASCII banner and a menu.

Main menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 MAIN MENU
  1. Scan image for social profiles
  2. Exit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👉 Select option (1 or 2):
```

Option 1 – Scan image for social profiles

Type 1 and press Enter. Then follow these steps:

1️⃣ Choose how to provide the photo

```
Choose a way:
  1️⃣ I will type the full path (easy with examples)
  2️⃣ I will copy the photo to this folder and just type its name
👉 Type 1 or 2:
```

· Option 1 (full path) – Use this if your photo is somewhere on your shared storage.
    Example path: /sdcard/DCIM/Camera/IMG_20240501.jpg
    ✅ What to do: Type the exact path and press Enter.
    ❌ What NOT to do: Don’t guess the path – you can check the path using a file manager or the ls command. Don’t use spaces in folder names without quotes.
· Option 2 (copy to current folder) – Recommended for beginners.
    ✅ What to do: First copy your photo into ~/TanakaSocialsnap (you can use cp /sdcard/DCIM/Camera/photo.jpg .). Then type only the filename, e.g., photo.jpg.
    ❌ What NOT to do: Don’t forget to copy the file first – otherwise the tool will say “File not found”.

2️⃣ Face detection

The tool will automatically:

· Download a face detector (only the first time – needs internet)
· Scan for faces (you’ll see a spinning animation with your name)
· Crop the first face and save it in the faces/ folder

✅ If successful: ✅ Found 1 face(s)! Using the first one.
❌ If not successful: ❌ No face found.
→ Why? The photo may be too dark, the face not front‑facing, or the image too small. Try another photo.

3️⃣ Upload to Imgur

The cropped face is uploaded to Imgur. You’ll see:

```
☁️ STEP 3: UPLOADING FACE TO THE WEB...
📤 Uploading to Imgur..
Your face is now online at: https://i.imgur.com/XXXXXX.jpg
```

✅ What to do: Wait for the upload to finish.
❌ What NOT to do: Don’t close the tool – the URL is needed for the next step.

4️⃣ Open the link in your browser

The tool will try to open the link automatically using termux-open-url.

· If Termux:API is installed, your browser opens automatically.
· If not, you’ll see a warning and the URL – copy it manually and paste into your browser.

✅ What to do: If the browser opens, you’re good. If not, manually open the link.
❌ What NOT to do: Don’t skip this step – you must do the reverse image search to find social profiles.

5️⃣ Perform reverse image search (manual – most important)

Follow the on‑screen instructions exactly:

1. Go to Google Images (images.google.com) in your browser.
2. Click the camera icon 🔍.
3. Choose “Paste image URL”.
4. Paste the Imgur link (the one you just got).
5. Press Search.
6. Look for social media links – Instagram, Facebook, Twitter, TikTok, LinkedIn.

✅ What to do: Scroll through the search results. Click on any link that looks like a profile page.
❌ What NOT to do: Don’t paste random search result pages – only direct profile URLs (e.g., https://www.instagram.com/johndoe/). Don’t paste video links or news articles.

6️⃣ Paste the discovered URLs

Back in Termux, you’ll be asked:

```
📎 Paste URLs here: 
```

✅ What to do: Copy each profile URL from your browser and paste them here, separated by spaces.
Example:

```
https://www.instagram.com/mucheketanaka
tiktok.com/@mucheketanaka
tanakamucheke3@gmail.com
```

Then press Enter.
❌ What NOT to do: Don’t paste more than one URL without a space. Don’t paste incomplete URLs.

7️⃣ View results

The tool extracts usernames and saves a JSON report in the results/ folder.
Example output:

```
✅ Saved report to results/tanaka_social_snap_20250505_143022.json
📢 Found usernames: johndoe, johndoe
```

✅ What to do: You can open the JSON file with a text editor or cat results/*.json to see all details.
❌ What NOT to do: Don’t delete the results/ folder if you want to keep your reports.

8️⃣ Return to menu

Press Enter when prompted to go back to the main menu. You can scan another image or exit.

Option 2 – Exit

Type 2 and press Enter to exit the tool.

⚠️ Common mistakes and how to avoid them

Mistake Why it happens How to avoid
File not found The path you typed doesn’t exist Use Option 2 (copy to current folder) or double‑check the path with ls
No face found The photo is blurry, too dark, or the face is sideways Use a clear, front‑facing, well‑lit photo
Upload failed No internet connection or Imgur is blocked Check your Wi‑Fi/mobile data
termux-open-url not found Termux:API not installed Run pkg install termux-api (optional – tool still works manually)
No usernames extracted You pasted a wrong URL (e.g., Google search page) Only paste direct social profile URLs like https://instagram.com/username
cv2.error OpenCV not installed correctly Run pip install opencv-python-headless again

❓ FAQ

Why doesn’t the tool automatically find social profiles?

Because Google, Bing, and Yandex actively block automated reverse image searches. The tool does everything else automatically – you only need to paste the Imgur URL into Google Images once. That’s the only reliable way on Termux.

Can I use this to track someone in real time?

No. This tool only finds public images that have already been indexed by Google. It cannot track a person’s current location or live activity.

Is this illegal?

It depends on how you use it.
✅ Legal: Searching for your own face, researching public figures, or using with explicit permission.
❌ Illegal: Stalking, harassing, or investigating someone without consent.
You are responsible for complying with your local laws.

Does it work on iOS?

No – this tool is built for Termux on Android. It will not work on iPhones.

The tool freezes during face detection – what should I do?

Press Ctrl + C to exit, then run python TanakaSocialsnap.py again. If it happens repeatedly, your photo might be too large – try resizing it to under 5MB.

🛠️ Updating the tool

To get the latest version:

```bash
cd ~/TanakaSocialsnap
git pull
pip install --upgrade opencv-python-headless colorama requests
```

📁 File structure after using the tool

```
~/TanakaSocialsnap/
├── TanakaSocialsnap.py       # Main script
├── faces/                    # Cropped face images
│   └── face_1234567890.jpg
├── results/                  # JSON reports
│   └── tanaka_social_snap_20250505_143022.json
├── haarcascade_frontalface_default.xml   # Face detector (auto-downloaded)
└── README.md
```

💬 Need help?

· Open an issue on Github
· Read the tool’s on‑screen instructions carefully – each step explains itself.

---

Remember: With great power comes great responsibility. Use this tool ethically and only with explicit consent.
— Tanaka Mucheke

```

Copy the above into your `README.md` file and push to GitHub. Your users will have a clear, step‑by‑step guide that answers their “how, when, which, and why” questions.4. **Extracts public information** from discovered profiles
5. **Exports findings** to JSON/CSV for analysis

Think of it as an OSINT tool for investigating publicly available information through facial recognition.

## 📱 Installation

### Prerequisites
- Android device with Termux installed
- Internet connection
- Basic command line knowledge

### One-Command Installation (Recommended)
Open Termux and paste this command:

```bash
pkg update && pkg upgrade -y && pkg install git -y && git clone https://github.com/Tanakaprogramminghub/TanakaSocialsnap.git && cd SocialSnap && bash install.sh
