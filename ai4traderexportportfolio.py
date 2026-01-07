from playwright.sync_api import sync_playwright
import csv
import os
import time

OUTPUT_DIR = "/Users/user/Documents/ai4trade/portfolio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

output_csv_portfolio = f"{OUTPUT_DIR}/ai4trade_portfolio_all_models.csv"

all_rows = []
headers_saved = False

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(
        "https://ai4trade.ai/portfolio.html",
        wait_until="domcontentloaded",
        timeout=60000
    )

    # Wait for initial loading overlay to disappear
    try:
        page.wait_for_selector("#loadingOverlay", state="hidden", timeout=60000)
    except:
        pass

    # ---- STEP 1: Get all model options ----
    model_options = page.eval_on_selector_all(
        "#agentSelect option",
        "opts => opts.map(o => ({ value: o.value, text: o.innerText.trim() }))"
    )

    print(f"Found {len(model_options)} models")

    for model in model_options:
        print(f"▶ Loading model: {model['text']}")

        # ---- STEP 2: Select model ----
        page.select_option("#agentSelect", model["value"])

        # ---- STEP 3: Wait for portfolio reload ----
        try:
            page.wait_for_selector("#loadingOverlay", state="hidden", timeout=60000)
        except:
            pass

        time.sleep(1)  # DOM stabilization

        # ---- STEP 4: Extract headers once ----
        if not headers_saved:
            headers = page.eval_on_selector_all(
                "table thead th",
                "ths => ths.map(th => th.innerText.trim())"
            )
            headers = ["model"] + headers
            headers_saved = True

        # ---- STEP 5: Extract rows ----
        rows = page.eval_on_selector_all(
            "table tbody tr",
            """trs => trs.map(tr =>
                Array.from(tr.querySelectorAll('td'))
                    .map(td => td.innerText.trim())
            )"""
        )

        for row in rows:
            all_rows.append([model["text"]] + row)

    browser.close()

# ---- STEP 6: Write CSV ----
with open(output_csv_portfolio, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(all_rows)

print(f"✅ All model portfolios saved to {output_csv_portfolio}")
