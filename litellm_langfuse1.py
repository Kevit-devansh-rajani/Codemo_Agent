import os
from dotenv import load_dotenv
import litellm
from langfuse import get_client

load_dotenv()

os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY")
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY")
os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")

litellm.success_callback = ["langfuse"]
litellm.failure_callback = ["langfuse"]

langfuse = get_client()

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

    with langfuse.start_as_current_span(name=f"codegen_iteration_{iteration}") as span:
        span.update_trace(
            input=task_description,
            session_id="codegen-session",
            metadata={"model": MODEL}
        )

        try:
            response = litellm.completion(
                model=MODEL,
                messages=messages,
                metadata={
                    "langfuse_session_id": "codegen-session",
                    "iteration": iteration
                }
            )

            code = response['choices'][0]['message']['content']

            span.update_trace(output=code)
            span.score(name="iteration_success", value=1.0)

            return code

        except Exception as e:
            span.update_trace(level="ERROR", status_message=str(e))   
            raise   