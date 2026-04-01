
# 🔍 EQL – SQL Injection & Login Security Tester

<div align="center">
  <img src="https://img.shields.io/badge/SQL-Injection-red?style=for-the-badge&logo=mysql">
  <img src="https://img.shields.io/badge/Brute-Force-orange?style=for-the-badge&logo=hashicorp">
  <img src="https://img.shields.io/badge/Security-Testing-blue?style=for-the-badge&logo=shield">
  
  [![Telegram](https://img.shields.io/badge/Telegram-@ERROR0101risback-26A5E4?style=for-the-badge&logo=telegram)](https://t.me/ERROR0101risback)
  [![Instagram](https://img.shields.io/badge/Instagram-@fahad0101r-E4405F?style=for-the-badge&logo=instagram)](https://instagram.com/fahad0101r)
  [![GitHub](https://img.shields.io/badge/GitHub-ERROR0101r-181717?style=for-the-badge&logo=github)](https://github.com/ERROR0101r)
  [![Telegram Channel](https://img.shields.io/badge/Channel-@aab_ho_ga_comeback-2CA5E0?style=for-the-badge&logo=telegram)](https://t.me/aab_ho_ga_comeback)
  
  <p><strong>Developer: @ERROR0101risback</strong></p>
  <p><em>Version: 3.0 (Stable)</em></p>
</div>

---

## 📋 TABLE OF CONTENTS
- [What is EQL?](#what-is-eql)
- [Important – Educational Only](#important--educational-only)
- [Features](#features)
- [Quick Setup](#quick-setup)
- [Usage Guide](#usage-guide)
- [Output Files](#output-files)
- [Installation Details](#installation-details)
- [Step by Step Tutorial](#step-by-step-tutorial)
- [Developer Contact](#developer-contact)
- [Repository](#repository)
- [License](#license)

---

## WHAT IS EQL?

**EQL (Enhanced Query Lever)** is a powerful security testing tool designed to identify **SQL injection vulnerabilities** and **weak credentials** in web applications.

Built for **authorized security testing** and **educational awareness** purposes only.

| Feature | Description |
|---------|-------------|
| **SQL Injection Testing** | 45+ payloads to test authentication bypass vulnerabilities |
| **Brute Force Testing** | Test username/password combinations |
| **Full Mode** | Combined SQL injection + brute force testing |
| **Smart Detection** | Automatically detects success when failure message is absent |
| **Custom Failure Keywords** | Define failure messages for accurate detection |
| **Custom Wordlists** | Use preset lists or provide your own username/password files |
| **Detailed Reports** | Auto-generated scan.txt with all findings |

---

## IMPORTANT – EDUCATIONAL ONLY

```

THIS TOOL IS STRICTLY FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY.

By using this tool, you agree to:

· Use only on systems you own or have explicit written permission to test
· Take full responsibility for your actions
· Not use for illegal activities

Misuse of this tool for unauthorized access, credential theft, 
or any illegal activity is not supported and may violate laws.

The author (@ERROR0101risback) does not condone any illegal activities.

```

---

## FEATURES

| Feature | Description |
|---------|-------------|
| **45+ SQL Payloads** | Comprehensive SQL injection payload collection |
| **Smart Success Detection** | If failure message not found → automatically counts as success |
| **Custom Failure Keywords** | Define your own failure messages for accurate detection |
| **Dual Mode** | SQL Injection only / Brute Force only / Full Test |
| **Preset Wordlists** | Built-in username and password lists |
| **Custom Wordlists** | Load your own username/password files |
| **Auto Reporting** | Automatically saves results to scan.txt |
| **Time-Based Detection** | Detects blind SQL injection via response delays |
| **Redirect Detection** | Identifies successful logins via URL changes |

---

## QUICK SETUP

### One Command Setup:
```bash
git clone https://github.com/ERROR0101r/Eql.git
cd Eql
pip install -r requirements.txt
python main.py
```

Termux (Android):

```bash
pkg update && pkg upgrade
pkg install python git
git clone https://github.com/ERROR0101r/Eql.git
cd Eql
pip install -r requirements.txt
python main.py
```

Linux (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install python3 python3-pip git
git clone https://github.com/ERROR0101r/Eql.git
cd Eql
pip3 install -r requirements.txt
python3 main.py
```

Windows:

```bash
git clone https://github.com/ERROR0101r/Eql.git
cd Eql
pip install -r requirements.txt
python main.py
```

---

USAGE GUIDE

Run the Tool:

```bash
python main.py
```

Step 1: Accept Disclaimer

```
Accept terms? (yes/no): yes
```

Step 2: Enter Target Information

```
[+] Enter target information
Login URL: http://example.com/admin/login.php
Username field name: username
Password field name: password
Submit button name: login
```

Step 3: Enter Failure Keywords Only

```
Enter failure keywords (comma separated): Invalid password, Login failed, Incorrect
```

Note: If failure message not found on page, tool will mark as SUCCESS

Step 4: Select Testing Mode

```
1. SQL Injection Only
2. Brute Force Only
3. Full Test (Both)
Mode (1/2/3): 3
```

Step 5: Choose Wordlists

```
--- Username List ---
1. Use preset list
2. Use custom file path
Select (1/2): 1

--- Password List ---
1. Use preset list
2. Use custom file path
Select (1/2): 1
```

Step 6: View Results

```
============================================================
SCAN COMPLETE
============================================================
SQL Injection Findings: 3
Valid Credentials Found: 1
============================================================
```

---

HOW DETECTION WORKS

Scenario Detection Method
Failure keyword found Login FAILED
No failure keyword found Login SUCCESSFUL (assumed valid)
Redirect occurs Login SUCCESSFUL
Time delay > 4 seconds Possible SQL injection success
URL changes Login SUCCESSFUL

---

OUTPUT FILES

All scan results are automatically saved to:

```
scan.txt
```

Report Includes:

· Scan date and time
· Failure keywords used
· SQL injection vulnerabilities found (payloads and indicators)
· Valid credentials discovered (username/password)
· Response times and indicators

---

INSTALLATION DETAILS

Requirements:

· Python 3.6 or higher
· requests library

File Structure:

```
Eql/
├── main.py           # Main tool
├── requirements.txt  # Dependencies
├── scan.txt         # Results (auto-generated)
└── README.md        # Documentation
```

---

STEP BY STEP TUTORIAL

Finding Field Names:

1. Open website in Chrome/Firefox
2. Right-click on username box → Inspect
3. Look for name="username" attribute
4. Do same for password field and submit button

Finding Failure Keywords:

1. Enter wrong password
2. Note the error message shown
3. Enter that message as failure keyword

Example Flow:

```
$ python main.py

Accept terms? (yes/no): yes

[+] Enter target information
Login URL: http://testphp.vulnweb.com/login.php
Username field name: uname
Password field name: pass
Submit button name: submit

Enter failure keywords: invalid, incorrect, failed

Mode (1/2/3): 3

--- Username List ---
1. Use preset list
2. Use custom file path
Select (1/2): 1

--- Password List ---
1. Use preset list
2. Use custom file path
Select (1/2): 1

[+] Loaded 19 usernames, 19 passwords

============================================================
SQL INJECTION TESTING
============================================================
[1/45] Testing: ' OR '1'='1' --...
    [.] Not vulnerable - Failure keyword found
[2/45] Testing: ' OR '1'='1' #...
    [!] VULNERABLE! No failure keyword found (Success)

============================================================
BRUTE FORCE TESTING
============================================================
[1/361] Testing: admin:admin...
    [.] Failed - Failure keyword found
[2/361] Testing: admin:password...
    [.] Failed - Failure keyword found
[3/361] Testing: admin:123456...
    [!!!] FOUND! admin:123456 - No failure keyword found

[+] Report saved to scan.txt

============================================================
SCAN COMPLETE
============================================================
SQL Injection Findings: 1
Valid Credentials Found: 1
============================================================
```

---

DEVELOPER CONTACT

<div align="center">
  <p><strong>Name:</strong> ERROR0101risback / Fahad</p>
  <p>
    <a href="https://t.me/ERROR0101risback">Telegram</a> •
    <a href="https://instagram.com/fahad0101r">Instagram</a> •
    <a href="https://github.com/ERROR0101r">GitHub</a>
  </p>
  <p><strong>Telegram Channel:</strong> <a href="https://t.me/aab_ho_ga_comeback">@aab_ho_ga_comeback</a></p>
</div>

---

REPOSITORY

· GitHub: https://github.com/ERROR0101r/Eql
· Download ZIP: https://github.com/ERROR0101r/Eql/archive/refs/heads/main.zip

---

LICENSE

```
This project is for educational purposes only.
No license is granted for commercial or malicious use.
Use at your own risk.

You are free to:
- Use for authorized security testing
- Modify for personal educational use
- Share with other security professionals

You are NOT permitted to:
- Use for unauthorized hacking
- Use to steal credentials
- Distribute as a malicious tool
```

---

<div align="center">
  <h3>🔍 Test. Secure. Protect. 🔍</h3>
  <p><i>Made with 🔥 by @ERROR0101risback</i></p>

  <p>
    <a href="https://t.me/ERROR0101risback"><img src="https://img.shields.io/badge/Telegram-@ERROR0101risback-26A5E4?style=flat-square&logo=telegram"></a>
    <a href="https://instagram.com/fahad0101r"><img src="https://img.shields.io/badge/Instagram-@fahad0101r-E4405F?style=flat-square&logo=instagram"></a>
    <a href="https://github.com/ERROR0101r"><img src="https://img.shields.io/badge/GitHub-ERROR0101r-181717?style=flat-square&logo=github"></a>
    <a href="https://t.me/aab_ho_ga_comeback"><img src="https://img.shields.io/badge/Channel-@aab_ho_ga_comeback-2CA5E0?style=flat-square&logo=telegram"></a>
  </p>

  <p>© 2026 EQL | Version 3.0 Stable</p>
</div>