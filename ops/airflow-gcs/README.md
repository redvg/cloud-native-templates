- runs daily, controlled by `schedule_interval`
- dag uses 2 custom operators, check upstream airflow which might already have those
- dag depends on `slack_foo` http conn string in config 
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
