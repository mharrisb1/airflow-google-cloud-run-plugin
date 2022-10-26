from five18 import PyProjectToml

from airflow_google_cloud_run_plugin import __version__


def test_version():
    toml = PyProjectToml()
    version = toml.tool_table.poetry.version
    assert __version__ == version
