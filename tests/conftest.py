import os

# framework
import pytest

# to create fake data/env
from unittest import mock
from airflow.models import Variable, Connection, DagBag

# reusable setup code for tests, which can be used across multiple test functions
# fixture function which will be used inside a test fucntion
@pytest.fixture
def api_key():
    # changing the env variable AIRFLOW_VAR_API_KEY to a mock value for testing purpose
    with mock.patch.dict("os.environ", AIRFLOW_VAR_API_KEY="MOCK_KEY1234"):
        yield Variable.get(
            "API_KEY"
        )  # this internally checks os.environ["AIRFLOW_VAR_API_KEY"]


@pytest.fixture
def channel_handle():
    with mock.patch.dict("os.environ", AIRFLOW_VAR_CHANNEL_HANDLE="MRCHEESE"):
        yield Variable.get("CHANNEL_HANDLE")


@pytest.fixture
def mock_postgres_conn_vars():
    conn = Connection(
        login="mock_username",
        password="mock_password",
        host="mock_host",
        port=1234,
        schema="mock_db_name",
    )
    conn_uri = conn.get_uri()
    with mock.patch.dict("os.environ", AIRFLOW_CONN_POSTGRES_DB_YT_ELT=conn_uri):
        yield Connection.get_connection_from_secrets("POSTGRES_DB_YT_ELT")

#dagbag -> airflow container which holds all the dags
@pytest.fixture()
def dagbag():
    yield DagBag()#object
