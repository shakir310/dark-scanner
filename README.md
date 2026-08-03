# 🦇 Dark & Mysterious - Web Vulnerability Scanner

> 🚀 **A Python Flask-based Web Vulnerability Scanner**  
> Inspired by tools like Gobuster, Nikto, and WPScan.  
> Scan websites for sensitive directories, security header misconfigurations, open ports, and more!

---

## ✨ Features

- 🧨 **Directory Bruteforcing:** Scans 100+ sensitive paths (Admin panels, `.env`, `.git`, backups, etc.).
- 🔒 **SSL & Security Headers Check:** Identifies missing HSTS, X-Frame-Options, CSP, etc.
- 🌐 **Open Port Discovery:** Detects open ports (21, 22, 80, 443, 3306, etc.).
- 📄 **Professional PDF Reports:** One-click PDF generation of the vulnerability report.
- ⚡ **Fast & Multi-threaded:** Uses concurrent requests for speed.
- 💀 **Dark & Mysterious UI:** Cyberpunk/Hacker themed interface with typing animations.

---

## 🖥️ How to Run Locally (For Kali Linux / Windows)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shakir310/dark-scanner.git
   cd dark-scanner
Step 2: Install dependencies,,,bash
pip install -r requirements.txt

Step 3: Run the Flask server

bash
python app.py
Step 4: Open in browser
Go to http://127.0.0.1:5000 and start scanning!

🛠️ How to Use
Enter a target URL (e.g., https://example.com).

Click the SCAN button.

Wait a few seconds for the multi-threaded scan to complete.

View real-time severity stats (Critical, High, Medium, Low).

Click Download PDF Report to save the results.

🐧 Kali Linux Usage
This tool is fully compatible with Kali Linux and other Debian-based distributions. Just follow the installation steps above and run it like any standard reconnaissance tool.

📌 Tech Stack
Backend: Python 3, Flask, Gunicorn, Requests

Frontend: HTML5, CSS3, JavaScript

Reporting: ReportLab (PDF Generation)

Concurrency: ThreadPoolExecutor

⚠️ Disclaimer
This tool is intended for educational purposes and authorized security testing only. Do not use it against targets without explicit written permission. The author is not responsible for any misuse.

🤝 Connect
Developed by Shakir
🔗 GitHub Profile

⭐ If you find this useful, please give it a Star!

text

---
