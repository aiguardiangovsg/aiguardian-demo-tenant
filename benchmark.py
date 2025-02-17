#!/usr/bin/env python
import datetime
import json
import os
import re
import sys
import time
from urllib.parse import urljoin

import requests  # type: ignore


def log(message):
    print(f"{datetime.datetime.now(datetime.UTC)} | {message}")


def create_headers(api_key, type="application/json"):
    return {"Content-Type": type, "X-API-Key": api_key}


def make_request(method, url, headers, data=None, params=None, type="json"):
    try:
        log(f"{method} request to {url}")
        if method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "GET":
            response = requests.get(url, params=params, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()

        if type != "json":
            return response.text

        response_json = response.json()

        log(f"Status code: {response.status_code}")
        if os.environ.get("DEBUG") == "TRUE":
            log("Response JSON:")
            log(json.dumps(response_json, indent=10))

        return response_json
    except requests.exceptions.RequestException as e:
        log(f"An error occurred while making the request: {e}")  # noqa: E501
        sys.exit(1)


def start_litmus_test(base_url, data, headers):
    url = urljoin(base_url, "/api/testRuns")
    response_json = make_request("POST", url, headers, data=data)

    log(f"Response JSON: {response_json}")

    run_id = response_json.get("id")

    log(f"Run ID: {run_id}")

    if not run_id:
        log("Error: 'id' field not found in the response")
        sys.exit(1)

    return run_id


def check_litmus_test_status(base_url, run_id, headers):
    url = urljoin(base_url, f"/api/testRuns/{run_id}")

    log("Checking status")
    response_json = make_request("GET", url, headers)

    return response_json


def get_litmus_test_results(base_url, run_id, headers, api_key):
    url = urljoin(base_url, f"/api/testResults/{run_id}?format=json")
    response_json = make_request("GET", url, headers)
    url = urljoin(base_url, f"/api/testResults/{run_id}?format=html")
    response_html = make_request("GET", url, headers, type="html")

    dirname = "litmus_test_results"
    os.makedirs(dirname, exist_ok=True)

    # Save the results to a file with the date
    filename = f"litmus_test_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"  # noqa: E501

    json_filename = os.path.join(dirname, f"{filename}.json")
    with open(json_filename, "w") as f:
        json.dump(response_json, f, indent=2)

    html_filename = os.path.join(dirname, f"{filename}.html")
    with open(html_filename, "w") as f:
        f.write(response_html)

    log(f"Test results saved to {json_filename} and {html_filename}")

    return response_json


def is_valid_url(url):
    url_pattern = re.compile(
        r"^https?://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
        r"localhost|"
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)?$",
        re.IGNORECASE,
    )
    return url_pattern.match(url) is not None


def validate_and_get_args():
    if len(sys.argv) < 7:
        log("Error: Insufficient arguments.")
        log(
            "Usage: python benchmark.py <base_url> <run_name> <endpoint> <test_suites> <num_of_prompts> <api_key> [check_interval] [timeout]"  # noqa: E501
        )
        log(
            "Example: python benchmark.py https://api.example.com 'My First Test Run' 'my-endpoint-1' 'aiguardian-baseline-tests' 5 your_api_key_here"  # noqa: E501
        )
        log(
            "`check_interval` and `timeout` are optional, default values are 10 and 1800, unit is second."  # noqa: E501
        )
        sys.exit(1)

    base_url, run_name, endpoint, input_value, num_of_prompts, api_key = (
        sys.argv[1:7]
    )

    interval = int(sys.argv[7]) if len(sys.argv) > 7 else 10
    timeout = int(sys.argv[8]) if len(sys.argv) > 8 else 1800

    base_url = sys.argv[1]

    if not is_valid_url(base_url):
        log(
            f"Error: Invalid base URL: {base_url}. Please provide a valid URL."
        )
        log("Example: https://api.example.com")
        sys.exit(1)

    return (
        base_url,
        run_name,
        endpoint,
        input_value,
        num_of_prompts,
        api_key,
        interval,
        timeout,
    )


# Main steps
# 1. Validate and get the arguments
# 2. POST request to start the Litmus test
# 3. Check the status of the Litmus test with a GET request until it completes
# 4. Fetch the results if the benchmark completed successfully
# 5. Save the results to a JSON file
def main():
    start_time = time.monotonic()
    (
        base_url,
        run_name,
        endpoint,
        input_value,
        num_of_prompts,
        api_key,
        interval,
        timeout,
    ) = validate_and_get_args()

    headers = create_headers(api_key)

    data = {
        "run_name": run_name,
        "endpoint": endpoint,
        "test_suites": [input_value],
        "num_of_prompts": num_of_prompts,
    }

    log(
        f"Starting Litmus Test with the following data: {json.dumps(data, indent=2)}"  # noqa: E501
    )
    run_id = start_litmus_test(base_url, data, headers)

    max_attempts = int(timeout / interval)
    delay_seconds = interval
    final_status = None

    log(f"Checking status in {delay_seconds} seconds...")
    time.sleep(delay_seconds)
    max_attempts -= 1

    for attempt in range(max_attempts):
        status_response = check_litmus_test_status(base_url, run_id, headers)

        log(json.dumps(status_response, indent=2))

        LITMUS_TEST_STATUS = {
            "NEW": "NEW",
            "QUEUED": "QUEUED",
            "RUNNING": "RUNNING",
            "COMPLETED": "COMPLETED",
            "ABORTED": "ABORTED",
            "ERRORED": "ERRORED",
            "SKIPPED": "SKIPPED",
        }

        if "status" in status_response:
            final_status = status_response["status"]

            if status_response["status"] in [
                LITMUS_TEST_STATUS["COMPLETED"],
                LITMUS_TEST_STATUS["ABORTED"],
                LITMUS_TEST_STATUS["ERRORED"],
                LITMUS_TEST_STATUS["SKIPPED"],
            ]:
                # Break the loop if the benchmark has completed
                break

        if attempt < max_attempts - 1:
            log(
                f"Test is still running with status: {status_response['status']}. Checking again in {delay_seconds} seconds..."  # noqa: E501
            )
            time.sleep(delay_seconds)
        else:
            log(
                f"Error: Timeout ({timeout}) reached. Test did not complete in time."  # noqa: E501
            )
            sys.exit(1)

    log(f"Test was completed, final status: {final_status}")

    # Fetch the results if the benchmark completed successfully
    log("Fetching results of the test")
    get_litmus_test_results(base_url, run_id, headers, api_key)

    log(
        f"Test completed successfully in {time.monotonic() - start_time:.0f}s. The result can be viewed online at {base_url}/test-runs/{run_id}"  # noqa: E501
    )


if __name__ == "__main__":
    main()
