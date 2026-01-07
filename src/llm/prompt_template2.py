from typing import Dict

SUMMARY_PROMPT = """
You are a helpful financial analyst. Given the following monthly KPI table (columns: Date, Revenue, Expenses, EBITDA, Free_Cash_Flow), produce:
- A short executive summary (3 sentences)
- Top 3 risks (bullet list)
- Top 3 opportunities (bullet list)
- Two suggested strategic actions with rationale


Data:
{data_table}


Respond in JSON with fields: executive_summary, risks (list), opportunities (list), actions (list of objects with title and rationale).
"""

PROMPT_TEMPLATE_SHORT = SUMMARY_PROMPT

def build_summary_prompt(table_csv: str) -> str:
    return PROMPT_TEMPLATE_SHORT.format(data_table=table_csv)


# for testing
if __name__ == "__main__":
    test_df = """
    Date,Revenue,Expenses,EBITDA,Free_Cash_Flow
    2024-01-01,100000,60000,40000,35000
    2024-02-01,110000,65000,45000,40000
    2024-03-01,105000,63000,42000,37000
    """
    final_prompt = build_summary_prompt(test_df)
    print(final_prompt)
