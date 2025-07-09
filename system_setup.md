# Leavitt Law Calibration (lvtlaw)

This repository guides you through the process of setting up your environment, installing dependencies, and running the project using Python.

## Table of Contents

1. [Installing Python](#1-installing-python)
   - [Windows](#windows)
   - [Ubuntu](#ubuntu)
   - [MacOS](#macos)
2. [Installing Git and Cloning the Repo](#2-installing-git-and-cloning-the-repo)
3. [Creating and Activating Environment](#3-creating-and-activating-environment)
   - [Using `requirements.txt`](#using-requirementstxt)
   - [Using Conda `environment.yml`](#using-conda-environmentyml)
4. [Running the Code](#4-running-the-code)

---

## 1. Installing Python

### Windows

1. Download Python from the official website: [Python.org](https://www.python.org/downloads/windows/)
2. Run the installer and ensure the **"Add Python to PATH"** option is selected during installation.
3. Verify the installation by opening PowerShell or Command Prompt and running:

   ```powershell
   python --version
   ```
### Ubuntu
```
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```
### macOS
```
brew install python
python3 --version
```
## 2. Installing Git and Cloning the Repo
### Install Git
Windows: https://git-scm.com/download/win

Ubuntu: sudo apt install git

macOS: brew install git

### Clone the Repository
```
git clone https://github.com/mshubham00/Leavitt_Law_Calibration.git
cd Leavitt_Law_Calibration
```
## 3. Creating and Activating Environment

### Using requirement.tex
```
python -m venv lvtlaw_env
```
#### Ubuntu
```
source lvtlaw_env\Scripts\activate
```
#### Window Powershell
```
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\lvtlaw_env\Scripts\Activate.ps1
```
#### Window Terminal
```
.\lvtlaw_env\Scripts\activate.bat
```

#### Install Dependencies
```
pip install -r requirements.txt
```
### Using environment.yml
```
conda env create -f environment.yml
conda activate lvtlaw_calibration_env
```

## 4. Execute the code
```
python main.py
```







