from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 1200})
    page.goto("file:///c:/Users/vaibh/Desktop/coep-scopus-web-dashboard/index.html")
    page.wait_for_timeout(2500)
    
    # Impact
    page.locator('button.tab-nav-btn:has-text("Impact")').first.click()
    page.wait_for_timeout(1000)
    page.locator("#chart-dept-cites").screenshot(path="c:/Users/vaibh/Desktop/SCOPUS Dashboard/web_dashboard/scratch/shot_dept_cites_elem.png")
    page.locator("#chart-citation-accrual").screenshot(path="c:/Users/vaibh/Desktop/SCOPUS Dashboard/web_dashboard/scratch/shot_accrual_elem.png")

    # Collab
    page.locator('button.tab-nav-btn:has-text("Collaboration")').first.click()
    page.wait_for_timeout(1000)
    page.locator("#chart-world-map").screenshot(path="c:/Users/vaibh/Desktop/SCOPUS Dashboard/web_dashboard/scratch/shot_world_map_elem.png")
    page.locator("#chart-partner-countries").screenshot(path="c:/Users/vaibh/Desktop/SCOPUS Dashboard/web_dashboard/scratch/shot_partner_elem.png")
    page.locator("#chart-industry-collab-dept").screenshot(path="c:/Users/vaibh/Desktop/SCOPUS Dashboard/web_dashboard/scratch/shot_industry_elem.png")

    # Quality
    page.locator('button.tab-nav-btn:has-text("Quality")').first.click()
    page.wait_for_timeout(1000)
    page.locator("#chart-quartile-donut").screenshot(path="c:/Users/vaibh/Desktop/SCOPUS Dashboard/web_dashboard/scratch/shot_donut_elem.png")
    page.locator("#chart-impact-bubble").screenshot(path="c:/Users/vaibh/Desktop/SCOPUS Dashboard/web_dashboard/scratch/shot_bubble_elem.png")
    page.locator("#chart-dept-radar").screenshot(path="c:/Users/vaibh/Desktop/SCOPUS Dashboard/web_dashboard/scratch/shot_radar_elem.png")

    browser.close()
print("All element screenshots captured successfully!")
