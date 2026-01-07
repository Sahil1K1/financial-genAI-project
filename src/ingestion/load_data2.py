from pathlib import Path
import pandas as pd
import logging
from src.utils.logger import get_logger

logger = get_logger('load_data')

DEFAULT_RAW = Path('data/raw/Financial_data_final.xlsx')
# print(DEFAULT_RAW)

def load_excel_to_dfs(path: Path = None):
    path = Path(path) if path is not None else DEFAULT_RAW
    path = path.resolve()
    # print(f'printing path inside of function: {path}')
    if not path.exists():
        logger.error(f'Raw data is not found at {Path}')
        raise FileNotFoundError(path)
    logger.info(f'Loading Excel from {path}')
    xls = pd.ExcelFile(path)
    sheets = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
    logger.info(f'Loaded sheets: {list(sheets.keys())}') # this logger info is used for printing the message in terminal without using print statment and also it will print the output with time and file_information like from which file this part is coming in
    # can utilize this anywhere we needed to know the progress of something
    return sheets

def save_processed(sheets: dict, output_dir: Path):
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, df in sheets.items():
        fname = out_dir / f"{name.replace(' ','_')}.csv"
        df.to_csv(fname, index=False)
        logger.info(f'wrote {fname} ({len(df)}) rows')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='load raw excel and save CSVs')
    parser.add_argument('--raw', type=str, default=str(DEFAULT_RAW)) # this will be used as an input, to access this args.raw
    parser.add_argument('--out', type=str, default='data/processed') # to access this args.out
    args = parser.parse_args()
    sheets = load_excel_to_dfs(Path(args.raw))
    save_processed(sheets=sheets, output_dir=Path(args.out))
