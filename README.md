# start-stop-alloydb-gcp
cloudrun function for start stop alloyDB in GCP

**flow** <br/>
Cloud Scheduler ------> Pub/Sub ------> Cloudrun Function
<br/>
Permission Required <br/>
**service account permission clourun function** ( Revision > Security > Identity & encryption > service account ) <br/>
- AlloyDB admin <br/>
<br/>
**add service account Pub/Sub trigger in [ function > security > permission ]** <br/>
- Cloud Run Invoker <br/>
<br/>
**adjust retry policy in pub/sub** <br/>
Acknowledgement deadline: 60 <br/>
Retry policy: <br/>
- min: 10 <br/>
- max: 20 <br/>
<br/>
**Cloud Scheduler Configuration**
- frequency in cron format <br/>
    (minute) (Hour) (day) (month) (day of week mon-sun) <br/>
    <br/>
    *example* 30 19 * * 1-5 <br/>
    Minute and Hour: <br/>
    At 7:30 PM <br/>
    and Day: <br/>
    From Monday to Friday <br/>
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
