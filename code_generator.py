import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_code(task_description, feedback=""):

    system_prompt = f"""
    You are an expert Python programmer. Your task is to generate ONLY the function definition(s) required to solve the user’s problem.
    Do NOT include:
    - Any test cases
    - print statements
    - Example calls
    - Comments related to testing or example outputs

    Make sure the function handles all possible edge cases and is written in an optimal way.

    If there is feedback from previous failed tests, improve the function based on that feedback: {feedback}
    """

    if feedback:
        system_prompt += f"\nPrevious feedback from failed tests: {feedback}\nPlease improve the code accordingly."

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task_description}
        ],
        temperature=0
    )

    code = response.choices[0].message.content.strip()
    return code
