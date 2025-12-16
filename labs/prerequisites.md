# GitHub Copilot Workshop

## Prerequisites & Environment Setup

This file lists what participants should know before attending the workshop and step-by-step setup instructions to prepare their Windows laptop (PowerShell-ready commands included).

## Skills participants should have

- Basic Git: clone, branch, commit, push/pull, simple conflict resolution.
- Comfortable using VS Code: open project, install extensions, use built-in terminal.
- Command line basics (PowerShell): navigating folders, running scripts, activating virtual environments.
- Basic programming literacy:
  - Python fundamentals (scripts, pip, virtualenvs).
  - Web fundamentals (HTTP, URLs, basic client/server concept).
- Basic testing concepts: unit vs integration vs BDD tests, and test runners (pytest, behave).
- Familiarity with browser automation concepts (Selenium).
- A GitHub account and basic familiarity with signing into VS Code (required for Copilot extension use).

## Required software (recommended versions)

- Git (latest stable). Install from: https://git-scm.com/
- VS Code (latest stable). Install from: https://code.visualstudio.com/
- Python 3.10+ (3.11 recommended). Install from: https://www.python.org/
- pip (comes with Python) and virtualenv support.
- A modern browser (Chrome or Edge Chromium) for Selenium-driven tests.

Optional package managers to speed installs:
- Chocolatey (https://chocolatey.org/) or Scoop (https://scoop.sh/)

## VS Code extensions to install

- GitHub Copilot (sign-in required and Copilot subscription/trial)
- Python (Microsoft)

## Visual Studio Professional 2022 (optional)

Note that the labs were designed for lightweight editors and command-line tools (VS Code + PowerShell + virtualenv). Visual Studio 2022 is optional and we dont have the time to explain and debug all lab and its instructions for both environments. When you decide to use VS2022 ensure you have the proper knowlegde.

- Ensure Python support inside Visual Studio is enabled.
- Using a virtualenv in Visual Studio:
  - Create a virtualenv with the steps shown earlier (`python -m venv .venv`).
  - In Visual Studio, open the folder and configure the Python environment to point at `\.venv\Scripts\python.exe`.
  - Use the built-in terminal (PowerShell) to run the same `pip install -r` commands and test runners.

## Accounts / Access

- GitHub account (required for Copilot and for cloning/pushing exercises)
- GitHub Copilot access (subscription)


## Quick PowerShell setup commands (copy-paste)

Notes:
- Run these from a PowerShell prompt. If PowerShell blocks script execution, the included command relaxes policy for the current user.
- Replace `<lab-dir>` below with the path to the `labs` folder you cloned (for this repository: the root folder that contains `lab-s1`, `lab-0`, etc.).

### 1) Clone the repo (example):

```powershell
# clone (replace with your repo URL or use the provided folder)
git clone https://github.com/RaphaelHerd/gh-cp-training.git
cd "<path-to-cloned-repo>\labs"
```

### 2) Create and activate a Python virtual environment (recommended):

```powershell
# create venv in current folder
python -m venv .venv

# if PowerShell blocks activation scripts, allow for current user (run once)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# activate the venv (PowerShell)
.\.venv\Scripts\Activate.ps1

# verify python & pip
python --version
pip --version
```

### 3) Install dependencies for a lab (example for `lab-s1`):

```powershell
# while venv activated
pip install -r .\lab-s1\requirements.txt

# for pytest-based lab-s3
pip install -r .\lab-s3\requirements.txt
```

Notes on `requirements.txt` in this workshop:
- The behave-based labs (`lab-s1`, `lab-s2`, `lab-s4`, `lab-s5`, `lab-s6`) include packages such as:
  - behave, behave-webdriver, allure-behave, selenium>=4.6.0, pyyaml, selenium-page-factory, unittest2, assertpy, urllib3, grpcio==1.60.1
- `lab-s3` uses pytest and related packages (pytest, requests, jsonschema).

### 4) Dry-run behave BDD tests:

```powershell
# activate venv first
.\.venv\Scripts\Activate.ps1
# ensure that no errors occur
behave --version

```

### 5) Dry-run pytest tests

```powershell
.\.venv\Scripts\Activate.ps1
pytest --version
```
## Troubleshooting

- Windows ExecutionPolicy can block `Activate.ps1`. Use `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` to allow activation.
- Selenium >=4.6 uses Selenium Manager to download drivers automatically; if your machine blocks downloads, you may need to install the browser driver (e.g. chrome driver) manually and add it to PATH.