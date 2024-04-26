# Fleet Management for AWS Sidewalk Nodes

This repository contains scripts to manage fleet and perform Over-The-Air (OTA) configurations for AWS Sidewalk Nodes.

## Structure

1. **Uplink/parse.py/js**: Script to parse uplink payload according to the backend structure.
2. **Downlink/downlinker.py**: Script to prepare and send downlink payload to node devices using AWS Boto3 SDK.
3. **Downlink/config.json**: JSON file containing configuration parameters required to prepare the payload.

## Running the Script

### Prerequisites

1. Ensure you have your AWS account configured and authorized.
2. Install the `boto3` SDK (Python3 AWS SDK).

### Script Usage

1. Run the script using the command:
   ```
   python3 downlinker.py --config </path/to/config.json> --routine <name_of_the_routine>
   ```
2. By default:
   - The script looks for `config.json` in the current working directory.
   - If no "--routine" is supplied, the script runs the "default" routine.

### Example Usages

- Run with default settings:
  ```
  python3 downlinker.py
  ```
- Run with a specific routine:
  ```
  python3 downlinker.py --routine routine1
  ```

_Last Updated 4/25/2024_
