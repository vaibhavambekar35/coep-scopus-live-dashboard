from playwright.sync_api import sync_playwright

def test_screen_sizes():
    resolutions = [
        ("1920x1080 (Full HD)", 1920, 1080),
        ("1536x864 (Standard Windows 125% scale)", 1536, 864),
        ("1366x768 (Standard Laptop)", 1366, 768),
        ("1280x720 (Compact Desktop)", 1280, 720),
        ("1024x768 (Tablet Landscape / Small Laptop)", 1024, 768),
        ("800x600 (Narrow Window)", 800, 600)
    ]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        for name, w, h in resolutions:
            context = browser.new_context(viewport={"width": w, "height": h})
            page = context.new_page()
            page.goto("https://coep-scopus-live-dashboard.streamlit.app", wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(4000)
            
            iframe = page.frame_locator('iframe[title="streamlitApp"]')
            
            sidebar = iframe.locator("section[data-testid='stSidebar']")
            is_sidebar_vis = False
            sidebar_aria = "none"
            if sidebar.count() > 0:
                is_sidebar_vis = sidebar.first.is_visible()
                sidebar_aria = sidebar.first.get_attribute("aria-expanded")
                
            expand_btn = iframe.locator("button[data-testid='stExpandSidebarButton'], [data-testid='collapsedControl']")
            is_expand_vis = False
            if expand_btn.count() > 0:
                is_expand_vis = expand_btn.first.is_visible()
                
            print(f"[{name}] Sidebar Vis: {is_sidebar_vis} | Aria: {sidebar_aria} | Expand Btn: {is_expand_vis}")
            page.screenshot(path=f"diag_{w}x{h}.png")
            context.close()
            
        browser.close()

if __name__ == "__main__":
    test_screen_sizes()
