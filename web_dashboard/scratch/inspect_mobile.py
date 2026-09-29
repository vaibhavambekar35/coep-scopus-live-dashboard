import http.server
import threading
import time
import os
import json
from playwright.sync_api import sync_playwright

PORT = 8996
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
        # Mobile viewport 390x844 (iPhone 12/13/14)
        m_page = browser.new_page(viewport={"width": 390, "height": 844})
        m_page.goto(f"http://localhost:{PORT}/index.html", wait_until="load")
        time.sleep(3)

        # Check overflow on mobile
        def check_overflow(tab_name):
            return m_page.evaluate("""() => {
                const docWidth = document.documentElement.clientWidth;
                const winWidth = window.innerWidth;
                const scrollWidth = document.documentElement.scrollWidth;
                const bodyScrollWidth = document.body.scrollWidth;
                const overflowing = [];
                const all = document.querySelectorAll('*');
                for (const el of all) {
                    const rect = el.getBoundingClientRect();
                    if (rect.right > winWidth + 2) {
                        overflowing.push({
                            tag: el.tagName,
                            id: el.id,
                            cls: (el.className && typeof el.className === 'string') ? el.className.slice(0, 50) : '',
                            right: Math.round(rect.right),
                            width: Math.round(rect.width)
                        });
                    }
                }
                return { winWidth, docWidth, scrollWidth, bodyScrollWidth, overflowing: overflowing.slice(0, 15) };
            }""")

        print("--- Home / Trends tab overflow ---")
        print(json.dumps(check_overflow("Trends"), indent=2))

        # Switch to Impact tab
        m_page.locator('button.tab-nav-btn:has-text("Impact")').first.click()
        time.sleep(1)
        print("--- Impact tab overflow ---")
        print(json.dumps(check_overflow("Impact"), indent=2))
        
        # Take card screenshots on Impact tab
        card_accrual = m_page.locator("#chart-citation-accrual").locator("xpath=..")
        card_accrual.screenshot(path=os.path.join(OUTPUT_DIR, "card_mobile_accrual.png"))
        card_dept = m_page.locator("#chart-dept-cites").locator("xpath=..")
        card_dept.screenshot(path=os.path.join(OUTPUT_DIR, "card_mobile_dept_cites.png"))

        # Switch to Collaboration tab
        m_page.locator('button.tab-nav-btn:has-text("Collaboration")').first.click()
        time.sleep(1)
        print("--- Collaboration tab overflow ---")
        print(json.dumps(check_overflow("Collaboration"), indent=2))
        card_map = m_page.locator("#chart-world-map").locator("xpath=..")
        card_map.screenshot(path=os.path.join(OUTPUT_DIR, "card_mobile_world_map.png"))
        card_partner = m_page.locator("#chart-partner-countries").locator("xpath=..")
        card_partner.screenshot(path=os.path.join(OUTPUT_DIR, "card_mobile_partner_countries.png"))

        # Switch to Quality tab
        m_page.locator('button.tab-nav-btn:has-text("Quality")').first.click()
        time.sleep(1)
        print("--- Quality tab overflow ---")
        print(json.dumps(check_overflow("Quality"), indent=2))
        card_donut = m_page.locator("#chart-quartile-donut").locator("xpath=..")
        card_donut.screenshot(path=os.path.join(OUTPUT_DIR, "card_mobile_donut.png"))
        card_bubble = m_page.locator("#chart-impact-bubble").locator("xpath=..")
        card_bubble.screenshot(path=os.path.join(OUTPUT_DIR, "card_mobile_bubble.png"))
        card_radar = m_page.locator("#chart-dept-radar").locator("xpath=..")
        card_radar.screenshot(path=os.path.join(OUTPUT_DIR, "card_mobile_radar.png"))

        browser.close()
        print("Mobile inspection completed successfully.")
finally:
    server.shutdown()
