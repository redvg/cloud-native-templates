#!/bin/bash


echo 'deploying fleet with 20 devices and 10,000 signals each'
SIGNALS=10000
for i in {1..20}
do
  ID="fleet-device-$i-$(date +%s000)"
  echo 'creating device:' $ID
  gcloud beta iot devices create $ID \
    --project=$PROJECT_ID \
    --region=$REGION \
    --registry=simulation \
    --public-key path=rsa_cert.pem,type=rs256
  echo 'sending signals:' $SIGNALS
  python mqtt.py \
    --project_id=$PROJECT_ID \
    --cloud_region=$REGION \
    --registry_id=simulation \
    --device_id=$ID \
    --private_key_file=rsa_private.pem \
    --message_type=event \
    --num_messages=$SIGNALS \
    --algorithm=RS256 > $ID.log &
done
