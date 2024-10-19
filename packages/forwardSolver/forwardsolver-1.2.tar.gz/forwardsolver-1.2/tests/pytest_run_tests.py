import os

if __name__ == "__main__":

    # pytest_args = ["-v", "-s"]
    # pytest_args.extend(["forwardSolver/tests/utils",
    #                     "--report-log=test-report-forwardsolver-tests.log",])
    # os.system(
    #         "python -m coverage run --source=src -m pytest -n auto --cov "
    #         + " ".join(pytest_args)
    #     )

    # Run all tests
    os.system(
        "python -m pytest -n auto . -v -s --cov=src "
        "--report-log=test-report-all-tests.log "
        "--cov"
    )
    # pytest_args.extend(
    #     [
    #         "--report-log=test-report-all-tests.log",
    #     ]
    # )

    # os.system(
    #     "python -m coverage run --source=src -m pytest -n auto "
    #     + " ".join(pytest_args)
    # )
