"""
Auth: Jatan Pandya 4/25/2024

Script to prepare Downlink Payload

Structure:

Sets the buzzer volume to Low, Medium, or High (0, 1, 2).
01 = Buzzer_Set

Enables or disables the NFC reader.
02 = NFC_Set

Sets the "Bin Full" sensor alert distance to 0, 1, or 2.
03 = Bin_Level

Adjusts the UHF reader power to 0, 1, or 2.
04 = UHF_Power

Customizes the LED display for Venue 1, Venue 2, or Venue 3.
05 = Display_Set

Assigns a unique ID to each Topper board.
06 = BinID_Set

Configures NFC parameters for updating the merchant ID.
07 = NFC_Merch_Set



Example :

Buzzer_Set = "Low"
NFC_Set = "Enable"
Bin_Level = "Low"
UHF_Power = "Low"
Display_Set = "Venue_1"
BinID_Set = "QTLLC"
NFC_Merch_Set = "VTAP007"

"""



import boto3
import time
import base64 

class Downlink:
    def __init__(self, Buzzer_Set="DEFAULT", NFC_Set="DEFAULT", Bin_Level="DEFAULT", UHF_Power="DEFAULT", Display_Set="DEFAULT", BinID_Set="DEFAULT", NFC_Merch_Set="DEFAULT"):
        self.Buzzer_Set = Buzzer_Set
        self.NFC_Set = NFC_Set
        self.Bin_Level = Bin_Level
        self.UHF_Power = UHF_Power
        self.Display_Set = Display_Set
        self.BinID_Set = BinID_Set
        self.NFC_Merch_Set = NFC_Merch_Set

        
        ## Class Variables
        self.payload_raw = ''
        self.payload = ''

    def configure(self):
        """
        make lower level abstraction changes. Allowing backend to have control over variables.
        eg. Buzzer_Set = "Low" --> 0. And henceforth

        
        Keeping self.BinID_Set, self.NFC_Merch_Set unchanged

        """

        SetMap = {

            "LEVEL" : {
                "low" : "0",
                "medium" : "1",
                "high" : "2",
            },
            
            "FLAG" : {
                "enable" : "1",
                "disable" : "0"
            },
            

            # Set Internal ID for each Venue. E.g. User's Pepsi will interpreted as P101_East at backend
            "VENUE" : {
                "venue1" : "Venue_1",
                "venue2" : "Venue_2",
                "venue3" : "Venue_3"
            }

        }


        if self.Buzzer_Set.lower() in SetMap["LEVEL"]:
            self.Buzzer_Set = SetMap["LEVEL"][self.Buzzer_Set.lower()]
        elif self.Buzzer_Set == 'DEFAULT':
            pass
        else:
            raise ValueError("Acceptable parameters for <Buzzer_Set> are 'low', 'medium', or 'high'")
        
        if self.NFC_Set.lower() in SetMap["FLAG"]:
            self.NFC_Set = SetMap["FLAG"][self.NFC_Set.lower()]
        elif self.NFC_Set == 'DEFAULT':
            pass
        else:
            raise ValueError("Acceptable parameters for <NFC_Set> are 'enable' or 'disable'")
    
        if self.Bin_Level.lower() in SetMap["LEVEL"]:
            self.Bin_Level = SetMap["LEVEL"][self.Bin_Level.lower()]
        elif self.Bin_Level == 'DEFAULT':
            pass
        else:
            raise ValueError("Acceptable parameters for <Bin_Level> are 'low', 'medium', or 'high'")
        
        if self.UHF_Power.lower() in SetMap["LEVEL"]:
            self.UHF_Power = SetMap["LEVEL"][self.UHF_Power.lower()]
        elif self.UHF_Power == 'DEFAULT':
            pass
        else:
            raise ValueError("Acceptable parameters for <UHF_Power> are 'low', 'medium', or 'high'")
        
        if self.Display_Set.lower() in SetMap["VENUE"]:
            self.Display_Set = SetMap["VENUE"][self.Display_Set.lower()]
        elif self.Display_Set == 'DEFAULT':
            pass
        else:
            raise ValueError("Acceptable parameters for <Display_Set> are 'VENUE1', 'VENUE1', or 'VENUE1'")
        

    def payloadStruct(self):
        SEP = ","
        self.payload_raw = self.Buzzer_Set + SEP + self.NFC_Set + SEP + self.Bin_Level + SEP + self.UHF_Power + SEP + self.Display_Set + SEP + self.BinID_Set + SEP + self.NFC_Merch_Set
        print(f"\nRaw Payload : {self.payload_raw}\n")
        

    def encoder(self):
        PAYLOAD_BYTE = self.payload_raw.encode("ascii")
        PAYLOAD_BYTE_BASE_64 = base64.b64encode(PAYLOAD_BYTE)
        self.payload = PAYLOAD_BYTE_BASE_64.decode("ascii")
        print(f"Byte64 Payload : {self.payload}\n")


    def prep(self):
        self.configure()
        self.payloadStruct()
        self.encoder()


    def awsDownlink(self, N, freq, device_id="5ac752d9-a6ab-4ba0-bef5-304a0cc41c9b"):
        self.prep()
        iotwireless = boto3.client('iotwireless')
        transmit_mode = 1

        for i in range(1,N+1):  
            wireless_metadata = {
                "Sidewalk": {
                    "Seq": i,
                    "MessageType": "CUSTOM_COMMAND_ID_NOTIFY",
                    "AckModeRetryDurationSecs": 60
                }
            }

            response = iotwireless.send_data_to_wireless_device(
                Id=device_id,
                TransmitMode=transmit_mode,
                PayloadData=self.payload,
                WirelessMetadata=wireless_metadata
            )

            print(f"Payload '{self.payload}' sent to device '{device_id}'")
            time.sleep(freq)
        print("\nCompleted!\n")



def main():
    dl = Downlink(Buzzer_Set="LOW",NFC_Set="ENABLE",Bin_Level="LOW",UHF_Power="LOW",Display_Set="VENUE1",BinID_Set="JP001", NFC_Merch_Set="VTAP010")
    dl.awsDownlink(N=10, freq=1)

main()