# AIGuardian Litmus Demo Tenant

A demo project to showcase Litmus test integration using GitHub Actions

# Litmus Test Integration Demo

This repository demonstrates an integration of Litmus tests into a GitHub Actions CI/CD pipeline. It's designed to provide a practical example of how automated safety checks can be implemented for generative AI applications, ensuring they meet defined safety criteria before deployment. The setup is suitable for projects developing or deploying generative AI applications and focuses on mitigating risks by identifying issues such as bias, unfair treatment, and adversarial vulnerabilities.

## Overview

Ensuring the safety, fairness, and robustness of AI applications is critical. This project integrates a set of AI safety checks into a continuous integration (CI) pipeline using GitHub Actions. By automating these tests, we aim to catch potential safety issues early in the development process, making it easier for teams to maintain high standards of AI safety.

## Features

- **Automated AI Safety Tests**: Run safety tests on every code push, ensuring that the model meets predefined safety criteria.
- **GitHub Actions Workflow**: Easily integrate the workflow into your GitHub repository.
- **Customizable Test Parameters**: Configure test suites, endpoints, number of prompts, and timeouts through workflow dispatch inputs or repository variables.

## Getting Started

### 1. Set Up GitHub Actions Workflow

The project includes a GitHub Actions workflow file (`.github/workflows/litmus-test.yml`). This file configures the CI pipeline to run safety checks automatically on each push and pull request.

### 2. Configure Repository Variables and Secrets

Set up the following repository variables and secrets in your GitHub repository:

**Variables:**
- `LITMUS_BASE_URL`: The base URL of your Litmus API including version (e.g.: "https://litmus-api-base-url/api/v1")
- `ENDPOINT`: The endpoint to test (e.g.: "your-endpoint-name")
- `TEST_SUITES`: The test suites to run (e.g.: "aiguardian-baseline-tests")
- `NUM_OF_PROMPTS`: Number of prompts to generate (e.g.: "5")
- `INTERVAL`: Time interval in seconds between status checks (default: "10")
- `TIMEOUT`: Maximum time in seconds to wait for test completion (default: "1800")

**Secrets:**
- `LITMUS_API_KEY`: Your Litmus API key

### 3. Customize the Workflow

You can run the workflow manually through the GitHub Actions interface and override the default parameters:

```yaml
  workflow_dispatch:
    inputs:
      endpoint:
        description: "Endpoint Name"
        required: false
      test_suites:
        description: "Test Suites (comma-separated)"
        default: "aiguardian-baseline-tests"
        required: false
      num_of_prompts:
        description: "Number of Prompts"
        default: "5"
        required: false
      timeout:
        description: "Timeout (in seconds)"
        default: "600"
        required: false
```

### 4. Run Tests Locally (Optional)

You can also run the benchmark script locally:

```bash
python benchmark.py \
  "https://litmus-api-base-url/api/v1" \
  "test-run-name" \
  "your-endpoint-name" \
  "aiguardian-baseline-tests" \
  5 \
  "your-api-key" \
  10 \
  180
```

Arguments:
1. Base URL - The Litmus API base URL
2. Run Name - Name for the test run
3. Endpoint - The endpoint to be tested
4. Test Suites - The test suite to run
5. Number of Prompts - Number of prompts to generate
6. API Key - Your Litmus API key
7. Check Interval (optional) - Time between status checks in seconds
8. Timeout (optional) - Maximum time to wait for test completion in seconds

### 5. View and Analyze Results

After the workflow completes, test results will be available as GitHub workflow artifacts. The results are saved in both JSON and HTML formats in the `litmus_test_results` directory.

You can also view online results at `https://{LITMUS_BASE_DOMAIN}/test-runs/{run_id}` as indicated in the workflow output where `LITMUS_BASE_DOMAIN` is the domain name of `LITMUS_BASE_URL`.

## Contributing

If you have ideas to improve the safety checks, feel free to submit a pull request. Contributions are welcome!

---

By automating Litmus safety checks with GitHub Actions, this aims to help developers ensure that their AI applications are safe, fair, and robust. This integration can be a critical tool in a responsible AI development pipeline.
