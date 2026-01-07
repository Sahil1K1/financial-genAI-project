import pandas as pd
import numpy as np
from pathlib import Path
import os
import openpyxl

num_rows = 2500
data = {
    "Date": pd.date_range(start="2023-01-01", periods=num_rows, freq="D"),
    "Revenue": np.random.randint(10000, 500000, num_rows),
    "Expenses": np.random.randint(5000, 300000, num_rows),
    "Profit" : np.random.randint(5000, 20000, num_rows),
    "Department": np.random.choice(["Finance", "Sales", "Operations", "R&D", "Marketing"], num_rows),
}


df = pd.DataFrame(data)
# print(df.info())

file_path = os.path.join((Path(__file__).resolve().parents[0]), 'Financial_data.xlsx')
print(file_path)
# df.to_excel(file_path, index=False)
print('done')

#######################################################

num_rows = 3000
dates = pd.date_range(start="2022-01-01", periods=num_rows, freq="D")

# Sheet 1: P&L Statement Data
pnl_data = {
    "Date": dates,
    "Revenue": np.random.randint(20000, 800000, num_rows),
    "COGS": np.random.randint(10000, 400000, num_rows),
    "Operating_Expenses": np.random.randint(5000, 200000, num_rows),
    "Interest_Expense": np.random.randint(500, 20000, num_rows),
    "Taxes": np.random.randint(500, 30000, num_rows),
}

pnl_df = pd.DataFrame(pnl_data)
pnl_df["Gross_Profit"] = pnl_df["Revenue"] - pnl_df["COGS"]
pnl_df["Operating_Income"] = pnl_df["Gross_Profit"] - pnl_df["Operating_Expenses"]
pnl_df["Net_Income"] = pnl_df["Operating_Income"] - pnl_df["Interest_Expense"] - pnl_df["Taxes"]
pnl_df["EBITDA"] = pnl_df["Operating_Income"] + pnl_df["Operating_Expenses"] + pnl_df["Interest_Expense"]

# Sheet 2: Cash Flow Statement Data
cashflow_data = {
    "Date": dates,
    "Net_Income": pnl_df["Net_Income"],
    "Depreciation": np.random.randint(2000, 15000, num_rows),
    "Change_in_Working_Capital": np.random.randint(-20000, 20000, num_rows),
    "Capital_Expenditures": np.random.randint(5000, 40000, num_rows),
    "Investments": np.random.randint(-50000, 50000, num_rows),
}

cashflow_df = pd.DataFrame(cashflow_data)
cashflow_df["Operating_Cash_Flow"] = (
    cashflow_df["Net_Income"]
    + cashflow_df["Depreciation"]
    + cashflow_df["Change_in_Working_Capital"]
)
cashflow_df["Free_Cash_Flow"] = (
    cashflow_df["Operating_Cash_Flow"]
    - cashflow_df["Capital_Expenditures"]
)

# Sheet 3: KPI Summary
kpi_data = {
    "Date": dates,
    "ROI": np.random.uniform(5, 35, num_rows),
    "ROE": np.random.uniform(8, 40, num_rows),
    "ROA": np.random.uniform(2, 20, num_rows),
    "Debt_to_Equity": np.random.uniform(0.1, 3.5, num_rows),
    "Current_Ratio": np.random.uniform(0.8, 3.0, num_rows),
}

kpi_df = pd.DataFrame(kpi_data)

# print(pnl_df)
# print(cashflow_df)
# print(kpi_df)

# now saving each of these dataframe into one single excel file but in 3 different sheets
file_path2 = os.path.join((Path(__file__).resolve().parents[0]), "Financial_data_final.xlsx")

with pd.ExcelWriter(file_path2, 'openpyxl') as writer:
    pnl_df.to_excel(writer, sheet_name='P&L Statement', index=False)
    cashflow_df.to_excel(writer, sheet_name='Cashflow statement', index=False)
    kpi_df.to_excel(writer, sheet_name='KPI summary', index=False)

print('done')