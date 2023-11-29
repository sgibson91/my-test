import os
import json

workflow_run = os.environ.get("WORKFLOW_RUN", None)

if workflow_run is None:
    raise ValueError("WORKFLOW_RUN must be set!")

workflow_run = json.loads(workflow_run)
print(workflow_run)
