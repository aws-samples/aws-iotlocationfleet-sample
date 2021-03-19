## AWS IoT Location Fleet Tracker Sample code

This example application creates an IoT Thing, AWS IoT policy and certificate, Amazon EventBridge rule and Lambda function. 
The SAM template accepts the following parameters and creates the components:
 ARN of Geofence Collection ID
 ARN of Location Tracker
 ARN of the AWS IoT certificate
 Email ID to send notification to
 
 The sample python program will simulate the gps location updates being sent to IoT core which are directed to Amazon Location services which triggers an EventBridge notification based on the geo event of the asset entering a geofenced location around the warehouse.

Important: this application uses various AWS services and there are costs associated with these services after the Free Tier usage - please see the [AWS Pricing page](https://aws.amazon.com/pricing/) for details. You are responsible for any AWS costs incurred. No warranty is implied in this example.

```bash
.
├── README.MD                  <-- This instructions file
├── LambdaFunction             <-- Source code for a lambda function
│   └── lambda_function.py     <-- Main Lambda handler
│   └── requirements.txt       <-- Requirements file
├── template.yaml              <-- SAM template
├── LocationIoT.py             <-- Python client program to generate IoT events
```

## Requirements

* AWS CLI already configured with Administrator permission
* [Python 3.x installed](https://www.python.org/downloads/)

## Installation Instructions

1. [Create an AWS account](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html) if you do not already have one and login.

2. [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and [install the AWS Serverless Application Model CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) on your local machine.

3. Create a geofence collection, location tracker and AWS IoT certificate.

4. Create a new directory, navigate to that directory in a terminal and using command line clone the repository: ```git clone https://github.com/aws-samples/aws-iotlocationfleet-sample```.

5. From the command line, run:
```
cd ./aws-iotlocationfleet-sample
sam deploy --guided
```
Choose a stack name, input the parameter values, and allow SAM to create the resources.

## How it works

It has 3 parts:
i) template.yaml - This is the SAM template which creates the resources - 
               IoT Thing
               IoT Policy
               IoT Certificate
               Amazon EventBridge rule
               IoT topic

ii) Lambda function code - this is used by the above SAM template to create the Lambda function which gets invoked by IoT rule and will pipe data from IoT to location services

iii) LocationIoT.py - This is a python code that will run on the users laptop and uses AWS IoT Python SDK to send location coordinates to IoT Core. This mimics an IoT device attached to an asset which sends location coordinates as it navigates.

The sample python program will simulate the gps location updates being sent to IoT core which are directed to Amazon Location services which triggers an EventBridge notification based on the geo event of the asset entering a geofenced location around the target.

==============================================

Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.

SPDX-License-Identifier: MIT-0
## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

