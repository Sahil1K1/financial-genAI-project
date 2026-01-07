import json
from pathlib import Path
from src.ingestion.load_data2 import load_excel_to_dfs, save_processed
from src.preprocessing.clean_transform import basic_cleaning, process_sheet
from src.llm.prompt_template2 import build_summary_prompt
from src.llm.generate_insights import call_llm, generate_summary
import logging
from src.utils.logger import get_logger
import pandas as pd

logger = get_logger('pipeline')
logger.info('pipeline file execution started')

DEFAULT_RAW = Path('data/raw/Financial_data_final.xlsx')

"""covering ingesting > preprocessing > LLM insights"""

def final_pipeline(raw_excel_path: Path, processed_path: Path, output_dir: Path):
    processed_dir = Path(processed_path)
    output_dirs = Path(output_dir)
    output_dirs.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    # loading sheets
    sheets = load_excel_to_dfs(raw_excel_path)
    # return sheets

    # saving sheets
    save_processed(sheets=sheets, output_dir=processed_dir)
    
    # generating summaries
    summaries = {}
    all_dfs = {}
    for sheet_name in sheets:
        input_csv = processed_dir / f"{sheet_name.replace(' ','_')}.csv"
        output_csv = output_dirs / f"processed_{sheet_name.replace(' ', '_')}.csv"
        process_sheet(csv_path=input_csv, out_path=output_csv)
        
        df = pd.read_csv(output_csv)
        logger.info('DataFrame created successfully')
        df = basic_cleaning(df)
        logger.info('basic cleaning is done')
        all_dfs[sheet_name] = df
    # return all_dfs
    combined_context = build_combined_df(all_dfs)
    # return combined_context
    final_prompt = build_summary_prompt(combined_context)
    # return type(final_prompt)
    try:
        summary = final_generate_summary(final_prompt)
    except Exception as e:
        logger.warning(f'LLM failed: {e}')
        summary = {"error":str(e)}
    if isinstance(summary, str):
        try:
            summary_dict = json.loads(summary)
        except json.JSONDecodeError:
            summary_dict = {'raw_response': summary}
    
    summaries_path = output_dirs / "llm_output.json"
    summaries_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summaries_path, 'w') as file:
        json.dump(summary_dict, fp=file, indent=4, ensure_ascii=False) # apart from the content, here files needs to be mentioned as well.
    logger.info(f"summary is saved to {summaries_path} successfully")
    return summaries_path

def build_combined_df(dataframes_dict : dict) -> str:
    """converting all dfs into single item and in string form"""
    all_context = []
    logger.info('appending all sheets in one')
    for sheet_name, df in dataframes_dict.items():
        all_context.append("="*60)
        all_context.append(f"Sheet: {sheet_name}")
        all_context.append("="*60)
        all_context.append(f"Rows: {len(df)}, Columns: {list(df.columns)}")

        df = df.to_csv(index=False)
        all_context.append(df)
        all_context.append("")
    combined_text = '\n'.join(all_context)
    logger.info('appending process completed')
    return combined_text

def final_generate_summary(prompt: str):
    logger.info('calling llm and passig prompt')
    llm_response = call_llm(prompt=prompt, model='llama3.1:8b')
    logger.info('response generated successfully')
    return llm_response


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser('final pipeline')
    parser.add_argument('--raw',type=str, default=str(DEFAULT_RAW))
    parser.add_argument('--processed', type=str, default='data/processed')
    parser.add_argument('--output', type=str, default='data/outputs')
    args = parser.parse_args()
    final_pipeline(raw_excel_path=Path(args.raw), processed_path=Path(args.processed), output_dir=Path(args.output))