from pathlib import Path
import os
import pandas as pd


def load_dataset():
    file_path = os.path.join((Path(__file__).resolve().parents[2]), 'data', 'raw')
    files_list = []
    for files in os.listdir(file_path):
        # print(files)
        if files.endswith('.xlsx'):
            excel_file = pd.ExcelFile(os.path.join(file_path, files))
            for sheet_names in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_names)
                files_list.append(df)
        elif files.endswith('.csv'):
            df = pd.read_csv(os.path.join(file_path, files))
            files_list.append(df)
    return files_list

# print(load_dataset())