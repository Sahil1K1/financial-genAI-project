from pathlib import Path
import pandas as pd
import numpy as np
from src.utils.logger import get_logger

logger = get_logger('clean transform')

def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns = lambda x:x.strip())
    
    for col in df.columns:
        if 'data' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')
        elif 'revenue' in col.lower():
            df['Revenue_MA_30'] = df[col].rolling(30, min_periods=1).mean()
            df['Revenue_growth_pct'] = df[col].pct_change().fillna(0)

    return df


def process_sheet(csv_path: Path, out_path: Path):
    df = pd.read_csv(csv_path)
    logger.info(f'processing {csv_path} ({len(df)}) rows')
    df = basic_cleaning(df)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    # print(df)
    logger.info(f'processing done and saved in {out_path}')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='clean financial csv')
    parser.add_argument('--input', type=str, required=True) # here passing required and not default value if value is not provided in pipeline then this will throw an error
    parser.add_argument('--output', type=str, required=True)
    args = parser.parse_args()
    process_sheet(csv_path=Path(args.input), out_path=Path(args.output))


# checking this for one single file, dry run
# if __name__ == '__main__':
#     import argparse
#     parser = argparse.ArgumentParser(description='clean financial csv')
#     parser.add_argument('--input', type=str,  default='data/processed/P&L_Statement.csv')
#     parser.add_argument('--output', type=str, default='data/outputs/Cashflow_statement_cleaned.csv')
#     args = parser.parse_args()
#     process_sheet(csv_path=Path(args.input), out_path=Path(args.output))