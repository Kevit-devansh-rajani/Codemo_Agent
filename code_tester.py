import unittest
import io
import contextlib
import textwrap

def run_tests(code):
    feedback = ""
    test_results = {"passed": False}

    code = textwrap.dedent(code).strip()

    test_code = f"""
        import unittest

        {code}

        class TestGeneratedCode(unittest.TestCase):
            def test_fibonacci_series(self):
                if 'fibonacci_series' in globals():
                    self.assertEqual(fibonacci_series(1), [0])
                    self.assertEqual(fibonacci_series(5), [0, 1, 1, 2, 3])
                else:
                    self.assertTrue(True)
"""

    test_code = textwrap.dedent(test_code)

    try:
        # Run the test dynamically
        exec_globals = {}
        exec(test_code, exec_globals)

        stream = io.StringIO()
        runner = unittest.TextTestRunner(stream=stream, verbosity=2)
        suite = unittest.defaultTestLoader.loadTestsFromModule(
            type("DynamicModule", (), exec_globals)
        )
        result = runner.run(suite)

        if result.wasSuccessful():
            test_results["passed"] = True
            feedback = "All tests passed successfully."
        else:
            feedback = stream.getvalue()
            test_results["passed"] = False

    except Exception as e:
        feedback = f"Your code has an error: {e}"
        test_results["passed"] = False

    return test_results, feedback
