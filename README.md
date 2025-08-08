# AWS IoT Location Fleet Tracker

A production-ready solution for real-time fleet tracking and geofence monitoring using AWS IoT Core and Amazon Location Services.

## Overview

This application demonstrates how to build a complete IoT fleet tracking system that detects when vehicles or assets enter or exit predefined geographic boundaries (geofences). When a tracked asset crosses a geofence boundary, the system automatically sends email notifications to designated recipients.

## Key Concepts

### Trackers
In Amazon Location Service, a **Tracker** is a resource that stores and manages the position history of your devices or assets. Trackers receive location updates from your devices and maintain a record of their movements over time. In this project, the tracker named `myfleettracker` receives location updates from the IoT device and enables real-time monitoring of fleet vehicles.

### Geofence Collections
A **Geofence Collection** is a container for geofences in Amazon Location Service. It groups related geofences together and manages the evaluation of position updates against these boundaries. In this project, the geofence collection named `myfleetgeofences` holds the warehouse boundary definition and generates events when tracked devices interact with it.

### Geofences
A **Geofence** is a virtual perimeter defined around a geographic area. When a tracked device enters or exits this perimeter, the system generates an event. In this project, we define a geofence named `mywarehouse` that represents a warehouse facility. The system sends notifications when fleet vehicles enter or exit this area, enabling real-time awareness of vehicle movements at critical locations.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │     │                 │
│  IoT Device     │     │   AWS IoT Core  │     │  AWS Lambda     │     │ Amazon Location │
│  (Simulator)    │────▶│                 │────▶│                 │────▶│   Service       │
│                 │     │                 │     │                 │     │                 │
└─────────────────┘     └────────┬────────┘     └─────────────────┘     └────────┬────────┘
                                 │                                               │
                                 │                                               │
                                 │                                               │
                                 │                                               │
                        ┌────────▼────────┐                            ┌─────────▼─────────┐
                        │                 │                            │                   │
                        │  IoT Rule       │                            │ Geofence Event    │
                        │                 │                            │                   │
                        └────────┬────────┘                            └─────────┬─────────┘
                                 │                                               │
                                 │                                               │
                                 │                                               │
                                 │                                               │
                                 │                                     ┌─────────▼─────────┐
                                 │                                     │                   │
                                 │                                     │ Amazon EventBridge│
                                 │                                     │                   │
                                 │                                     └─────────┬─────────┘
                                 │                                               │
                                 │                                               │
                                 │                                               │
                                 │                                               │
                        ┌────────▼────────┐                            ┌─────────▼─────────┐
                        │                 │                            │                   │
                        │  Certificate    │                            │   Amazon SNS      │
                        │                 │                            │                   │
                        └─────────────────┘                            └─────────┬─────────┘
                                                                                 │
                                                                                 │
                                                                                 │
                                                                                 │
                                                                       ┌─────────▼─────────┐
                                                                       │                   │
                                                                       │  Email            │
                                                                       │  Notification     │
                                                                       │                   │
                                                                       └───────────────────┘
```

The solution consists of:

1. **IoT Device (Simulator)**: A Python client that simulates a GPS-enabled device sending location coordinates
2. **AWS IoT Core**: Securely ingests location data from devices using MQTT protocol
3. **IoT Rule**: Routes incoming messages to the Lambda function
4. **Certificate**: Authenticates the IoT device for secure communication
5. **AWS Lambda**: Processes location updates and forwards them to Amazon Location Service
6. **Amazon Location Service**: 
   - Tracks device positions using the Tracker resource
   - Monitors geofence boundaries using the Geofence Collection
   - Generates events when devices enter or exit geofences
7. **Amazon EventBridge**: Routes geofence events to notification services based on rules
8. **Amazon SNS**: Delivers email notifications to designated recipients
9. **Email Notification**: Alerts stakeholders when vehicles enter or exit the warehouse area

## Prerequisites

- AWS Account with administrator access
- [AWS CLI](https://aws.amazon.com/cli/) configured with your credentials
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) installed
- [Python 3.8+](https://www.python.org/downloads/) installed
- Basic knowledge of AWS services

## Pre-Deployment Setup

Before deploying the SAM template, you need to create three key resources in AWS:

### 1. Create an Amazon Location Service Tracker

1. Navigate to the [Amazon Location Service console](https://console.aws.amazon.com/location/home)
2. Click on **Trackers** under **Manage Resources** in the left navigation panel
3. Click **Create tracker**
4. Enter a name (e.g., `myfleettracker`)
5. Select your desired position filtering
6. Click **Create tracker**
7. After creation, note the tracker ARN (format: `arn:aws:geo:[region]:[account-id]:tracker/myfleettracker`)

### 2. Create an Amazon Location Service Geofence Collection

1. In the Amazon Location Service console, click on **Geofences** under **Manage Resources** in the left navigation panel
2. Click **Create geofence collection**
3. Enter a name (e.g., `myfleetgeofences`)
4. Keep all the selects as default
5. Click **Create geofence collection**
6. In the **Geofences** tab, click **Add geofences**
7. For the geofence entry method, select **Browse files**
8. Create a GeoJSON file named `warehouse-geofence.json` with the following content:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [-78.69000, 35.80280],
            [-78.69000, 35.80220],
            [-78.68850, 35.80220],
            [-78.68850, 35.80280],
            [-78.69000, 35.80280]
          ]
        ]
      },
      "properties": {
        "geofenceId": "mywarehouse",
        "name": "Warehouse Facility",
        "description": "Main warehouse facility for fleet operations"
      }
    }
  ]
}
```

10. Click **Choose file** and select your GeoJSON file
11. Click **Add geofences**

> **Note:** The coordinates in the sample GeoJSON file define a simple rectangular geofence near the location used in the simulation code. You should adjust these coordinates to match your desired geofence location.

12. To find the ARN, go back to the geofence collections list, select your collection, and check the **Details** section
13. Note the geofence collection ARN (format: `arn:aws:geo:[region]:[account-id]:geofence-collection/myfleetgeofences`)

### 3. Create an AWS IoT Certificate

1. Navigate to the [AWS IoT Core console](https://console.aws.amazon.com/iot/home)
2. In the left navigation panel, expand **Security**, then click **Certificates**
3. Under the **Add certificate** button menu,  Click **Create certificate**
4. Under "Certificate branch selection", select **Auto-generate new certificate (recommended)**
5. Under Certificate status, select **Active** as the certificate status selection
6. Click **Create**
7. On the "Download certificates and keys" page, download all the certificate files:
   - Device certificate
   - Private key
   - Root CA certificate (Amazon Root CA 1)
   
   > **Important:** This is your only opportunity to download these files. If you don't download them now, you'll need to create a new certificate.
8. Click **Continue**  (we'll attach policies later through the SAM template)   
9. Click on the certificate ID to view its details page
10. Note the certificate ARN (format: `arn:aws:iot:[region]:[account-id]:cert/[certificate-id]`)
11. Rename the downloaded files to match what the code expects and place them in the same code folder:
    - Device certificate → `myfleetiot.cert.pem`
    - Private key → `myfleetiot.private.key`
    - Root CA certificate → `AmazonRootCA1.crt`

### How These Resources Work Together

- **IoT Certificate**: Authenticates your device to securely connect to AWS IoT Core and publish location data
- **Location Tracker**: Stores and manages the position history of your devices
- **Geofence Collection**: Defines geographic boundaries and generates events when tracked devices enter or exit these areas

The Lambda function receives location data from IoT Core and updates the device position in the Location Tracker. When a device crosses a geofence boundary in your Geofence Collection, Amazon Location Service generates an event that triggers the EventBridge rule and sends a notification.

## Deployment

```bash
# Clone the repository
git clone https://github.com/aws-samples/aws-iotlocationfleet-sample
cd aws-iotlocationfleet-sample

# Deploy the application
sam deploy --guided
```

When prompted, provide:
- Stack name (e.g., `iot-location-fleet`)
- ARN of your Location geofence collection (from step 2)
- ARN of your Location tracker (from step 1)
- ARN of your IoT certificate (from step 3)
- Email address for notifications

Note : You will recieve an email to confirm Subscription of topic : arn:aws:sns:us-west-2:[AccountId]]:myfleetlocationtopic

It takes close to 3 mins for the Stack creation process to complete and you will see a message similar to : "Successfully created/updated stack - iot-location-fleet in us-west-2
"

### 2. Configure the IoT Device Simulator

Before running the simulator:

1. Download your IoT certificate files from AWS IoT Core console
2. Place the following files in the same directory as `LocationIoT.py`:
   - `AmazonRootCA1.crt`
   - `myfleetiot.cert.pem`
   - `myfleetiot.private.key`

### 3. Run the Simulator

First, install the required Python packages:

```bash
# Install required packages
pip3 install AWSIoTPythonSDK

# If you encounter ModuleNotFoundError: No module named 'psutil'
# Try installing with:
pip3 install psutil

# On some systems, you might need to install development tools first:
# For Ubuntu/Debian:
# sudo apt-get install python3-dev
# For Red Hat/CentOS:
# sudo yum install python3-devel
# For macOS (with Homebrew):
# brew install python
```

Then run the simulator:

```bash
python LocationIoT.py
# or if that doesn't work:
python3 LocationIoT.py
```

When prompted, enter your IoT endpoint (found in AWS IoT Core console under Settings > Device data endpoint).

## Troubleshooting

### Connection Timeout Error

If you encounter a `connectTimeoutException` error like:
```
Connect timed out
AWSIoTPythonSDK.exception.AWSIoTExceptions.connectTimeoutException
```

This indicates the IoT device simulator cannot connect to AWS IoT Core. Here are the most common causes and solutions:

#### 1. Certificate Issues
- **Problem**: Certificate not activated or incorrectly named
- **Solution**: 
  - Ensure your certificate is **ACTIVE** in the AWS IoT Core console
  - Verify certificate files are named correctly:
    - `myfleetiot.cert.pem` (device certificate)
    - `myfleetiot.private.key` (private key)
    - `AmazonRootCA1.crt` (root CA certificate)
  - Check that all three files are in the same directory as `LocationIoT.py`

#### 2. Policy Not Attached
- **Problem**: The IoT policy hasn't been attached to the certificate
- **Solution**: 
  - Deploy the SAM template first (`sam deploy --guided`)
  - The template automatically creates and attaches the required policy
  - If you created the certificate manually, ensure the policy `myfleetiotpolicy` is attached

#### 3. Incorrect IoT Endpoint
- **Problem**: Wrong or malformed IoT endpoint URL
- **Solution**:
  - Go to AWS IoT Core console → Settings → Device data endpoint
  - Copy the exact endpoint (format: `xxxxxxxx-ats.iot.region.amazonaws.com`)
  - Don't include `https://` prefix when entering the endpoint

#### 4. Region Mismatch
- **Problem**: Certificate and endpoint are in different AWS regions
- **Solution**:
  - Ensure your certificate, IoT endpoint, and other resources are in the same region
  - Check the region in your IoT endpoint URL (e.g., `us-west-2`)

#### 5. Network/Firewall Issues
- **Problem**: Corporate firewall blocking port 8883
- **Solution**:
  - Ensure port 8883 (MQTT over TLS) is open
  - Try from a different network if possible
  - Contact your network administrator if needed

#### 6. File Permissions
- **Problem**: Certificate files don't have proper read permissions
- **Solution**:
  ```bash
  chmod 644 myfleetiot.cert.pem
  chmod 600 myfleetiot.private.key
  chmod 644 AmazonRootCA1.crt
  ```

### Testing Connection
To verify your setup before running the full simulator:

1. **Check certificate status**:
   - Go to AWS IoT Core → Security → Certificates
   - Ensure your certificate shows as "ACTIVE"

2. **Verify policy attachment**:
   - Click on your certificate
   - Check the "Policies" tab to ensure `myfleetiotpolicy` is attached

3. **Test with AWS IoT Device Tester** (optional):
   - Use AWS IoT Device Tester for additional connection validation

### Other Common Issues

#### Module Import Errors
```bash
# Install missing modules
pip3 install AWSIoTPythonSDK==1.4.9 psutil
```

#### Python Version Issues
```bash
# Use Python 3.8 or higher
python3 --version
# If needed, install Python 3.8+
```

### No Geofence Alerts Received

If the simulator runs successfully but you don't receive email notifications for geofence events:

#### 1. Coordinate Mismatch
- **Problem**: Simulation coordinates don't cross the geofence boundary
- **Solution**: 
  - Use the updated `warehouse-geofence.json` file provided above
  - The geofence now covers the simulation path coordinates
  - Re-upload the corrected GeoJSON file to your geofence collection

#### 2. SNS Subscription Not Confirmed
- **Problem**: Email subscription to SNS topic not confirmed
- **Solution**:
  - Check your email for a subscription confirmation message
  - Click the "Confirm subscription" link in the email
  - If no email received, check spam folder

#### 3. EventBridge Rule Configuration
- **Problem**: EventBridge rule not properly configured or GeofenceId mismatch
- **Solution**:
  - Go to Amazon EventBridge console → Rules
  - Find the rule `myfleeteventrule`
  - Verify it's enabled and targets the correct SNS topic
  - **Important**: If you see geofence events in CloudWatch but no emails, check if the GeofenceId in the events matches what the EventBridge rule expects. The updated template removes the GeofenceId filter to match any geofence.

#### 4. Location Service Integration
- **Problem**: Tracker and geofence collection not properly linked
- **Solution**:
  - Ensure both tracker and geofence collection are in the same region
  - Verify the ARNs used in the SAM deployment are correct

#### 5. Testing Geofence Events
To verify your geofence is working:

1. **Check Amazon Location Service console**:
   - Go to Amazon Location Service → Trackers
   - Select your tracker (`myfleettracker`)
   - View the device positions on the map
   - Verify the positions are being updated

2. **Monitor EventBridge**:
   - Go to Amazon EventBridge → Rules
   - Check the metrics for your rule to see if events are being processed

3. **Check CloudWatch Logs**:
   - Look for Lambda function logs to verify location updates are being processed

#### 6. GeofenceId Mismatch Issue
- **Problem**: You see geofence events in CloudWatch logs but no email alerts
- **Symptoms**: CloudWatch shows events like:
  ```json
  {
    "detail": {
      "EventType": "ENTER",
      "GeofenceId": "monitoring-67ed3b24-c116-407e-ae81-a63f470dd4cf",
      "DeviceId": "deviceid1"
    }
  }
  ```
- **Solution**: The EventBridge rule was looking for `GeofenceId: "mywarehouse"` but AWS Location Service generates random GeofenceIds. The updated template.yaml removes this filter to match any GeofenceId.

#### 7. Manual Testing
You can manually test the geofence by modifying coordinates in LocationIoT.py:

```python
# Add a test coordinate that's clearly outside the geofence
switcher={
    1: (-78.70000, 35.80000),  # Outside geofence
    2: (-78.69000, 35.80250),  # Inside geofence
    3: (-78.70000, 35.80000),  # Outside geofence again
}
```

## Customization

### Modifying the Geofence Path

Edit the `switcher` dictionaries in `LocationIoT.py` to change the simulated path:

```python
# Change this to 'exit' to simulate leaving the geofence
mode = 'exit'
```

### Adding More Devices

1. Create additional IoT Things in AWS IoT Core
2. Update the `deviceid` in `getlocation()` function
3. Create new certificate for each device

## Monitoring

1. Check AWS IoT Core for incoming messages
2. View Amazon Location Service console to see device positions
3. Monitor your email for geofence notifications

## Cost Considerations

This application uses several AWS services that may incur costs beyond the Free Tier:
- AWS IoT Core (message ingestion)
- AWS Lambda (invocations)
- Amazon Location Service (tracking and geofencing)
- Amazon SNS (notifications)

Review the [AWS Pricing Calculator](https://calculator.aws/) to estimate costs for your specific use case.

## Security

- All IoT communications are secured with TLS certificates
- IAM roles enforce least-privilege access
- See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for security issue reporting

## License

This project is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file for details.