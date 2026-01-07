from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template = """
You are a financial analyst. Analyze the following company metrics:

{data}

Generate:
1. Key financial risks
2. Investment opportunities
3. Recommendations for the CFO
4. Summary in bullet points

Output must be structured JSON.
""", input_variables=['data'], validate_template=True)

# print(prompt)