from datetime import datetime
import json
import os

import boto3

TRACKER_NAME = "myfleettracker"

def lambda_handler(event, context):

  updates = [
    {
      "DeviceId": event["deviceid"],
      "SampleTime": datetime.fromtimestamp(event["timestamp"]).isoformat(),
      "Position": [
        event["location"]["long"],
        event["location"]["lat"]
      ]
    }
  ]

  client = boto3.client("location")
  response = client.batch_update_device_position(TrackerName=TRACKER_NAME, Updates=updates)

  return {
    "statusCode": 200,
    "body": json.dumps(response)
  }
