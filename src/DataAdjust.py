import pandas as pd
'''
DataAdjust.py
3. Drop rows with any N/A values.
4. Group the data by 'Symbol'.
5. For each group, create a summary row containing:
    - Symbol
    - Start Date
    - End Date
    - Original Adjusted Close
    - Final Adjusted Close
    - Original Earnings
    - Final Earnings
    - Original P/E Ratio
    - Final P/E Ratio
6. Write the summary data to 'stocks_summary_one_row.csv'.
  '''

# Read the CSV
df = pd.read_csv("stocks_calc_final.csv")

# Ensure Date is recognized as a datetime for proper sorting
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Drop rows with any N/A values
df_clean = df.dropna()

# Group by symbol
grouped = df_clean.groupby("Symbol", group_keys=True)

summary_rows = []
for symbol, group in grouped:
    # Sort by Date so the first row is the earliest date, the last row is the latest date
    group_sorted = group.sort_values("Date")
    first_row = group_sorted.iloc[0]
    last_row = group_sorted.iloc[-1]
    
    # Create a single summary row for this symbol
    summary_rows.append({
        "Symbol": symbol,
        "Start Date": first_row["Date"].strftime("%Y-%m-%d"),
        "End Date": last_row["Date"].strftime("%Y-%m-%d"),
        "Original Adjusted Close": first_row["Adjusted Close"],
        "Final Adjusted Close": last_row["Adjusted Close"],
        "Original Earnings": first_row["Earnings"],
        "Final Earnings": last_row["Earnings"],
        "Original P/E Ratio": first_row["P/E Ratio"],
        "Final P/E Ratio": last_row["P/E Ratio"]
    })

# Create a new DataFrame and write to CSV
summary_df = pd.DataFrame(summary_rows)
summary_df.to_csv("stocks_summary_one_row.csv", index=False)



"""
This script processes stock data from a CSV file, calculates trailing twelve months (TTM) earnings per share (EPS) 
and price-to-earnings (P/E) ratios, and outputs the results to a new CSV file.
Steps:
1. Read stock data from 'stocks_calc_final.csv'.
2. Convert the 'Date' column to datetime format and sort the data by 'Symbol' and 'Date'.
3. Group the data by 'Symbol'.
4. For each group, calculate the TTM EPS and P/E ratios:
    - Initialize 'EPS (ttm)' and 'P/E (ttm)' columns with NaN values.
    - For each row, if there are enough previous rows (189 days), calculate the TTM EPS as the sum of earnings 
      from the current row and the rows 63, 126, and 189 days prior.
    - Calculate the TTM P/E ratio as the adjusted close price divided by the TTM EPS.
5. Concatenate the processed groups and write the final DataFrame to 'stocks_calc_final_with_ttm.csv'.
Output:
- 'stocks_calc_final_with_ttm.csv': A CSV file containing the original data along with the calculated 'EPS (ttm)' 
  and 'P/E (ttm)' columns.
"""
import pandas as pd
import numpy as np

df = pd.read_csv("stocks_calc_final.csv")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.sort_values(["Symbol", "Date"])

output_groups = []

for symbol, group in df.groupby("Symbol", group_keys=False):
    # Sort by date, reset index so each row has a clean 0..N index
    group = group.sort_values("Date").reset_index(drop=True)
    
    # Initialize columns
    group["EPS (ttm)"] = np.nan
    group["P/E (ttm)"] = np.nan
    
    for i in range(len(group)):
        if i >= 189:  # Enough rows
            earnings_values = [
                group.at[i, "Earnings"],
                group.at[i-63, "Earnings"],
                group.at[i-126, "Earnings"],
                group.at[i-189, "Earnings"]
            ]
            if all(pd.notna(earnings_values)) and all(earnings_values):
                eps_ttm = sum(earnings_values)
                group.at[i, "EPS (ttm)"] = eps_ttm
                if eps_ttm != 0:
                    group.at[i, "P/E (ttm)"] = group.at[i, "Adjusted Close"] / eps_ttm
    
    output_groups.append(group)

final_df = pd.concat(output_groups, ignore_index=True)
final_df.to_csv("stocks_calc_final_with_ttm.csv", index=False)