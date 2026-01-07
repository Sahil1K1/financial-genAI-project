from src.ingestion.load_data import load_dataset
from src.llm.prompt_template import prompt
# from src.llm.final_app import generate_insights
from langchain_core.output_parsers import StrOutputParser

def pipeline():
    data = load_dataset()
    final_prompt = prompt.format_prompt(data[0].to_json())
    # llm = generate_insights()
    # chain = final_prompt | llm | StrOutputParser()
    # return chain
    return final_prompt
    # return data[0]

# a, b = pipeline()

print(pipeline())