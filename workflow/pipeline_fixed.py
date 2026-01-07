from src.ingestion.load_data import load_dataset
from src.llm.prompt_template import prompt
# from src.llm.final_app import generate_insights
from langchain_core.output_parsers import StrOutputParser


def pipeline():
    """
    Pipeline to process financial data and generate LLM prompts.
    
    Returns:
        PromptValue: Formatted prompt ready for LLM chain
    """
    try:
        # Load the dataset
        data = load_dataset()
        
        # Validate data exists
        if not data or len(data) == 0:
            raise ValueError("No data loaded. Please check if data files exist in data/raw directory")
        
        # Get the first dataframe
        df = data[0]
        
        # Convert DataFrame to a more digestible format for LLM
        # Option 1: Convert to JSON string (current approach)
        data_json = df.to_json(orient='records', date_format='iso')
        
        # Option 2: Get summary statistics instead of full data (better for large datasets)
        # data_summary = {
        #     "shape": df.shape,
        #     "columns": df.columns.tolist(),
        #     "summary_stats": df.describe().to_dict(),
        #     "sample_records": df.head(10).to_dict('records'),
        #     "null_counts": df.isnull().sum().to_dict()
        # }
        # import json
        # data_json = json.dumps(data_summary, indent=2)
        
        # Format the prompt with data
        # Using format_prompt() which returns PromptValue (compatible with LangChain chains)
        final_prompt = prompt.format_prompt(data=data_json)
        
        # When you uncomment the LLM code, the chain will work like this:
        # llm = generate_insights()
        # chain = final_prompt | llm | StrOutputParser()
        # result = chain.invoke({})
        # return result
        
        return final_prompt
        
    except FileNotFoundError as e:
        print(f"Error: Data file not found - {e}")
        raise
    except Exception as e:
        print(f"Error in pipeline: {e}")
        raise


def pipeline_with_string_output():
    """
    Alternative pipeline that returns formatted string instead of PromptValue.
    Use this if you want to see the actual prompt text.
    
    Returns:
        str: Formatted prompt as string
    """
    try:
        data = load_dataset()
        
        if not data or len(data) == 0:
            raise ValueError("No data loaded")
        
        df = data[0]
        data_json = df.to_json(orient='records', date_format='iso')
        
        # Using format() which returns a string
        final_prompt_str = prompt.format(data=data_json)
        
        return final_prompt_str
        
    except Exception as e:
        print(f"Error in pipeline: {e}")
        raise


if __name__ == "__main__":
    # Test the pipeline
    print("=" * 80)
    print("Testing pipeline():")
    print("=" * 80)
    result = pipeline()
    print(f"Type: {type(result)}")
    print(f"Content:\n{result}")
    
    print("\n" + "=" * 80)
    print("Testing pipeline_with_string_output():")
    print("=" * 80)
    result_str = pipeline_with_string_output()
    print(f"Type: {type(result_str)}")
    # Print first 1000 characters to avoid overwhelming output
    print(f"Content (first 1000 chars):\n{result_str[:1000]}...")
