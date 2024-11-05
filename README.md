# AIGuardian Litmus Demo Tenant

A demo project to showcase Litmus test integration using GitHub Actions

# Litmus Test Integration Demo

This repository demonstrates an integration of Litmus tests into a GitHub Actions CI/CD pipeline. It’s designed to provide a practical example of how automated safety checks can be implemented for generative AI applications, ensuring they meet defined safety criteria before deployment. The setup is suitable for projects developing or deploying generative AI applications and focuses on mitigating risks by identifying issues such as bias, unfair treatment, and adversarial vulnerabilities.

## Overview

Ensuring the safety, fairness, and robustness of AI applications is critical. This project integrates a set of AI safety checks into a continuous integration (CI) pipeline using GitHub Actions. By automating these tests, we aim to catch potential safety issues early in the development process, making it easier for teams to maintain high standards of AI safety.

## Features

- **Automated AI Safety Tests**: Run safety tests on every code push, ensuring that the model meets predefined safety criteria.
- **GitHub Actions Workflow**: Easily integrate the workflow into your GitHub repository.

## Getting Started

### 1. Set Up GitHub Actions Workflow

The project includes a GitHub Actions workflow file (`.github/workflows/litmus-test.yml`). This file configures the CI pipeline to run safety checks automatically on each push and pull request.

### 2. Customize Safety Tests

- Modify `on` setting to customize triggers specific to your application.
- Update the parameters of the `Run Litmus Tests` step using appropriate environment variables to fine-tune the test criteria.
```yaml
      - name: Run Litmus Tests
        uses: dsaidgovsg/aiguardian-litmus-test@<version>
        with:
          base_url: ${{ vars.LITMUS_BASE_URL }}
          run_name: ${{ github.run_id }}-${{ github.run_attempt }}
          endpoint: ${{ vars.ENDPOINT }}
          cookbook: ${{ vars.COOKBOOK }}
          num_of_prompts: ${{ vars.NUM_OF_PROMPTS || '1'}}
          api_key: ${{ secrets.LITMUS_KEY }}
          debug_mode: ${{ vars.DEBUG_MODE || 'false' }}
```

### 3. Push Changes to GitHub

After setting up the workflow and configuring the tests, push your changes to GitHub. The safety tests will automatically run, with results visible under the **Actions** tab in your repository.

## Contributing

If you have ideas to improve the safety checks, feel free to submit a pull request. Contributions are welcome!

---

By automating Litmus safety checks with GitHub Actions, this aims to help developers ensure that their AI applications are safe, fair, and robust. This integration can be a critical tool in a responsible AI development pipeline.
