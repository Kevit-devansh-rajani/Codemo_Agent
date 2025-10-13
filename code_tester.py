import inspect
import textwrap

def run_tests(code):

    feedback = ""
    test_results = {"passed": False, "details": []}

    code = textwrap.dedent(code).strip()

    namespace = {}
    try:
        exec(code, namespace)
    except Exception as e:
        return {"passed": False}, f"Syntax/runtime error in code: {e}"

    # Get function name dynamically
    funcs = [obj for obj in namespace.values() if inspect.isfunction(obj)]
    if not funcs:
        return {"passed": False}, "No function found in the generated code."

    func = funcs[0]
    try:
        sig = inspect.signature(func)
    except ValueError:
        return {"passed": False}, "Could not determine function signature."
    
    # Generate a set of test cases
    test_cases = []
    param_values = []

    for param in sig.parameters.values():
        if param.annotation == int:
            param_values.append([1, 0, -5, 100])
        elif param.annotation == float:
            param_values.append([1.0, 0.0, -5.5, 100.1])
        elif param.annotation == str:
            param_values.append(["test", "", "long string example"])
        elif param.annotation == list:
            param_values.append([[], [1, 2], ["a", "b"]])
        elif param.annotation == bool:
            param_values.append([True, False])
        else:
            # Default for unknown types
            param_values.append([1, "test", [], None])

    # Create combinations of parameter values
    if param_values:
        import itertools
        for case_args in itertools.product(*param_values):
            # This can create a very large number of tests, let's limit it for now
            if len(test_cases) < 10:
                test_cases.append(case_args)

    if not test_cases and len(sig.parameters) == 0: # For functions with no arguments
        test_cases.append(())

    all_passed = True
    for i, args in enumerate(test_cases):
        try:
            # This is still a simplification, as we don't know the expected output
            # We are just checking for runtime errors for now.
            func(*args)
            test_results["details"].append({"case": i + 1, "args": args, "status": "passed"})
        except Exception as e:
            all_passed = False
            feedback += f"Test case {i+1} failed for input {args}.\nError: {e}\n\n"
            test_results["details"].append({"case": i + 1, "args": args, "status": "failed", "error": str(e)})

    test_results["passed"] = all_passed

    if not all_passed:
        feedback = "Some tests failed. Please fix the code based on the following failures:\n" + feedback

    return test_results, feedback
