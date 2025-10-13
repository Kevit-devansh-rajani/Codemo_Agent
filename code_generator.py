import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_code(task_description, feedback=""):

    system_prompt = f"""
    You are an expert Python programmer. 
    Generate ONLY the function definition(s) required to solve the user's problem.

    Important Rules:
    - Do NOT include any markdown formatting (no ```python or ```).
    - Do NOT include test cases or example calls.
    - Do NOT add print statements or explanations.
    - Output only clean, executable Python function definitions.
    - Give Proper Identation for python code

    If there is feedback from previous failed tests, improve the function based on that feedback: {feedback}
    """


    if feedback:
        system_prompt += f"\nPrevious feedback from failed tests: {feedback}\nPlease improve the code accordingly."

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task_description}
        ],
        temperature=0
    )

    code = response.choices[0].message.content.strip()
    return code
