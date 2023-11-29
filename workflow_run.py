import os
import json

import requests

api_url = "https://api.github.com"

# GITHUB_TOKEN = ${{ secrets.GITHUB_TOKEN }} in workflow file
token = os.environ.get("GITHUB_TOKEN", None)
if token is None:
    raise ValueError("GITHUB_TOKEN must be set!")

# WORKFLOW_RUN = ${{ github.event.workflow_run }} in workflow file
workflow_run = os.environ.get("WORKFLOW_RUN", None)
if workflow_run is None:
    raise ValueError("WORKFLOW_RUN must be set!")
workflow_run = json.loads(workflow_run)

# Set headers to send with requests
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
}

# List all artifacts for the workflow run
resp = requests.get(workflow_run["artifacts_url"], headers=headers, params={"per_page": 100})
all_artifacts = resp.json()["artifacts"]
print(all_artifacts)
