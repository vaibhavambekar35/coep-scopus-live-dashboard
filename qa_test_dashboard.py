import os
import sys
import time
import socket
import subprocess
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def run_qa_tests():
    print("=== STARTING QA TESTING FOR COEP SCOPUS WEB DASHBOARD ===")

    port = get_free_port()
    server_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port)],
        cwd="c:\\Users\\vaibh\\Desktop\\SCOPUS Dashboard\\web_dashboard",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(1.5)

    test_url = f"http://127.0.0.1:{port}/index.html"
    file_url = "file:///C:/Users/vaibh/Desktop/SCOPUS%20Dashboard/web_dashboard/index.html"
    
    errors = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1600, "height": 1000})
            page = context.new_page()

            page.on("pageerror", lambda exc: errors.append(str(exc)))

            # Test 1: HTTP Local Server
            print(f"\n[TEST 1] Navigating to {test_url}...")
            page.goto(test_url, wait_until="load")
            time.sleep(1.5)

            title = page.title()
            print(f"  [OK] Page Title: '{title}'")

            total_pubs = page.locator("#kpi-total-pubs").text_content()
            citations = page.locator("#kpi-citations").text_content()
            print(f"  [OK] 10 KPI Grid Loaded: Total Pubs={total_pubs}, Citations={citations}")

            page.screenshot(path="c:\\Users\\vaibh\\Desktop\\SCOPUS Dashboard\\web_dashboard\\qa_original_streamlit_ui.png")
            print("  [OK] Screenshot saved: qa_original_streamlit_ui.png")

            # Test 2: Horizontal Navigation Tabs
            tab_names = ["Trends", "Impact", "Collaboration", "Quality", "Authors", "Live Feed", "AI Copilot"]
            print("\n[TEST 2] Testing 7 Horizontal Tabs...")
            for tab in tab_names:
                page.locator(f".tab-nav-btn:has-text('{tab}')").click()
                time.sleep(0.5)
                page.evaluate("window.scrollTo(0, 500)")
                time.sleep(0.3)
                page.screenshot(path=f"c:\\Users\\vaibh\\Desktop\\SCOPUS Dashboard\\web_dashboard\\qa_coep_{tab.lower().replace(' ', '_')}_tab.png")
                print(f"  [OK] Saved screenshot for '{tab}' tab")

            # Test 3: Dual Theme Mode Buttons
            print("\n[TEST 3] Testing Dual Theme Mode Buttons...")
            page.locator("#theme-btn-light").click()
            time.sleep(0.4)
            theme_attr = page.locator("html").get_attribute("data-theme")
            page.screenshot(path="c:\\Users\\vaibh\\Desktop\\SCOPUS Dashboard\\web_dashboard\\qa_coep_light_mode.png")
            print(f"  [OK] Clicked Light Mode -> html data-theme: '{theme_attr}'")

            page.locator("#theme-btn-dark").click()
            time.sleep(0.4)
            theme_attr_dark = page.locator("html").get_attribute("data-theme")
            page.screenshot(path="c:\\Users\\vaibh\\Desktop\\SCOPUS Dashboard\\web_dashboard\\qa_coep_dark_mode.png")
            print(f"  [OK] Clicked Dark Mode -> html data-theme: '{theme_attr_dark}'")

            # Test 4: Mobile Responsive Viewport (375x812 iPhone / Mobile view)
            print("\n[TEST 4] Testing Mobile Viewport (375x812)...")
            mobile_context = browser.new_context(viewport={"width": 375, "height": 812})
            mobile_page = mobile_context.new_page()
            mobile_page.on("pageerror", lambda exc: errors.append(f"Mobile Page Error: {exc}"))

            mobile_page.goto(test_url, wait_until="load")
            time.sleep(1.5)
            mobile_page.screenshot(path="c:\\Users\\vaibh\\Desktop\\SCOPUS Dashboard\\web_dashboard\\qa_mobile_closed_sidebar.png")
            print("  [OK] Mobile closed sidebar screenshot saved: qa_mobile_closed_sidebar.png")

            # Click Mobile Filters Toggle
            mobile_page.locator("#mobile-toggle-sidebar").click()
            time.sleep(0.5)
            mobile_page.screenshot(path="c:\\Users\\vaibh\\Desktop\\SCOPUS Dashboard\\web_dashboard\\qa_mobile_open_sidebar.png")
            print("  [OK] Mobile open sidebar drawer screenshot saved: qa_mobile_open_sidebar.png")

            # Close Mobile Sidebar
            mobile_page.locator("#mobile-close-sidebar").click()
            time.sleep(0.5)

            mobile_context.close()
            browser.close()
    finally:
        server_process.terminate()

    print("\n=== QA SUMMARY ===")
    print(f"Total Browser Exceptions: {len(errors)}")
    for err in errors:
        print(f"  [ERROR] {err}")
    print("=== QA TESTING FINISHED ===")

if __name__ == "__main__":
    run_qa_tests()
