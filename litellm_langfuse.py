import os
from dotenv import load_dotenv
import litellm
from langfuse import Langfuse

load_dotenv()

os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY")
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY")
os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")

litellm.success_callback = ["langfuse"]
litellm.failure_callback = ["langfuse"]

langfuse = Langfuse()

MODEL = "cohere/command-r-plus-08-2024"

def generate_code(task_description, feedback="", iteration=1):
    system_prompt = f"""
    You are an expert Python programmer. Your task is to generate ONLY the function definition(s) required to solve the user's problem.
    Your code should be robust and handle edge cases.
    Do NOT include:
    - Any test cases
    - print statements
    - Example calls
    - Comments related to testing or example outputs
    - Any extra statements without code

    Make sure the function handles all possible edge cases and is written in an optimal way.

    If there is feedback from previous failed tests, improve the function based on that feedback: {feedback}
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": task_description}
    ]

    trace = langfuse.trace(
        name=f"codegen_iteration_{iteration}",
        input=task_description,
        session_id="codegen-session",
        metadata={"model": MODEL}
    )

    try:
        response = litellm.completion(
            model=MODEL,
            messages=messages
        )

        code = response['choices'][0]['message']['content']

        trace.update(output=code)
        trace.score(name="iteration_success", value=1.0)

        return code

    except Exception as e:
        trace.error(name="completion_error", error=str(e))
        raise
