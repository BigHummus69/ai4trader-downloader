import pandas as pd
portfolio_csv = "/Users/user/Documents/ai4trade/portfolio/ai4trade_portfolio_all_models.csv"
home_csv = "/Users/user/Documents/ai4trade/ai4trade_latest.csv"

df_portfolio = pd.read_csv(portfolio_csv)
df_home = pd.read_csv(home_csv)

df_portfolio['source'] = 'portfolio'
df_home['source'] = 'home'
df_combined = pd.concat([df_portfolio, df_home], ignore_index=True, sort=False)
combined_csv = "/Users/sriramshanmugam/Documents/ai4trade/combined_ai4trade_data.csv"
df_combined.to_csv(combined_csv, index=False)
print(f"✅ Combined CSV saved to {combined_csv}")
