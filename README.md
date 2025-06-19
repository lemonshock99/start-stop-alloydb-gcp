# start-stop-alloydb-gcp
cloudrun function for start stop alloyDB in GCP

flow
Cloud Scheduler ------> Pub/Sub ------> Cloudrun Function

Permission
**service account permission**
- AlloyDB admin

**add service account Pub/Sub trigger in function**
- Cloud Run Invoker

**adjust retry policy in pub/sub**
Acknowledgement deadline: 60
Retry policy:
- min: 10
- max: 20


