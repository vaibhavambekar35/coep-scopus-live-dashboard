import http.server
import socketserver
import threading
import time
import os
from playwright.sync_api import sync_playwright

PORT = 8999
DIRECTORY = r"c:\Users\vaibh\Desktop\coep-scopus-web-dashboard"
OUTPUT_DIR = r"c:\Users\vaibh\Desktop\SCOPUS Dashboard\web_dashboard\scratch"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

server = socketserver.TCPServer(("", PORT), Handler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()
print(f"Server started at http://localhost:{PORT}")

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # 1. Desktop screenshots (1600x1000)
        context = browser.new_context(viewport={"width": 1600, "height": 1000})
        page = context.new_page()
        page.goto(f"http://localhost:{PORT}/index.html", wait_until="networkidle")
        time.sleep(2)

        tabs = ["Impact", "Collaboration", "Quality"]
        for tab in tabs:
            btn = page.locator(f"button.tab-nav-btn:has-text('{tab}')").first
            btn.click()
            time.sleep(1.5)
            # Scroll down slightly to ensure charts are in view
            page.screenshot(path=os.path.join(OUTPUT_DIR, f"coep_{tab.lower()}_desktop.png"))
            print(f"Captured {tab} desktop")

        # 2. Mobile screenshots (390x844 - iPhone 12/13/14)
        m_context = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
        m_page = m_context.new_page()
        m_page.goto(f"http://localhost:{PORT}/index.html", wait_until="networkidle")
        time.sleep(2)

        for tab in tabs:
            btn = m_page.locator(f"button.tab-nav-btn:has-text('{tab}')").first
            btn.click()
            time.sleep(1.5)
            m_page.screenshot(path=os.path.join(OUTPUT_DIR, f"coep_{tab.lower()}_mobile_top.png"))
            m_page.evaluate("window.scrollTo(0, 600)")
            time.sleep(1)
            m_page.screenshot(path=os.path.join(OUTPUT_DIR, f"coep_{tab.lower()}_mobile_mid.png"))
            print(f"Captured {tab} mobile")

        browser.close()
finally:
    server.shutdown()
    print("Server stopped.")
