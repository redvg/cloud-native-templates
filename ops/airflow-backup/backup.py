import datetime, time
import json
from airflow import models
from airflow.utils import dates
#from airflow.gcp.operators.datastore import DatastoreExportOperator
from airflow.contrib.operators.datastore_export_operator import DatastoreExportOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.gcp.operators.cloud_memorystore import CloudMemorystoreExportInstanceOperator
#from airflow.contrib.hooks.slack_webhook_hook import SlackWebhookHook
from airflow.utils.trigger_rule import TriggerRule


YESTERDAY = dates.days_ago(1)

DEFAULT_DAG_ARGS = {
    'start_date': YESTERDAY,
    #'email': models.Variable.get('admin_email'),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'project_id': "models.Variable.get('gcp_project_id')",
}

with models.DAG(dag_id='daily_backup_v1',
                description='Scheduled backup',
                schedule_interval=datetime.timedelta(days=1),
                catchup=False,
                default_args=DEFAULT_DAG_ARGS) as dag:
    
    gcs_bucket_name = models.Variable.get('gcs_backup_bucket')
    gcs_folder_name_firestore = models.Variable.get('gcs_folder_name_firestore')
    gcs_folder_name_memorystore = models.Variable.get('gcs_folder_name_memorystore')
    memorystore_instance_name = models.Variable.get('memorystore_instance_name')

    firestore_export_task = DatastoreExportOperator(
        task_id="firestore_export_task",
        bucket=gcs_bucket_name,
        namespace=str(int(time.time())),
        #project_id=GCP_PROJECT_ID,
        overwrite_existing=False,
    )

    memorystore_export_task = CloudMemorystoreExportInstanceOperator(
        task_id="memorystore_export_task",
        #location="europe-north1",
        instance=memorystore_instance_name,
        output_config={"gcs_destination": {"uri": gcs_folder_name_memorystore}},
        #project_id=GCP_PROJECT_ID,
    )

    memorystore_export_task >> firestore_export_task

    slack_success_notification_job = SimpleHttpOperator(
        task_id='slack_notify_success',
        http_conn_id='slack_foo',
        endpoint='T02542U5Y/BQP67NHUH/LKUwVyFK0El5ckExVWPCSwmC',
        method='POST',
        data=json.dumps({'text': 'Backup succeeded!'}),
        headers={"Content-Type": "application/json"},
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    slack_failure_notification_job = SimpleHttpOperator(
        task_id='slack_notify_failure',
        http_conn_id='slack_foo',
        endpoint='T02542U5Y/BQP67NHUH/LKUwVyFK0El5ckExVWPCSwmC',
        method='POST',
        data=json.dumps({'text': 'Backup failed'}),
        headers={"Content-Type": "application/json"},
        trigger_rule=TriggerRule.ALL_FAILED
    )

    firestore_export_task.set_downstream(slack_success_notification_job)
    firestore_export_task.set_downstream(slack_failure_notification_job)
