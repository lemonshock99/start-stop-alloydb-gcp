# start-stop-alloydb-gcp
cloudrun function for start stop alloyDB in GCP

**flow**
Cloud Scheduler ------> Pub/Sub ------> Cloudrun Function

Permission
**service account permission**
- AlloyDB admin

**add service account Pub/Sub trigger in [ function > security > permission ]**
- Cloud Run Invoker

**adjust retry policy in pub/sub**
Acknowledgement deadline: 60
Retry policy:
- min: 10
- max: 20

**Cloud Scheduler Configuration**
- frequency in cron format
    (minute) (Hour) (day) (month) (day of week mon-sun)
    
    *example* 30 19 * * 1-5
    Minute and Hour:
    At 7:30 PM
    and Day:
    From Monday to Friday
- target type
  pub/sub and chose pubsub topic
- Message Body

```
    {
      "data": [
        {
        {"project_id": <Project ID>,
          "region": <AlloyDB Region>,
          "clusterID": <AlloyDB Cluster ID>,
          "instance_id": <AlloyDB Instance ID>,
          "action": "start" # start/stop
        },
        {
          ......
        }
      ]
    }
```
