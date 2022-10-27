import os
import unittest

import datetime as dt

from airflow import DAG
from airflow.models import TaskInstance
from airflow.utils.state import DagRunState
from airflow.utils.types import DagRunType

from airflow_google_cloud_run_plugin.operators.cloud_run import CloudRunJobOperator

TASK_ID = "example_task"
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DEFAULT_DATE = dt.datetime(2022, 1, 1).astimezone(dt.timezone.utc)


class TestCloudRunJobOperator(unittest.TestCase):
    def setUp(self) -> None:
        super(TestCloudRunJobOperator, self).setUp()
        self.dag = DAG(
            dag_id="test_dag",
            default_args={"owner": "unittest", "start_date": DEFAULT_DATE},
        )
        CloudRunJobOperator(
            task_id=TASK_ID,
            name="example-job",
            location="us-central1",
            project_id=GCP_PROJECT_ID,
            image="gcr.io/gcp-runtimes/ubuntu_18_0_4",
            command=["echo"],
            cpu="1000m",
            memory="512Mi",
            create_if_not_exists=True,
            delete_on_exit=True,
            dag=self.dag,
        )

    def test_full_lifecycle(self) -> None:
        dagrun = self.dag.create_dagrun(
            state=DagRunState.RUNNING,
            execution_date=DEFAULT_DATE,
            start_date=DEFAULT_DATE,
            run_type=DagRunType.MANUAL,
        )
        ti: TaskInstance = dagrun.get_task_instance(task_id=TASK_ID)
        ti.task = self.dag.get_task(task_id=TASK_ID)
        ti.task.execute(ti.get_template_context())
