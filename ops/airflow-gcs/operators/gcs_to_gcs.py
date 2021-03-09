from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import logging

# https://airflow.readthedocs.io/en/stable/_modules/airflow/contrib/operators/gcs_to_gcs.html

class GoogleCloudStorageToGoogleCloudStorageOperator(BaseOperator):

    template_fields = (
        'source_bucket',
        'destination_bucket',
        'upstream_batch_provider_task_id'
    )
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self,
                 source_bucket,
                 destination_bucket,
                 upstream_batch_provider_task_id,
                 google_cloud_storage_conn_id='google_cloud_default',
                 delegate_to=None,
                 last_modified_time=None,
                 *args,
                 **kwargs):
        
        super(GoogleCloudStorageToGoogleCloudStorageOperator, self).__init__(*args, **kwargs)
        
        self.source_bucket = source_bucket
        
        self.destination_bucket = destination_bucket

        self.upstream_batch_provider_task_id = upstream_batch_provider_task_id
        
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        
        self.delegate_to = delegate_to
        
        self.last_modified_time = last_modified_time
        
        self.wildcard = '*'

    def execute(self, context):

        downstreamed_list_of_objects = self.xcom_pull(
            context=context, 
            task_ids=self.upstream_batch_provider_task_id
        )

        hook = GoogleCloudStorageHook(
            google_cloud_storage_conn_id=self.google_cloud_storage_conn_id,
            delegate_to=self.delegate_to
        )

        for each in downstreamed_list_of_objects:

            if self.last_modified_time is not None:

                if hook.is_updated_after(self.source_bucket, source_object, self.last_modified_time):
                    
                    pass
            
                else:
                    
                    continue

            log_message = 'Executing copy of gs://{source_bucket}/{source_object} to gs://{destination_bucket}/{destination_object}'

            log_message.format(
                source_bucket=self.source_bucket,
                source_object=each,
                destination_bucket=self.destination_bucket,
                destination_object=each
            )

            self.log.info(log_message)
            
            # TODO: use rewrite()
            # see https://airflow.readthedocs.io/en/stable/_modules/airflow/contrib/hooks/gcs_hook.html
            hook.copy(
                self.source_bucket, 
                each,
                self.destination_bucket, 
                each
            )
