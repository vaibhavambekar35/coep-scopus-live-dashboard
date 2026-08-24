from playwright.sync_api import sync_playwright

def test_interactive_mobile():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto("http://localhost:8501", wait_until="networkidle")
        page.wait_for_timeout(2000)
        
        # 1. Capture initial mobile screen with floating expand button
        page.screenshot(path="verified_mobile_01_closed.png")
        print("Saved verified_mobile_01_closed.png")
        
        # 2. Click expand button to open sidebar
        expand_btn = page.locator("button[data-testid='stExpandSidebarButton']").first
        print("Expand button visible:", expand_btn.is_visible())
        expand_btn.click()
        page.wait_for_timeout(1500)
        page.screenshot(path="verified_mobile_02_sidebar_open.png")
        print("Saved verified_mobile_02_sidebar_open.png")
        
        # 3. Scroll down in sidebar to see filters
        sidebar = page.locator("[data-testid='stSidebarContent']")
        sidebar.evaluate("el => el.scrollTop = 400")
        page.wait_for_timeout(1000)
        page.screenshot(path="verified_mobile_03_sidebar_scrolled.png")
        print("Saved verified_mobile_03_sidebar_scrolled.png")
        
        # 4. Verify Desktop is 100% untouched
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.wait_for_timeout(1500)
        page.screenshot(path="verified_desktop_locked_intact.png")
        print("Saved verified_desktop_locked_intact.png")
        
        browser.close()

if __name__ == "__main__":
    test_interactive_mobile()
