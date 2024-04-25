"""
Auth: Jatan Pandya
Script to send downlink messages sequentially using boto3 sdk
"""

import boto3
import time
import base64 
import random


def send_data(freq, total_N):
    seq = 0
    iotwireless = boto3.client('iotwireless')
    device_id = "5ac752d9-a6ab-4ba0-bef5-304a0cc41c9b"
    transmit_mode = 1 
    
    for i in range(freq):  
        PAYLOAD_DATA_RAW = f"MSG={random.randint(1,2)} SEQ={seq}"
        PAYLOAD_BYTE = PAYLOAD_DATA_RAW.encode("ascii")
        PAYLOAD_BYTE_BASE_64 = base64.b64encode(PAYLOAD_BYTE)
        PAYLOAD_BYTE_STR = PAYLOAD_BYTE_BASE_64.decode("ascii")


        wireless_metadata = {
            "Sidewalk": {
                "Seq": seq,
                "MessageType": "CUSTOM_COMMAND_ID_NOTIFY",
                "AckModeRetryDurationSecs": 60
            }
        }

        response = iotwireless.send_data_to_wireless_device(
            Id=device_id,
            TransmitMode=transmit_mode,
            PayloadData=PAYLOAD_BYTE_STR,
            WirelessMetadata=wireless_metadata
        )
        seq += 1
        print(PAYLOAD_DATA_RAW)
        time.sleep(total_N)

send_data(100,20)
