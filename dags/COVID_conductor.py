from airflow import DAG
from airflow.contrib.sensors.gcs_sensors import GoogleCloudStorageObjectSensor
from airflow.contrib.operators.dataflow_operator import DataFlowTemplateOperator

GCP_CONN_ID = "GCP_CONN"

YESTERDAY = datetime.combine(
    datetime.today() - timedelta(1),
    datetime.min.time()
)

#Default Args
DEFAULT_ARGS = {
    'owner': 'service_account',
    'start_date': YESTERDAY,

}

dag = DAG(
    'COVID_conductor'
    default_args=DEFAULT_ARGS,
    schedule

)