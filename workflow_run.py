import io
import os
import sys
import json
import zipfile

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

# Artifact name
artifact_name = os.environ.get("ARTIFACT_NAME", "hello-world")

# Set headers to send with requests
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
}

# List all artifacts for the workflow run
resp = requests.get(workflow_run["artifacts_url"], headers=headers, params={"per_page": 100})
all_artifacts = resp.json()["artifacts"]

# If "Link" is present in the response headers, that means that the results are
# paginated and we need to loop through them to collect all the results.
# It is unlikely that we will have more than 100 artifact results for a single
# worflow ID however.
while ("Link" in resp.headers.keys()) and ('rel="next"' in res.headers["Link"]
):
    next_url = re.search(r'(?<=<)([\S]*)(?=>; rel="next")', resp.headers["Link"])
    resp = requests.get(next_url.group(0), headers=headers)
    all_artifacts.extend(resp.json()["artifacts"])

# Filter for the artifact with the name we want: 'hello-world'
indx, artifact_id = next(
    ((i, artifact["id"]) for i, artifact in enumerate(all_artifacts) if artifact["name"] == artifact_name),
    (None, None),
)

if artifact_id is None:
    print(f"No artifact found called '{artifact_name}' for workflow run: {run_id}")
    sys.exit()

# Download the artifact
resp = requests.get(all_artifacts[indx]["archive_download_url"], headers=headers, stream=True)

# Extract the zip archive
with zipfile.ZipFile(io.BytesIO(resp.content)) as zip_ref:
    zip_ref.extractall(os.getcwd())

# Read in file
with open(f"{artifact_name}.txt") as f:
    artifact_content = f.read().strip("\n")

print(artifact_content)
