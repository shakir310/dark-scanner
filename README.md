# 🦇 Dark & Mysterious - Web Vulnerability Scanner

**Version 1.0 | Python 3 + Flask**  
A powerful, multi-threaded web vulnerability scanner inspired by Gobuster, Nikto, and WPScan. Scans for sensitive directories, SSL issues, header misconfigurations, and open ports.

---

## ✨ Features

- 🧨 **Directory Bruteforcing:** Scans 100+ sensitive paths (Admin panels, .env, .git, backups, etc.).
- 🔒 **SSL & Security Headers Check:** Identifies missing HSTS, X-Frame-Options, CSP, etc.
- 🌐 **Open Port Discovery:** Detects open ports (21, 22, 80, 443, 3306, etc.).
- 📄 **Professional PDF Reports:** One-click PDF generation of the vulnerability report.
- ⚡ **Fast & Multi-threaded:** Uses concurrent requests for speed.
- 💀 **Dark & Mysterious UI:** Cyberpunk/Hacker themed interface with typing animations.

---

## 💻 Installation & Usage

**Step 1: Clone the repository**
```bash
git clone https://github.com/shakir310/dark-scanner.git
cd dark-scanner

Step 2: Install dependencies
Run the following commands in your terminal:
# For Kali Linux users: Create a virtual environment first
python3 -m venv .venv
source .venv/bin/activate

# Install the required libraries (For Windows users, skip the above 2 lines)
pip install -r requirements

Step 3: Run the application
'''bash python app.py

Step 4: Access the tool
Open your web browser and navigate to:
http://127.0.0.1:5000

🛠️ How to Use the Scanner
Enter a target URL (e.g., https://example.com).

Click the SCAN button.

Wait a few seconds for the scan to complete.

View real-time severity stats (Critical, High, Medium, Low).

Click Download PDF Report to save the results.

🐧 Kali Linux Compatibility
This tool is fully compatible with Kali Linux and other Debian-based distributions. Just follow the installation steps above and run it like any standard reconnaissance tool.

📌 Tech Stack
Backend: Python 3, Flask, Gunicorn, Requests

Frontend: HTML5, CSS3, JavaScript

Reporting: ReportLab (PDF Generation)

Concurrency: ThreadPoolExecutor

⚠️ Legal Disclaimer
This tool is intended for educational purposes and authorized security testing only.
Do NOT use it against targets without explicit written permission.
The author is not responsible for any misuse or illegal activities.

🤝 Connect with the Developer
Developed by Shakir
🔗 GitHub Profile

⭐ If you find this project useful, please give it a Star on GitHub!
