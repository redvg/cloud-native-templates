- dag uses http operator for slack notification, also possible to use SlackWebhookHook contribution
- dag uses contributed datastore operator, also possible to use official one
- dag depends on `slack_foo` http conn string in config 
- dag depends on slack webhook endpoint string
- runs daily, controlled by `schedule_interval`
- set necessary env vars
```bash
gcloud composer environments run foo \
     --location europe-west1 variables -- \
     --set bar zar
```
- deploying to GCP Cloud Composer is simply copying DAG files to DAG folder of respective Cloud Composer environment in GCS
```bash
gsutil -m cp *.py gs://[region]-[composer-env-id]-bucket/dags
```
