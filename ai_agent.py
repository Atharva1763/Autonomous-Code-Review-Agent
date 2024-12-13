from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import json
from dotenv import load_dotenv

load_dotenv()

# AI Integration Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Required if using OpenAI

def analyze_code(code_files,task_id):
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', openai_api_key = OPENAI_API_KEY)
    prompt = PromptTemplate(
        input_variables=["file_name", "code"],
        template="""
For the following Python code in file "{file_name}", analyze it and identify:

- Any style or formatting issues, including line numbers.
- Potential bugs or errors, including line numbers.
- Performance improvements, including line numbers.
- Best practices that are not followed, including line numbers.

Code:
{code}

Constraints on Output:

The analysis must be returned in JSON format.

'results' should be a dictionary.
Ensure all JSON keys are present and correctly named as shown.
All issue types must be one of the following: "style", "bug", "performance", "best_practice".

Only output valid JSON. DON'T output any other text or data.
"""
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    analysis_results = []
    result = []
    for file_info in code_files:
        file_name = file_info['file_name']
        code = file_info['code']
        result = chain.run(file_name=file_name, code=code,task_id=task_id)
        try:
            analysis = json.loads(result)
            analysis_results.append(analysis)
        except json.JSONDecodeError:
            pass
    return analysis_results