#!/data/data/com.termux/files/usr/bin/bash
# Tanaka Social Snap Installer
# Created by Tanaka Mucheke

# Colors for animations
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Spinner function
spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    while ps -p "$pid" > /dev/null 2>&1; do
        local temp=${spinstr#?}
        printf " [${CYAN}%c${NC}]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# Animated dots
dots() {
    local msg="$1"
    local duration=$2
    local end=$((SECONDS + duration))
    while [ $SECONDS -lt $end ]; do
        echo -ne "\r${GREEN}${msg}   ${NC}"
        sleep 0.3
        echo -ne "\r${GREEN}${msg}.  ${NC}"
        sleep 0.3
        echo -ne "\r${GREEN}${msg}.. ${NC}"
        sleep 0.3
        echo -ne "\r${GREEN}${msg}...${NC}"
        sleep 0.3
    done
    echo -ne "\r${GREEN}${msg} ✓${NC}\n"
}

# Clear screen
clear

echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                            ║${NC}"
echo -e "${CYAN}║     ████████╗ █████╗ ███╗   ██╗ █████╗ ██╗  ██╗ █████╗     ║${NC}"
echo -e "${CYAN}║     ╚══██╔══╝██╔══██╗████╗  ██║██╔══██╗██║ ██╔╝██╔══██╗    ║${NC}"
echo -e "${CYAN}║        ██║   ███████║██╔██╗ ██║███████║█████╔╝ ███████║    ║${NC}"
echo -e "${CYAN}║        ██║   ██╔══██║██║╚██╗██║██╔══██║██╔═██╗ ██╔══██║    ║${NC}"
echo -e "${CYAN}║        ██║   ██║  ██║██║ ╚████║██║  ██║██║  ██╗██║  ██║    ║${NC}"
echo -e "${CYAN}║        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ║${NC}"
echo -e "${CYAN}║                                                            ║${NC}"
echo -e "${CYAN}║         ███████╗ ██████╗  ██████╗██╗ █████╗ ██╗            ║${NC}"
echo -e "${CYAN}║         ██╔════╝██╔═══██╗██╔════╝██║██╔══██╗██║            ║${NC}"
echo -e "${CYAN}║         ███████╗██║   ██║██║     ██║███████║██║            ║${NC}"
echo -e "${CYAN}║         ╚════██║██║   ██║██║     ██║██╔══██║██║            ║${NC}"
echo -e "${CYAN}║         ███████║╚██████╔╝╚██████╗██║██║  ██║███████╗        ║${NC}"
echo -e "${CYAN}║         ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝        ║${NC}"
echo -e "${CYAN}╠════════════════════════════════════════════════════════════╣${NC}"
echo -e "${CYAN}║           ${MAGENTA}TANAKA SOCIAL SNAP - INSTALLER${CYAN}               ║${NC}"
echo -e "${CYAN}║            ${YELLOW}Created by Tanaka Mucheke${CYAN}                     ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}🔧 Starting installation...${NC}"
sleep 1

# Step 1: Update packages
echo -e "\n${CYAN}📦 Step 1/5: Updating Termux packages...${NC}"
(
    pkg update -y && pkg upgrade -y
) & spinner $!
echo -e "\r${GREEN}✅ Packages updated${NC}"

# Step 2: Install system dependencies
echo -e "\n${CYAN}📦 Step 2/5: Installing system dependencies (python, git, termux-api, opencv)...${NC}"
(
    pkg install -y python git termux-api opencv
) & spinner $!
echo -e "\r${GREEN}✅ System dependencies installed${NC}"

# Step 3: Install Python packages with animated dots
echo -e "\n${CYAN}🐍 Step 3/5: Installing Python packages (opencv, colorama, requests)...${NC}"
dots "📥 Installing opencv-python-headless" 2
pip install opencv-python-headless > /dev/null 2>&1
dots "🎨 Installing colorama" 1
pip install colorama > /dev/null 2>&1
dots "🌐 Installing requests" 1
pip install requests > /dev/null 2>&1
echo -e "${GREEN}✅ Python packages installed${NC}"

# Step 4: Make script executable
echo -e "\n${CYAN}🔧 Step 4/5: Making TanakaSocialsnap.py executable...${NC}"
chmod +x TanakaSocialsnap.py 2>/dev/null
echo -e "${GREEN}✅ Script is now executable${NC}"

# Step 5: Final check
echo -e "\n${CYAN}🔍 Step 5/5: Verifying installation...${NC}"
sleep 1

echo -e "\n${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${MAGENTA}✨ TANAKA MUCHEKE - TANAKA SOCIAL SNAP ✨${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}✅ Installation complete!${NC}"
echo -e "${CYAN}🚀 Run 'python TanakaSocialsnap.py' to start the tool.${NC}"
echo -e "${RED}⚠️  Remember: Use only with explicit permission.${NC}"
echo ""
