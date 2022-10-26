from airflow_google_cloud_run_plugin.cloud_run_v1.namespaces.job import (
    Job,
    JobSpec,
    ExecutionTemplateSpec,
)
from airflow_google_cloud_run_plugin.cloud_run_v1.namespaces.execution import Execution
from airflow_google_cloud_run_plugin.cloud_run_v1.types import (
    ObjectMeta,
    ExecutionSpec,
    TaskTemplateSpec,
    TaskSpec,
    Container,
    ResourceRequirements,
)

example_execution_spec = {
    "template": {
        "spec": {
            "containers": [
                {
                    "image": "debian",
                    "resources": {"limits": {"cpu": 1, "memory": "512Mi"}},
                }
            ]
        }
    }
}

example_metadata = {
    "name": "test-job",
    "namespace": "example-project",
    "annotations": {"run.googleapis.com/launch-stage": "BETA"},
}

example_job_config = {
    "metadata": example_metadata,
    "spec": {"template": {"spec": example_execution_spec}},
}

example_execution_config = {
    "metadata": example_metadata,
    "spec": example_execution_spec,
}


def test_minimal_job_construction():
    job = Job(
        metadata=ObjectMeta(
            name="test-job",
            namespace="example-project",
            annotations={"run.googleapis.com/launch-stage": "BETA"},
        ),
        spec=JobSpec(
            template=ExecutionTemplateSpec(
                spec=ExecutionSpec(
                    template=TaskTemplateSpec(
                        spec=TaskSpec(
                            containers=[
                                Container(
                                    image="debian",
                                    resources=ResourceRequirements(
                                        limits={"cpu": 1, "memory": "512Mi"}
                                    ),
                                )
                            ],
                        )
                    )
                )
            )
        ),
    )
    actual = job.to_dict()
    expected = example_job_config
    assert actual == expected


def test_minimal_job_construction_from_dict():
    d = example_job_config
    job = Job.from_dict(d)
    assert job.to_dict() == d


def test_minimal_execution_construction():
    execution = Execution(
        metadata=ObjectMeta(
            name="test-job",
            namespace="example-project",
            annotations={"run.googleapis.com/launch-stage": "BETA"},
        ),
        spec=ExecutionSpec(
            template=TaskTemplateSpec(
                spec=TaskSpec(
                    containers=[
                        Container(
                            image="debian",
                            resources=ResourceRequirements(
                                limits={"cpu": 1, "memory": "512Mi"}
                            ),
                        )
                    ],
                )
            )
        ),
    )
    actual = execution.to_dict()
    expected = example_execution_config
    assert actual == expected


def test_minimal_execution_construction_from_dict():
    d = example_execution_config
    execution = Execution.from_dict(d)
    assert execution.to_dict() == d
