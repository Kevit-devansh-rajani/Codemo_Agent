import streamlit as st
from code_generator import generate_code
from code_tester import run_tests

st.set_page_config(page_title="Codemo", layout="centered")
st.title("Codemo - AI Code Generation")

task_description = st.text_area("Enter your programming task:", height=150)

max_iterations = st.sidebar.number_input("Max Iterations", min_value=1, max_value=10, value=3)

if st.button("Generate Code"):
    if not task_description.strip():
        st.warning("Please enter a programming task!")
    else:
        feedback = ""
        for iteration in range(1, max_iterations + 1):
            st.info(f"Iteration {iteration}...")

            try:
                code = generate_code(task_description, feedback)
            except Exception as e:
                st.error(f"Error generating code: {e}")
                break

            st.code(code, language="python")

            test_results, feedback = run_tests(code)

            if test_results["passed"]:
                st.success(f"All tests passed in iteration {iteration}!")
                break
            else:
                st.warning(f"Some tests failed in iteration {iteration}. Feedback sent to AI for improvement.")
                st.warning(f"Feedback:\n{feedback}")

        else:
            st.error(f"Maximum iterations reached. Some tests are still failing. Last feedback:\n{feedback}")
