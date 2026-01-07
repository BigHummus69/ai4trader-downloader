import pandas as pd
from playwright.sync_api import sync_playwright
import os
import csv
import time

HOME_DIR = "/Users/user/Documents/ai4trade/balance"
os.makedirs(HOME_DIR, exist_ok=True)

output_csv_home = f"{HOME_DIR}/ai4trade_latest.csv"

PORTFOLIO_DIR = "/Users/sriramshanmugam/Documents/ai4trade/portfolio"
os.makedirs(PORTFOLIO_DIR, exist_ok=True)

output_csv_portfolio = f"{PORTFOLIO_DIR}/ai4trade_portfolio_all_models.csv"

all_rows = []
headers_saved = False


#----BALANCE EXPORT ----#
balance_success = False
try: # had to use this since my python kept crashing like crazy, its now part of final product
    with sync_playwright() as p: # assign p to sync_playwright so we can do stuff with it
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        page.goto(
            "https://ai4trade.ai",
            wait_until="domcontentloaded",
            timeout=60000
        )

        # Wait for overlay to disappear, there was a massive delay because of both Balance and Portfolio loading
        try:
            page.wait_for_selector("#loadingOverlay", state="hidden", timeout=60000)
        except:
            time.sleep(7)  # Fallback wait just in case


        # Wait for Export Data button
        page.wait_for_selector("#export-chart", timeout=20000)

        # download
        with page.expect_download() as download_info:
            page.click("#export-chart") # this is the id for the download button

        download = download_info.value
        download.save_as(output_csv_home)

        browser.close()

    print("Balance export completed successfully.")
    balance_success = True # turn to true so portfolio export can happen, boolean logic so if not true, the entire balance_success dosen't exist
except Exception as e:
    print(f"Balance export failed: {e}") # i aint elaborating on this

if balance_success:
    #----PORTFOLIO EXPORT ----#
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
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
            time.sleep(7)

        # adding steps because this is the complicated one

        # ----STEP 1: Get all models----
        model_options = page.eval_on_selector_all(
            "#agentSelect option",
            "opts => opts.map(o => ({ value: o.value, text: o.innerText.trim() }))"
        )

        print(f"Found {len(model_options)} models")

        for model in model_options:
            print(f"▶ Loading model: {model['text']}") # really cool thing, just look at that console go!

            # ----STEP 2: Select model----
            page.select_option("#agentSelect", model["value"])

            # ----STEP 3: Wait for portfolio reload----
            try:
                page.wait_for_selector("#loadingOverlay", state="hidden", timeout=60000)
            except:
                pass

            time.sleep(1)  # DOM stabilization so we don't crash, you'll have to increase if you have bad internet

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



    print(f"✅ Export complete: Portfolio data saved to {output_csv_portfolio}", f" and Balance data saved to {output_csv_home}")
else:
    print("Portfolio export skipped because balance export failed.") # haha funny if else statement ends

#----COMBINE CSV----#
portfolio_csv = "/Users/sriramshanmugam/Documents/ai4trade/portfolio/ai4trade_portfolio_all_models.csv"
home_csv = "/Users/sriramshanmugam/Documents/ai4trade/balance/ai4trade_latest.csv"

df_portfolio = pd.read_csv(portfolio_csv) #use pd to read csv
df_home = pd.read_csv(home_csv)

df_home['source'] = 'home' #add a column to identify source
df_combined = pd.concat([df_portfolio, df_home], ignore_index=True, sort=False) #concentate (idk what that means, it's just combining) both csvs
combined_csv = "/Users/sriramshanmugam/Documents/ai4trade/combined_ai4trade_data.csv" 
df_combined.to_csv(combined_csv, index=False)
print(f"✅ Combined CSV saved to {combined_csv}")

print("The combined CSV is very cooked, I didn't want to go through the effort of combining simillar columns so it's essentially just two CSV's in one big one. Either way, if you're using the website, you shouldn't need it anyway, you should use the individual CSV's for balance and portfolio separately.")
