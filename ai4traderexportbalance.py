from playwright.sync_api import sync_playwright
import os

DOWNLOAD_DIR = "/Users/user/Documents/ai4trade"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

output_csv_home = f"{DOWNLOAD_DIR}/ai4trade_latest.csv"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    page.goto(
        "https://ai4trade.ai",
        wait_until="domcontentloaded",
        timeout=60000
    )

    # Wait for overlay to disappear
    page.wait_for_selector("#loadingOverlay", state="hidden", timeout=60000)

    # Wait for Export Data button
    page.wait_for_selector("#export-chart", timeout=20000)

    # Click and download
    with page.expect_download() as download_info:
        page.click("#export-chart")

    download = download_info.value
    download.save_as(output_csv_home)

    browser.close()

print(f"✅ Export complete: {output_csv_home}")
