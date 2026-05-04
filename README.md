# SocialSnap - OSINT Facial Recognition Tool for Termux

**Created by Tanaka Mucheke**

[![Termux](https://img.shields.io/badge/Termux-Android-green)](https://termux.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> ⚠️ **WARNING**: This tool is for EDUCATIONAL PURPOSES ONLY. Use only with explicit consent from the target individual. Unauthorized tracking/facial recognition may violate privacy laws in your jurisdiction.

## 📸 What is TanakaSocialsnap?

SocialSnap is a OSINT (Open Source Intelligence) tool that:
1. **Detects faces** in images from your Android gallery
2. **Performs reverse image searches** across major search engines
3. **Identifies social media profiles** linked to the detected face
4. **Extracts public information** from discovered profiles
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