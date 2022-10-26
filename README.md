# airflow-google-cloud-run-plugin

Airflow plugin for
orchestrating [Google Cloud Run jobs](https://cloud.google.com/run/docs/overview/what-is-cloud-run#jobs).

## Features

1. Easier to use alternative
   to [`KubernetesPodOperator`](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html)
2. Securely use sensitive data stored in Google Cloud Secrets Manager
3. Create tasks with isolated dependencies
4. Enables polyglot workflows

## Resources

### Operators

1. `CloudRunJobCreateOperator`
2. `CloudRunJobDeleteOperator`
3. `CloudRunJobRunOperator`

### Hooks

1. `CloudRunJobHook`

## Usage

### Basic Usage

```python
from airflow import DAG

from airflow_google_cloud_run_plugin.operators.cloud_run import (
    CloudRunJobCreateOperator,
    CloudRunJobDeleteOperator,
    CloudRunJobRunOperator,
)

with DAG(dag_id="example_dag") as dag:
    create_job = CloudRunJobCreateOperator(
        task_id="create",
        name="example-job",
        location="us-central1",
        project_id="example-project",
        image="gcr.io/gcp-runtimes/ubuntu_18_0_4",
        command=["echo"],
        cpu="1000m",
        memory="512Mi"
    )

    run_job = CloudRunJobRunOperator(
        task_id="run",
        name="example-job",
        location="us-central1",
        project_id="example-project"
    )

    delete_job = CloudRunJobDeleteOperator(
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

from airflow_google_cloud_run_plugin.operators.cloud_run import (
    CloudRunJobCreateOperator,
    CloudRunJobDeleteOperator,
    CloudRunJobRunOperator,
)

# Simple environment variable
env1 = {
    "name": "FOO",
    "value": "not_so_secret_value_123"
}

# Environment variable from Secret Manager
env2 = {
    "name": "BAR",
    "valueFrom": {
        "secretKeyRef": {
            "name": "super_secret_password",
            "key": "1"  # or "latest" for latest secret version
        }
    }
}

with DAG(dag_id="example_dag_with_secrets") as dag:
    create_job = CloudRunJobCreateOperator(
        task_id="create",
        name="example-job",
        location="us-central1",
        project_id="example-project",
        image="gcr.io/gcp-runtimes/ubuntu_18_0_4",
        command=["echo"],
        env_vars=[env1, env2],
        cpu="1000m",
        memory="512Mi"
    )

    run_job = CloudRunJobRunOperator(
        task_id="run",
        name="example-job",
        location="us-central1",
        project_id="example-project"
    )

    delete_job = CloudRunJobDeleteOperator(
        task_id="delete",
        name="example-job",
        location="us-central1",
        project_id="example-project"
    )

    create_job >> run_job >> delete_job
```

## Improvement Suggestions

- Use approach from other GCP operators once this issue is resolved https://github.com/googleapis/python-run/issues/64
- Add operators for all CRUD operations
- Add run sensor (ref: [link](https://github.com/apache/airflow/tree/main/airflow/providers/google/cloud/sensors))
- Enable volume mounts (see [TaskSpec](https://cloud.google.com/run/docs/reference/rest/v1/TaskSpec))
- Allow user to configure resource requirements `requests` (see [ResourceRequirements](https://cloud.google.com/run/docs/reference/rest/v1/Container#resourcerequirements))
- Add remaining container options (see [Container](https://cloud.google.com/run/docs/reference/rest/v1/Container))
- Provide a job generator helper similar to Dataproc cluster config generator (see [link](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/dataproc.html#generating-cluster-config))
- Allow non-default credentials and for user to specify service account (see [link](https://google-auth.readthedocs.io/en/latest/user-guide.html#service-account-private-key-files))
- Allow failure threshold. If more than one task is specified, user should be allowed to specify number of failures allowed
- Add custom links for log URIs
- Add wrapper class for easier environment variable definition. Similar to `Secret` from Kubernetes provider (see [link](https://github.com/apache/airflow/blob/main/airflow/kubernetes/secret.py))
