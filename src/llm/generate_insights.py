import os
import logging
from src.utils.logger import get_logger
from src.llm.prompt_template2 import build_summary_prompt
from llama_index.llms.ollama import Ollama
import pandas as pd
import json
from pathlib import Path

logger = get_logger('generating insights')

response_json_file = Path(__file__).resolve().parent.parent.parent / 'data' / 'outputs' / 'output_data.json'

def call_llm(prompt: str, model: str = "llama3.1:8b") -> dict:
    logger.info('calling llm model')
    llm = Ollama(model=model, request_timeout=1800)
    logger.info('sending prompt to llm')
    response = llm.complete(prompt)
    response_txt = str(response)
    logger.info(f'received response: {response_txt}')
    return response_txt

def generate_summary(df, rows:int=20, model:str = "llama3.1:8b"):
    csv_snippet = df.head(rows).to_csv(index=False)
    prompt = build_summary_prompt(csv_snippet)
    result = call_llm(prompt=prompt, model=model)
    logger.info('response successfully generated from llm')
    response_json_file.parent.mkdir(parents=True, exist_ok=True)
    with open(response_json_file, 'w') as file:
        json.dump(result, file, indent=4)
    logger.info(f'response is saved in {response_json_file}')
    try:
        return json.loads(result)
    except Exception:
        return {'raw_text':result}

if __name__ == "__main__":
    logger.info('calling main function')
    test_df = pd.DataFrame({
        'Date': ['2024-01-01', '2024-02-01', '2024-03-01'],
        'Revenue': [100000, 110000, 105000],
        'Expenses': [60000, 65000, 63000],
        'EBITDA': [40000, 45000, 42000],
        'Free_Cash_Flow': [35000, 40000, 37000]
    })
    csv_path = Path().resolve() / 'data' / 'processed' / 'KPI_summary.csv'
    test_df2 = pd.read_csv(csv_path)
    result = generate_summary(test_df2)
    print(result)
    logger.info('Done!')