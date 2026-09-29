import http.server
import socketserver
import threading
import time
import os
from playwright.sync_api import sync_playwright

PORT = 8998
DIRECTORY = r"c:\Users\vaibh\Desktop\coep-scopus-web-dashboard"
OUTPUT_DIR = r"c:\Users\vaibh\Desktop\SCOPUS Dashboard\web_dashboard\scratch"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

server = socketserver.TCPServer(("", PORT), Handler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Desktop
        context = browser.new_context(viewport={"width": 1600, "height": 1200})
        page = context.new_page()
        page.goto(f"http://localhost:{PORT}/index.html", wait_until="networkidle")
        time.sleep(2)

        # Tab: Impact
        page.locator("button.tab-nav-btn:has-text('Impact')").first.click()
        time.sleep(1)
        page.locator("#tab-impact").scroll_into_view_if_needed()
        time.sleep(1)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "shot_impact_desktop.png"))

        # Tab: Collaboration
        page.locator("button.tab-nav-btn:has-text('Collaboration')").first.click()
        time.sleep(1)
        page.locator("#tab-collaboration").scroll_into_view_if_needed()
        time.sleep(1)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "shot_collab_desktop.png"))

        # Tab: Quality
        page.locator("button.tab-nav-btn:has-text('Quality')").first.click()
        time.sleep(1)
        page.locator("#tab-quality").scroll_into_view_if_needed()
        time.sleep(1)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "shot_quality_desktop.png"))
        
        # Scroll to radar chart on desktop
        page.locator("#chart-dept-radar").scroll_into_view_if_needed()
        time.sleep(1)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "shot_radar_desktop.png"))

        # Mobile
        m_context = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
        m_page = m_context.new_page()
        m_page.goto(f"http://localhost:{PORT}/index.html", wait_until="networkidle")
        time.sleep(2)

        m_page.locator("button.tab-nav-btn:has-text('Impact')").first.click()
        time.sleep(1)
        m_page.locator("#chart-citation-accrual").scroll_into_view_if_needed()
        time.sleep(1)
        m_page.screenshot(path=os.path.join(OUTPUT_DIR, "shot_impact_mobile.png"))

        m_page.locator("#chart-dept-cites").scroll_into_view_if_needed()
        time.sleep(1)
        m_page.screenshot(path=os.path.join(OUTPUT_DIR, "shot_dept_cites_mobile.png"))

        m_page.locator("button.tab-nav-btn:has-text('Collaboration')").first.click()
        time.sleep(1)
        m_page.locator("#chart-world-map").scroll_into_view_if_needed()
        time.sleep(1)
        m_page.screenshot(path=os.path.join(OUTPUT_DIR, "shot_collab_mobile.png"))

        m_page.locator("button.tab-nav-btn:has-text('Quality')").first.click()
        time.sleep(1)
        m_page.locator("#chart-quartile-donut").scroll_into_view_if_needed()
        time.sleep(1)
        m_page.screenshot(path=os.path.join(OUTPUT_DIR, "shot_donut_mobile.png"))

        m_page.locator("#chart-dept-radar").scroll_into_view_if_needed()
        time.sleep(1)
        m_page.screenshot(path=os.path.join(OUTPUT_DIR, "shot_radar_mobile.png"))

        browser.close()
finally:
    server.shutdown()
    print("Done")
