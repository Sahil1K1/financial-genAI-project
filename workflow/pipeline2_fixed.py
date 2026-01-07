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
    """
    Complete data pipeline: ingestion -> preprocessing -> LLM analysis
    
    Args:
        raw_excel_path: Path to raw Excel file
        processed_path: Directory for processed CSV files
        output_dir: Directory for final outputs
        
    Returns:
        Path: Path to the saved summary JSON file
    """
    processed_dir = Path(processed_path)
    output_dirs = Path(output_dir)
    output_dirs.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Loading sheets
    logger.info('Step 1: Loading Excel sheets...')
    sheets = load_excel_to_dfs(raw_excel_path)
    logger.info(f'Loaded {len(sheets)} sheets: {list(sheets.keys())}')

    # Step 2: Saving sheets to processed directory
    logger.info('Step 2: Saving sheets to processed directory...')
    save_processed(sheets=sheets, output_dir=processed_dir)
    
    # Step 3: Processing and cleaning all sheets
    logger.info('Step 3: Processing and cleaning sheets...')
    all_dfs = {}
    for sheet_name in sheets:
        logger.info(f'Processing sheet: {sheet_name}')
        input_csv = processed_dir / f"{sheet_name.replace(' ','_')}.csv"
        # ✅ Fixed: Use output_dirs instead of output_dir
        output_csv = output_dirs / f"processed_{sheet_name.replace(' ', '_')}.csv"
        
        # Clean and transform the data
        process_sheet(csv_path=input_csv, out_path=output_csv)
        
        # ✅ Fixed: Limit rows to reduce token usage and prevent timeout
        df = pd.read_csv(output_csv).head(100)  # Use first 100 rows
        all_dfs[sheet_name] = df
        logger.info(f'Loaded {len(df)} rows from {sheet_name}')
    
    # Step 4: Combine all sheets into single context
    logger.info('Step 4: Combining all sheets into single context...')
    combined_context = build_combined_df(all_dfs)
    logger.info(f'Combined context size: {len(combined_context)} characters')
    
    # Step 5: Build final prompt
    logger.info('Step 5: Building final prompt for LLM...')
    final_prompt = build_summary_prompt(combined_context)
    logger.info(f'Final prompt size: {len(final_prompt)} characters')
    
    # Step 6: Generate summary from LLM
    logger.info('Step 6: Generating comprehensive summary from LLM...')
    try:
        summary = final_generate_summary(final_prompt)
        logger.info('✅ Summary generated successfully')
    except Exception as e:
        logger.error(f'❌ LLM failed: {e}')
        summary = {"error": str(e), "error_type": type(e).__name__}
    
    # Step 7: Save summary to JSON file
    logger.info('Step 7: Saving summary to JSON file...')
    summaries_path = output_dirs / "llm_output.json"
    summaries_path.parent.mkdir(parents=True, exist_ok=True)
    
    # ✅ Fixed: Handle both string and dict responses
    if isinstance(summary, str):
        try:
            # Try to parse as JSON
            summary_dict = json.loads(summary)
            logger.info('Successfully parsed LLM response as JSON')
        except json.JSONDecodeError as e:
            logger.warning(f'LLM response is not valid JSON: {e}')
            # Wrap raw text response
            summary_dict = {"raw_response": summary}
    else:
        summary_dict = summary
    
    # ✅ Fixed: Write to file properly
    with open(summaries_path, 'w', encoding='utf-8') as file:
        json.dump(summary_dict, file, indent=4, ensure_ascii=False)
    
    logger.info(f"✅ Summary saved to {summaries_path} successfully")
    
    # Verify file was written
    if summaries_path.exists() and summaries_path.stat().st_size > 0:
        logger.info(f"File size: {summaries_path.stat().st_size} bytes")
    else:
        logger.warning("⚠️ Warning: Output file may be empty!")
    
    return summaries_path


def build_combined_df(dataframes_dict: dict) -> str:
    """
    Convert all DataFrames into a single combined string with proper formatting
    
    Args:
        dataframes_dict: Dictionary with sheet_name as key and DataFrame as value
        
    Returns:
        str: Combined context string with all financial data
    """
    all_context = []
    logger.info('Building combined context from all sheets...')
    
    for sheet_name, df in dataframes_dict.items():
        all_context.append("=" * 60)
        all_context.append(f"Sheet: {sheet_name}")
        all_context.append("=" * 60)
        all_context.append(f"Rows: {len(df)}, Columns: {list(df.columns)}")
        all_context.append("")  # Empty line for readability
        
        # Convert DataFrame to CSV string
        csv_data = df.to_csv(index=False)
        all_context.append(csv_data)
        all_context.append("")  # Empty line between sheets
    
    combined_text = '\n'.join(all_context)
    logger.info(f'Combined context created: {len(combined_text)} characters')
    return combined_text


def final_generate_summary(prompt: str, model: str = 'llama3.1:8b'):
    """
    Generate comprehensive financial summary using LLM
    
    Args:
        prompt: The formatted prompt with all financial data
        model: LLM model to use (default: llama3.1:8b)
        
    Returns:
        str: LLM response text
    """
    logger.info(f'Calling LLM model: {model}')
    logger.info(f'Prompt length: {len(prompt)} characters')
    
    # Call LLM with the prompt
    llm_response = call_llm(prompt=prompt, model=model)
    
    logger.info(f'Response generated successfully: {len(llm_response)} characters')
    logger.debug(f'Response preview: {llm_response[:200]}...')
    
    return llm_response


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Final comprehensive financial analysis pipeline')
    parser.add_argument('--raw', type=str, default=str(DEFAULT_RAW), 
                       help='Path to raw Excel file')
    parser.add_argument('--processed', type=str, default='data/processed',
                       help='Directory for processed CSV files')
    parser.add_argument('--output', type=str, default='data/outputs',
                       help='Directory for final outputs')
    
    args = parser.parse_args()
    
    try:
        # Run the pipeline
        result_path = final_pipeline(
            raw_excel_path=Path(args.raw),
            processed_path=Path(args.processed),
            output_dir=Path(args.output)
        )
        
        # Print success message
        print("\n" + "=" * 60)
        print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"📄 Output saved to: {result_path}")
        
        # Show preview of output
        if result_path.exists():
            with open(result_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            print(f"\n📊 Output preview:")
            print(json.dumps(content, indent=2)[:500] + "...")
        
        print("=" * 60 + "\n")
        
    except Exception as e:
        logger.exception("Pipeline failed with error")
        print(f"\n❌ Pipeline failed: {e}\n")
        raise
