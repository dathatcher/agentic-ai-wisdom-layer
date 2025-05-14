# Run this as Administrator  .\setup-agentic-env.ps1

Write-Host "Installing Chocolatey (if not installed)..."
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    refreshenv
}

Write-Host "Installing Python, Git, and Chrome..."
choco install -y python git googlechrome

Write-Host "Cloning your repository..."
cd $env:USERPROFILE
git clone https://github.com/dathatcher/wisdom-layer-poc.git
cd wisdom-layer-poc

Write-Host "Creating Python virtual environment..."
py -m venv venv
.\venv\Scripts\Activate.ps1

Write-Host "Upgrading pip and installing requirements..."
py -m pip install --upgrade pip

if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
} else {
    pip install streamlit networkx matplotlib
}

Write-Host "`n✅ Environment setup complete. To start Streamlit, run:"
Write-Host "   .\venv\Scripts\Activate.ps1"
Write-Host "   streamlit run app.py"
