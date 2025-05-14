#!/bin/bash

# === SYSTEM SETUP ===
echo "[1/5] Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "[2/5] Installing Python, pip, and venv..."
sudo apt install -y python3 python3-pip python3-venv

# === CLONE YOUR PROJECT (if not already present) ===
# git clone https://github.com/your-repo/wisdom-layer-poc.git
cd ~/wisdom-layer-poc || exit

# === PYTHON VIRTUAL ENV ===
echo "[3/5] Creating and activating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# === REQUIREMENTS ===
echo "[4/5] Installing Python dependencies..."
# If needed, fix incompatible torch version inside requirements.txt
sed -i '/torch==.*+cpu/d' requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

# === STREAMLIT LAUNCH HELP ===
echo "[5/5] Setup complete ✅"
echo "To run your Streamlit app:"
echo ""
echo "  source venv/bin/activate"
echo "  streamlit run app.py"
