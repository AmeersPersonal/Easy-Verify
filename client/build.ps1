# This script does a few things:
# 1. Checks if Python and pip are installed
# 2. Creates and activates a virtual environment
# 3. Installs dependencies from requirements.txt
# 4. Uses PyInstaller to build the executable
# 5. Registers a custom URI protocol (easy-verify://) to launch the executable


# Exit on error
$ErrorActionPreference = "Stop"




Write-Host "Checking for Python..." -ForegroundColor Blue

# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not in PATH."
    exit 1
}

# Print Python version
try {
    $pythonVersion = python --version
    Write-Host "Python found: $pythonVersion"
}
catch {
    Write-Error "Failed to get Python version."
    exit 1
}

# Check if pip is installed
Write-Host "Checking for pip..." -ForegroundColor Blue
try {
    $pipVersion = python -m pip --version
    Write-Host "pip found: $pipVersion" -ForegroundColor Green
}
catch {
    Write-Error "pip is not installed."
    exit 1
}

# Create virtual environment
$venvPath = ".venv"

if (-Not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Blue
    python -m venv $venvPath
}
else {
    Write-Host "Virtual environment already exists." -ForegroundColor Yellow
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Blue
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

if (-Not (Test-Path $activateScript)) {
    Write-Error "Activation script not found."
    exit 1
}
else {
    Write-host "Virtual environment activated." -ForegroundColor Green
}

. $activateScript

# Upgrade pip (optional but recommended)

if (-not( $args[0] -eq "skipUpdate")) {
    Write-Host "Upgrading pip..." -ForegroundColor Blue
    python -m pip install --upgrade pip
}

# Navigate to src directory
$srcPath = "src"

if (-Not (Test-Path $srcPath)) {
    Write-Error "src directory not found."
    exit 1
}

Set-Location $srcPath

# Install requirements
$requirementsFile = "requirements.txt"

if (-Not (Test-Path $requirementsFile)) {
    Write-Error "requirements.txt not found in src directory."
    exit 1
}

if(-Not($args[0] -eq "skipUpdate")) {
    Write-Host "Installing dependencies..." -ForegroundColor Blue
    pip install -r $requirementsFile
    # Ensure PyInstaller is installed 
    # Pyinstaller should be installed through requirements.txt, but we can ensure it here as well
    Write-Host "Ensuring PyInstaller is installed..." -ForegroundColor Blue
    pip install pyinstaller
}



# Check for spec file
$specFile = "main.spec"

if (-Not (Test-Path $specFile)) {
    Write-Error "main.spec not found in src directory."
    exit 1
}

# Go back to root directory
Set-Location ..

# Ensure build output folder exists
$buildDir = "build"
if (-Not (Test-Path $buildDir)) {
    New-Item -ItemType Directory -Path $buildDir | Out-Null
}

Write-Host "Building executable..." -ForegroundColor Blue

$error.clear()

pyinstaller "src/main.spec" --distpath $buildDir --workpath "$buildDir\build" --noconfirm 

if ($error) {
    Write-Error "PyInstaller build failed."
    Write-Error $error
    exit 1
}


$executablePath = Join-Path $buildDir "\main\main.exe"

Write-Host (Resolve-Path $executablePath)

Write-Host "Checking for executable at: $executablePath" -ForegroundColor Blue
if (Test-Path $executablePath) {
    Write-Host "Executable built successfully: $executablePath" -ForegroundColor Green
}
else {
    Write-Error "Build failed. Executable not found at expected location."
    Write-Host (Resolve-Path $executablePath)
    exit 1
}

Write-Host "Registering custom URI protocol: easy-verify://" -ForegroundColor Blue

$baseKey = "HKCU:\Software\Classes\easy-verify"
$commandKey = "$baseKey\shell\open\command"

# Create keys
New-Item -Path $commandKey -Force | Out-Null

# Set (Default) value for protocol description
Set-ItemProperty -Path $baseKey -Name "(Default)" -Value "URL:easy-verify Protocol"

# Set URL Protocol (empty string)
New-ItemProperty -Path $baseKey -Name "URL Protocol" -Value "" -PropertyType String -Force | Out-Null

# Set command to executable
# "%1" passes the URI argument
$commandValue = "`"$(Resolve-Path $executablePath)`" `"%1`""
Set-ItemProperty -Path $commandKey -Name "(Default)" -Value $commandValue

Write-Host "Custom URI protocol registered successfully." -ForegroundColor Green

Write-Host "Sometimes there is an error with the .spec file, check if the executable is built correctly, if not, edit the spec file." -ForegroundColor Yellow
