import http.server
import threading
import time
import os
from playwright.sync_api import sync_playwright

PORT = 8997
DIRECTORY = r"c:\Users\vaibh\Desktop\coep-scopus-web-dashboard"
OUTPUT_DIR = r"c:\Users\vaibh\Desktop\SCOPUS Dashboard\web_dashboard\scratch"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

server = http.server.ThreadingHTTPServer(("", PORT), Handler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        m_context = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
        m_page = m_context.new_page()
        m_page.goto(f"http://localhost:{PORT}/index.html", wait_until="load")
        time.sleep(3)

        # 1. Mobile Impact
        m_page.locator('button.tab-nav-btn:has-text("Impact")').first.click()
        time.sleep(1)
        m_page.locator("#chart-dept-cites").scroll_into_view_if_needed()
        time.sleep(1)
        m_page.screenshot(path=os.path.join(OUTPUT_DIR, "shot_mobile_impact_dept.png"))

        m_page.locator("#chart-citation-accrual").scroll_into_view_if_needed()
        time.sleep(1)
        m_page.screenshot(path=os.path.join(OUTPUT_DIR, "shot_mobile_impact_accrual.png"))

        # 2. Mobile Collaboration
        m_page.locator('button.tab-nav-btn:has-text("Collaboration")').first.click()
        time.sleep(1)
        m_page.locator("#chart-world-map").scroll_into_view_if_needed()
        time.sleep(1)
        m_page.screenshot(path=os.path.join(OUTPUT_DIR, "shot_mobile_collab_map.png"))

        m_page.locator("#chart-partner-countries").scroll_into_view_if_needed()
        time.sleep(1)
        m_page.screenshot(path=os.path.join(OUTPUT_DIR, "shot_mobile_partner_countries.png"))

        # 3. Mobile Quality
        m_page.locator('button.tab-nav-btn:has-text("Quality")').first.click()
        time.sleep(1)
        m_page.locator("#chart-quartile-donut").scroll_into_view_if_needed()
        time.sleep(1)
        m_page.screenshot(path=os.path.join(OUTPUT_DIR, "shot_mobile_donut.png"))

        m_page.locator("#chart-dept-radar").scroll_into_view_if_needed()
        time.sleep(1)
        m_page.screenshot(path=os.path.join(OUTPUT_DIR, "shot_mobile_radar.png"))

        browser.close()
        print("Mobile screenshots captured!")
finally:
    server.shutdown()
