#Function entry point: hello_pubsub

import base64
import json
import functions_framework
import google.auth
import google.auth.transport.requests
import requests
import asyncio


# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def hello_pubsub(cloud_event):
    try:
        message_data = base64.b64decode(cloud_event.data["message"]["data"])
        # Convert bytes to string and parse JSON
        json_str = message_data.decode('utf-8')
        datas = json.loads(json_str)

        print("---- start main function ---")
        print(datas)

        asyncio.run(run_all(datas))
    except:
        return "-----error------"


async def run_all(datas):

    tasks = []
    count = 1
    for data in datas["data"]:
        print(data)
        print(f"---- Loop count = {count}")
        projectID = data["project_id"]
        region = data["region"]
        clusterID = data["clusterID"]
        instanceID = data["instance_id"]
        action = data["action"]

        tasks.append(asyncio.create_task(stop_alloydb_instance_via_api(projectID, region, clusterID, instanceID, action)))
        count = count+1
        await asyncio.sleep(5)
    
    # for i in range(5):
    #     tasks.append(asyncio.create_task(funcB(i)))
    await asyncio.gather(*tasks)
    return "Function success"

# async def funcB(i):
#     print(f"Start {i}")
#     await asyncio.sleep(1)  # จำลองงานที่ใช้เวลา
#     print(f"End {i}")

async def stop_alloydb_instance_via_api(project_id: str, region: str, cluster_id: str, instance_id: str, action: str):
    """
    Stops an AlloyDB instance by calling the AlloyDB Admin API to set activation policy to NEVER.

    :param project_id: GCP project ID
    :param region: GCP region, e.g. 'asia-southeast1'
    :param cluster_id: AlloyDB cluster ID
    :param instance_id: AlloyDB instance ID
    """

    if action == "start":
        policy = "ALWAYS"
    elif action == "stop":
        policy = "NEVER"


    # 1. Get credentials and access token
    credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    credentials.refresh(google.auth.transport.requests.Request())
    access_token = credentials.token

    # 2. Define API endpoint
    instance_path = f"projects/{project_id}/locations/{region}/clusters/{cluster_id}/instances/{instance_id}"
    url = f"https://alloydb.googleapis.com/v1/{instance_path}?updateMask=activationPolicy"

    # 3. Prepare request headers and body
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "activationPolicy": policy
    }

    # 4. Send PATCH request
    try:
        response = requests.patch(url, headers=headers, json=body)

        if response.status_code == 200:
            print(f"Successfully {action} AlloyDB instance '{instance_id}'.")
        else:
            print(f"Failed to stop AlloyDB instance '{instance_id}'. Status: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error ----- {e}")
        
