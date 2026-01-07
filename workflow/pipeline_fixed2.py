from src.ingestion.load_data import load_dataset
from src.llm.prompt_template import prompt
# from src.llm.final_app import generate_insights
from langchain_core.output_parsers import StrOutputParser
from src.utils.logger import get_logger

logging = get_logger('pipeline_fixed')

def pipeline_function():
    dataset = load_dataset()[0]
    try:
        if dataset.empty or len(dataset) == 0:
            raise ValueError('No data found')
        dataset_json = dataset.to_json(orient='records', date_format='iso')
        final_prompt = prompt.format_prompt(data=dataset_json) # this is compatible with LLM chain and the input is expected in the same manner
        return final_prompt
    except FileNotFoundError as e:
        print(f'data file not found. Error {e}')
        raise
    except Exception as e:
        print(f'error in pipeline {e}')
        raise

def pipeline_function_str():
    """
    In order to see the prompt in str format and obesere what is the output actually will use prompt.format() this time"""
    dataset = load_dataset()
    try:
        if not dataset or len(dataset) == 0:
            raise ValueError('No data found')
        df = dataset[0]
        df = df.to_json(orient='records', date_format='iso')
        final_prompt = prompt.format(data=df)
        return final_prompt
    except FileNotFoundError as e:
        print(f'File not found {e}')
        raise

    except Exception as e:
        print(f'Error in code: {e}')
        raise



if __name__ == "__main__":
    # result = pipeline_function()
    # print(result)

    result2 = pipeline_function_str() # for debugging and checking if the output of the prompt is correct or not this is best
    # print(result2)

# print(pipeline_function())