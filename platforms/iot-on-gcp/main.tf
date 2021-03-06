variable "gac" {
  type = "string"
}

variable "project" {
  type = "string"
}

variable "region" {
  type = "string"
}

variable "zone" {
  type = "string"
}

variable "gce_vm" {
  type = "string"
}

variable "pubsub_topic" {
  type = "string"
}

variable "bq_dataset" {
  type = "string"
}

variable "bq_table" {
  type = "string"
}

variable "gcs_bucket" {
  type = "string"
}

variable "iot_registry" {
  type = "string"
}

variable "df_job_folder" {
  type = "string"
}

variable "df_template" {
  type = "string"
}

variable "df_tmp_folder" {
  type = "string"
}

variable "df_job" {
  type = "string"
}

provider "google" {
  credentials = var.gac
  project     = var.project
  region      = var.region
}

resource "random_id" "instance_id" {
  byte_length = 4
}

resource "google_compute_instance" "default" {
  name         = "${var.gce_vm}-${random_id.instance_id.hex}"
  machine_type = "n1-standard-1"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "debian-9-stretch-v20190729"
    }
  }

  network_interface {
    network = "default"
    access_config {
      //ephemeral IP
    }
  }

  depends_on = [
    google_pubsub_topic_iam_member.editor,
  ]
}

resource "google_pubsub_topic" "default" {
  name = var.pubsub_topic
}

resource "google_pubsub_topic_iam_member" "editor" {
  topic  = "projects/${var.project}/topics/${var.pubsub_topic}"
  role   = "roles/pubsub.publisher"
  member = "serviceAccount:cloud-iot@system.gserviceaccount.com"

  depends_on = [
    google_pubsub_topic.default,
  ]
}

resource "google_bigquery_dataset" "default" {
  dataset_id = var.bq_dataset
  location   = "EU"
}

resource "google_bigquery_table" "default" {
  dataset_id = "${google_bigquery_dataset.default.dataset_id}"
  table_id   = var.bq_table

  depends_on = [
    google_bigquery_dataset.default,
  ]

  schema = <<EOF
  [
      {
          "name": "timestamp",
          "type": "INTEGER",
          "mode": "REQUIRED"
      },
      {
          "name": "device",
          "type": "STRING",
          "mode": "REQUIRED"
      },
      {
          "name": "temperature",
          "type": "FLOAT",
          "mode": "REQUIRED"
      },
      {
          "name": "humidity",
          "type": "FLOAT",
          "mode": "REQUIRED"
      }
  ]
  EOF
}

resource "google_storage_bucket" "dataflow-staging" {
  name          = var.gcs_bucket
  location      = "EU"
  force_destroy = true
}

resource "google_cloudiot_registry" "default" {
  name = var.iot_registry

  event_notification_config = {
    pubsub_topic_name = "projects/${var.project}/topics/${var.pubsub_topic}"
  }

  mqtt_config = {
    mqtt_enabled_state = "MQTT_ENABLED"
  }

  depends_on = [
    google_pubsub_topic.default,
  ]

  credentials = [
    {
      public_key_certificate = {
        format      = "X509_CERTIFICATE_PEM"
        certificate = "${file("rsa_cert.pem")}"
      }
    },
  ]
}

resource "null_resource" "beam-staging" {
  provisioner "local-exec" {
    command = "cd beam; ./deploy.sh; cd .."
  }

  depends_on = [
    google_storage_bucket.dataflow-staging,
    google_pubsub_topic_iam_member.editor,
    google_bigquery_table.default,
    google_compute_instance.default
  ]
}

resource "google_dataflow_job" "default" {
    name = var.df_job
    zone = "us-central1-a"
    template_gcs_path = "gs://${var.gcs_bucket}/${var.df_job_folder}/${var.df_template}"
    temp_gcs_location = "gs://${var.gcs_bucket}/${var.df_tmp_folder}"
    parameters = {
        stream = "projects/${var.project}/topics/${var.pubsub_topic}"
        sink = "${var.project}:${var.bq_dataset}.${var.bq_table}"
    }
    depends_on = [
        null_resource.beam-staging,
    ]
}
