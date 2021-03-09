import datetime
import json
from airflow import models
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.python_operator import PythonOperator
from operators.gcs_list import GoogleCloudStorageListOperator
from operators.gcs_to_gcs import GoogleCloudStorageToGoogleCloudStorageOperator


BEFORE = datetime.datetime(2020, 1, 1)

DEFAULT_DAG_ARGS = {
    'depends_on_past': False,
    'email': [models.Variable.get('author_email')],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=20),
    'project_id': models.Variable.get('gcp_project_id')
}

ENV = 'staging'

with models.DAG(dag_id='SyncBlobs_v1_{env}'.format(env=ENV),
                description='New blobs check & import DAG triggered periodically',
                schedule_interval=datetime.timedelta(days=1),
                start_date=BEFORE,
                catchup=False,
                default_args=DEFAULT_DAG_ARGS) as dag:
    
    gcs_bucket_blobs_source = models.Variable.get('gcs_bucket_blobs_source{env}'.format(env=ENV))
    
    gcs_bucket_blobs_target = models.Variable.get('gcs_bucket_blobs_target{env}'.format(env=ENV))

    slack_start_notification_job = SimpleHttpOperator(
        task_id='slack_notify_start',
        http_conn_id='slack_foo',
        endpoint='',
        method='POST',
        data=json.dumps({'text': 'Checking for new blobs in {env}..'.format(env=ENV)}),
        headers={"Content-Type": "application/json"}
    )

    get_files_in_source_bucket_job = GoogleCloudStorageListOperator(
        task_id='get_files_in_source_bucket_job',
        bucket=gcs_bucket_blobs_source,
        prefix=''
    )

    get_files_in_target_bucket_job = GoogleCloudStorageListOperator(
        task_id='get_files_in_target_bucket_job',
        bucket=gcs_bucket_blobs_target,
        prefix=''
    )

    def compare_buckets(**kwds):
        ti = kwds['ti']
        files_in_source = [each for each in ti.xcom_pull(task_ids='get_files_in_source_bucket_job')]
        files_in_target = [each for each in ti.xcom_pull(task_ids='get_files_in_target_bucket_job')]
        new_files = list(set(files_in_source)-set(files_in_target))
        return new_files

    compare_buckets_job = PythonOperator(
        task_id='compare_buckets_job',
        python_callable=compare_buckets,
        provide_context=True
    )

    copy_new_blobs_job = GoogleCloudStorageToGoogleCloudStorageOperator(
        task_id='copy_new_blobs_job',
        source_bucket=gcs_bucket_blobs_source,
        destination_bucket=gcs_bucket_blobs_target,
        upstream_batch_provider_task_id='compare_buckets_job'
    )

    slack_start_notification_job >> get_files_in_source_bucket_job >> get_files_in_target_bucket_job >> compare_buckets_job >> copy_new_blobs_job
