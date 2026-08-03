from flask import Flask, render_template, request, jsonify, send_file
import requests
import socket
import ssl
import datetime
import io
from concurrent.futures import ThreadPoolExecutor, as_completed
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

app = Flask(__name__)

scan_results = []

# 🔥 100+ REAL DIRECTORIES
SENSITIVE_DIRS = [
    '/admin', '/administrator', '/adminpanel', '/admin-login', '/dashboard', '/cpanel', '/whm',
    '/wp-admin', '/wp-content', '/wp-includes', '/wp-json', '/wp-login.php',
    '/.git', '/.env', '/.htaccess', '/.svn', '/.aws', '/.ssh', '/.gitignore',
    '/backup', '/db', '/database', '/mysql', '/sql', '/config', '/configuration',
    '/uploads', '/files', '/images', '/assets', '/robots.txt', '/sitemap.xml',
    '/api', '/v1', '/v2', '/rest', '/graphql',
    '/test', '/tests', '/temp', '/logs', '/error_log', '/debug',
    '/phpmyadmin', '/pma', '/myadmin', '/mysqladmin',
    '/login', '/signin', '/auth', '/register', '/signup',
    '/panel', '/control', '/secure', '/private', '/hidden'
]

# ✅ Real Browser Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive"
}

def check_ssl(url):
    try:
        hostname = url.replace('https://', '').replace('http://', '').split('/')[0]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expiry = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                if expiry < datetime.datetime.now():
                    return {'vuln': 'SSL Certificate Expired', 'sev': 'High', 'desc': 'SSL certificate expired!', 'fix': 'Renew SSL immediately.'}
                elif (expiry - datetime.datetime.now()).days < 30:
                    return {'vuln': 'SSL Expiring Soon', 'sev': 'Medium', 'desc': 'SSL expires in less than 30 days.', 'fix': 'Renew SSL soon.'}
    except:
        pass
    return None

def check_headers(url):
    results = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        
        if 'X-Frame-Options' not in resp.headers:
            results.append({'vuln': 'Missing X-Frame-Options', 'sev': 'Medium', 'desc': 'Clickjacking risk!', 'fix': 'Add header: X-Frame-Options: DENY'})
        if 'X-Content-Type-Options' not in resp.headers:
            results.append({'vuln': 'Missing X-Content-Type-Options', 'sev': 'Medium', 'desc': 'MIME sniffing risk.', 'fix': 'Add header: X-Content-Type-Options: nosniff'})
        if 'Content-Security-Policy' not in resp.headers:
            results.append({'vuln': 'Missing CSP Header', 'sev': 'Medium', 'desc': 'Prevents XSS attacks.', 'fix': 'Implement strict CSP.'})
        if 'Strict-Transport-Security' not in resp.headers:
            results.append({'vuln': 'Missing HSTS', 'sev': 'Low', 'desc': 'Enforces secure HTTPS connections.', 'fix': 'Add HSTS header.'})
    except:
        results.append({'vuln': 'Connection Warning', 'sev': 'Low', 'desc': 'Website might have a firewall.', 'fix': 'No fix needed.'})
    return results

def check_ports(url):
    results = []
    hostname = url.replace('https://', '').replace('http://', '').split('/')[0]
    ports = [21, 22, 23, 80, 443, 3306, 3389, 8080, 8443]
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            res = sock.connect_ex((hostname, port))
            sock.close()
            if res == 0:
                results.append({'vuln': f'Open Port: {port}', 'sev': 'Low', 'desc': f'Port {port} is open.', 'fix': 'Close unused ports via Firewall.'})
        except:
            pass
    return results

# ✅ NEW LOGIC: 200 = High, Baaki sab (403, 401, 301, 302) = Medium
def check_directory(url, directory):
    full_url = url.rstrip('/') + directory
    try:
        resp = requests.get(full_url, headers=HEADERS, timeout=3, allow_redirects=True, verify=False)
        
        if resp.status_code == 404:
            return None # Fake link, ignore
        
        # 🔥 EXACT LOGIC: Jo link open ho raha hai (200) wo High. Baaki sab Medium.
        if resp.status_code == 200:
            severity = 'High'
            desc = f'🔗 <b>Publicly Accessible Link:</b> <a href="{full_url}" target="_blank">{full_url}</a> (Status: {resp.status_code})'
        else:
            # Agar 403, 401, 301, 302, 500 hai -> Wo Medium hoga
            severity = 'Medium'
            desc = f'🔗 <b>Restricted/Redirect Link:</b> <a href="{full_url}" target="_blank">{full_url}</a> (Status: {resp.status_code})'

        return {
            'vuln': f'Sensitive Directory Found',
            'sev': severity,
            'desc': desc,
            'fix': 'Restrict access using .htaccess / Nginx deny rules.'
        }
    except:
        return None

def run_gobuster_scan(url):
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_directory, url, d) for d in SENSITIVE_DIRS]
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    
    results.sort(key=lambda x: x['sev'], reverse=True)
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    global scan_results
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    raw_url = data.get('url', '').strip()
    if not raw_url:
        return jsonify({'error': 'URL is required'}), 400

    if not raw_url.startswith('http'):
        raw_url = 'https://' + raw_url

    scan_results = []
    
    ssl_check = check_ssl(raw_url)
    if ssl_check: scan_results.append(ssl_check)
    
    scan_results.extend(check_headers(raw_url))
    scan_results.extend(check_ports(raw_url))
    
    try:
        dir_results = run_gobuster_scan(raw_url)
        scan_results.extend(dir_results)
    except:
        pass
    
    if not scan_results:
        scan_results.append({'vuln': 'Scan Successful', 'sev': 'Low', 'desc': 'Scan completed. No common public vulnerabilities detected.', 'fix': 'Keep monitoring your server logs.'})

    counts = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
    for r in scan_results:
        counts[r['sev']] = counts.get(r['sev'], 0) + 1

    return jsonify({'results': scan_results, 'counts': counts})

@app.route('/download-report', methods=['GET'])
def download_report():
    if not scan_results:
        return "No scan data found.", 400

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = styles['Title']
    title_style.textColor = colors.HexColor('#7c3aed')
    normal_style = styles['Normal']
    
    story.append(Paragraph("<b>Dark & Mysterious - Security Audit</b>", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Report Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    story.append(Spacer(1, 24))

    for i, item in enumerate(scan_results):
        clean_desc = str(item['desc']).replace('<', '&lt;').replace('>', '&gt;')
        clean_fix = str(item['fix']).replace('<', '&lt;').replace('>', '&gt;')
        
        story.append(Paragraph(f"<b>{i+1}. {item['vuln']}</b>", styles['Heading2']))
        story.append(Paragraph(f"<font color='red'><b>Severity:</b></font> {item['sev']}", normal_style))
        story.append(Paragraph(f"<b>Description:</b> {clean_desc}", normal_style))
        story.append(Paragraph(f"<b>Remediation:</b> {clean_fix}", normal_style))
        story.append(Spacer(1, 15))

    doc.build(story)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='Dark_Mysterious_Report.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    app.run(host='0.0.0.0', port=5000, debug=True)