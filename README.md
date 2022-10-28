# airflow-google-cloud-run-plugin

[![PyPI version](https://badge.fury.io/py/airflow-google-cloud-run-plugin.svg)](https://badge.fury.io/py/airflow-google-cloud-run-plugin)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/airflow-google-cloud-run-plugin)](https://pypi.org/project/airflow-google-cloud-run-plugin/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/airflow-google-cloud-run-plugin.svg)](https://pypi.org/project/airflow-google-cloud-run-plugin/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Airflow plugin for
orchestrating [Google Cloud Run jobs](https://cloud.google.com/run/docs/overview/what-is-cloud-run#jobs).

## Features

1. Easier to use alternative
   to [`KubernetesPodOperator`](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html)
2. Securely use sensitive data stored in Google Cloud Secrets Manager
3. Create tasks with isolated dependencies
4. Enables polyglot workflows

## Resources

### Core Operators

1. `CloudRunJobOperator`

### CRUD-Based Operators

1. `CloudRunCreateJobOperator`
2. `CloudRunGetJobOperator` 🔜
3. `CloudRunUpdateJobOperator` 🔜
4. `CloudRunDeleteJobOperator`
5. `CloudRunListJobsOperator` 🔜

### Hooks

1. `CloudRunJobHook`

### Sensors

2. `CloudRunJobExecutionSensor` 🔜

## Usage

### Simple Job Lifecycle

```python
from airflow import DAG

from airflow_google_cloud_run_plugin.operators.cloud_run import CloudRunJobOperator

with DAG(dag_id="example_dag") as dag:
  job = CloudRunJobOperator(
    task_id="example-job",
    name="example-job",
    location="us-central1",
    project_id="example-project",
    image="gcr.io/gcp-runtimes/ubuntu_18_0_4",
    command=["echo"],
    cpu="1000m",
    memory="512Mi",
    create_if_not_exists=True,
    delete_on_exit=True
  )
```

### CRUD Job Lifecycle

```python
from airflow import DAG

from airflow_google_cloud_run_plugin.operators.cloud_run import (
  CloudRunJobOperator,
  CloudRunCreateJobOperator,
  CloudRunDeleteJobOperator,
)

with DAG(dag_id="example_dag") as dag:
  create_job = CloudRunCreateJobOperator(
    task_id="create",
    name="example-job",
    location="us-central1",
    project_id="example-project",
    image="gcr.io/gcp-runtimes/ubuntu_18_0_4",
    command=["echo"],
    cpu="1000m",
    memory="512Mi"
  )

  run_job = CloudRunJobOperator(
    task_id="run",
    name="example-job",
    location="us-central1",
    project_id="example-project"
  )

  delete_job = CloudRunDeleteJobOperator(
    task_id="delete",
    name="example-job",
    location="us-central1",
    project_id="example-project"
  )

  create_job >> run_job >> delete_job
```

### Using Environment Variables

```python
from airflow import DAG

from airflow_google_cloud_run_plugin.operators.cloud_run import CloudRunJobOperator

# Simple environment variable
FOO = {
  "name": "FOO",
  "value": "not_so_secret_value_123"
}

# Environment variable from Secret Manager
BAR = {
  "name": "BAR",
  "valueFrom": {
    "secretKeyRef": {
      "name": "super_secret_password",
      "key": "1"  # or "latest" for latest secret version
    }
  }
}

with DAG(dag_id="example_dag") as dag:
  job = CloudRunJobOperator(
    task_id="example-job",
    name="example-job",
    location="us-central1",
    project_id="example-project",
    image="gcr.io/gcp-runtimes/ubuntu_18_0_4",
    command=["echo"],
    args=["$FOO", "$BAR"],
    env_vars=[FOO, BAR],
    cpu="1000m",
    memory="512Mi",
    create_if_not_exists=True,
    delete_on_exit=True
  )
```

## Improvement Suggestions

- Add support for Cloud Run services
- Nicer user experience for defining args and commands
- Use approach from other GCP operators once this issue is resolved https://github.com/googleapis/python-run/issues/64
- Add operators for all CRUD operations
- Add run sensor (see [link](https://github.com/apache/airflow/tree/main/airflow/providers/google/cloud/sensors))
- Enable volume mounts (see [TaskSpec](https://cloud.google.com/run/docs/reference/rest/v1/TaskSpec))
- Allow user to configure resource requirements `requests` (
  see [ResourceRequirements](https://cloud.google.com/run/docs/reference/rest/v1/Container#resourcerequirements))
- Add remaining container options (see [Container](https://cloud.google.com/run/docs/reference/rest/v1/Container))
- Allow non-default credentials and for user to specify service account (
  see [link](https://google-auth.readthedocs.io/en/latest/user-guide.html#service-account-private-key-files))
- Allow failure threshold. If more than one task is specified, user should be allowed to specify number of failures
  allowed
- Add custom links for log URIs
- Add wrapper class for easier environment variable definition. Similar to `Secret` from Kubernetes provider (
  see [link](https://github.com/apache/airflow/blob/main/airflow/kubernetes/secret.py))
- Add slight time padding between job create and run
- Add ability to choose to replace the job with new config values if values have changed
