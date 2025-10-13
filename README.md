# Codemo 🤖

Codemo is an AI-powered code generation tool that iteratively writes and refines Python code based on your requirements. It uses a powerful language model to generate code and then tests it, providing feedback to the AI for improvements until the code is correct.

## ✨ Features

*   **AI Code Generation:** Describe your programming task in plain English, and Codemo will generate the Python code for you.
*   **Iterative Self-Correction:** Codemo automatically tests the generated code. If there are errors, it sends the feedback back to the AI to fix the code. This process repeats for a configurable number of iterations.
*   **Interactive Web UI:** A simple and intuitive web interface built with Streamlit to interact with the code generation process.
*   **Observability:** Integrated with Langfuse for detailed tracing and observability of the code generation and testing process.

## 🚀 How it works

1.  **Describe your task:** You enter a description of the programming task you want to accomplish (e.g., "write a function that takes a list of integers and returns the sum of all even numbers").
2.  **Code Generation:** Codemo sends your request to a large language model (Cohere's Command R+) to generate the Python function.
3.  **Automated Testing:** The generated code is immediately tested with a set of dynamically generated test cases.
4.  **Feedback Loop:** If the tests fail, the error messages and feedback are sent back to the language model. The model then attempts to fix the code based on this feedback.
5.  **Success!** The process continues until the code passes all tests, or the maximum number of iterations is reached.

## 🛠️ Tech Stack

*   **Backend:** Python
*   **Frontend:** Streamlit
*   **LLM Interaction:** LiteLLM
*   **LLM Providers:** Cohere (Command R+), OpenAI (GPT-3.5 Turbo), and others supported by LiteLLM.
*   **Observability:** Langfuse

### Using a Different LLM (e.g., OpenAI)

Thanks to LiteLLM, you can easily switch to other language models like OpenAI's GPT-3.5 Turbo.

1.  **Update the model in `litellm_langfuse.py`:**
    Change the `MODEL` constant to the desired model name:
    ```python
    # Before
    MODEL = "cohere/command-r-plus-08-2024"

    # After
    MODEL = "gpt-3.5-turbo"
    ```

2.  **Set the API key:**
    Add the API key for the new model to your `.env` file:
    ```
    OPENAI_API_KEY="your-openai-api-key"
    ```

## 📦 Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the root of the project and add your API keys:
    ```
    LANGFUSE_PUBLIC_KEY="your-langfuse-public-key"
    LANGFUSE_SECRET_KEY="your-langfuse-secret-key"
    COHERE_API_KEY="your-cohere-api-key"
    ```

## ▶️ How to run

Once you have installed the dependencies and set up your environment variables, you can run the application with:

```bash
streamlit run app.py
```

This will open the Codemo web interface in your browser.

## 📂 Project Structure

```
.
├── app.py                  # The main Streamlit application
├── litellm_langfuse.py     # Handles code generation and Langfuse tracing
├── code_tester.py          # Tests the generated Python code
├── requirements.txt        # Project dependencies
├── README.md               # This file
└── ...
```
