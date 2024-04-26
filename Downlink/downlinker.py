"""
Auth: Jatan Pandya 4/25/2024
Script to prepare Downlink Payload
"""

# import boto3
import time
import base64
import json
import argparse
import os


class Downlink:
    """
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

    def __init__(
        self,
        Buzzer_Set="DEFAULT",
        NFC_Set="DEFAULT",
        Bin_Level="DEFAULT",
        UHF_Power="DEFAULT",
        Display_Set="DEFAULT",
        BinID_Set="DEFAULT",
        NFC_Merch_Set="DEFAULT",
        BOOT_MODE="DEFAULT",
        SEP="<SEP>",
    ):
        self.Buzzer_Set = Buzzer_Set
        self.NFC_Set = NFC_Set
        self.Bin_Level = Bin_Level
        self.UHF_Power = UHF_Power
        self.Display_Set = Display_Set
        self.BinID_Set = BinID_Set
        self.NFC_Merch_Set = NFC_Merch_Set
        self.BOOT_MODE = BOOT_MODE

        # Config vars
        self.SEP = SEP

        # Class Variables
        self.payload_raw = ""
        self.payload = ""

        # self.aws_client = boto3.client("iotwireless")

    def __str__(self):
        return (
            f"\n=== Settings Summary ===\n"
            f"Buzzer Setting: {self.Buzzer_Set}\n"
            f"NFC Setting: {self.NFC_Set}\n"
            f"Bin Level: {self.Bin_Level}\n"
            f"UHF Power: {self.UHF_Power}\n"
            f"Display Setting: {self.Display_Set}\n"
            f"Bin ID Setting: {self.BinID_Set}\n"
            f"NFC Merchant Setting: {self.NFC_Merch_Set}\n"
            f"Boot Mode: {self.BOOT_MODE}\n"
            f"<SEP>: '{self.SEP}'\n"
            f"========================\n"
        )

    def configure(self):
        """
        make lower level abstraction changes. Allowing backend to have control over variables.
        eg. Buzzer_Set = "Low" --> 0. And henceforth


        Keeping self.BinID_Set, self.NFC_Merch_Set unchanged

        """

        SetMap = {
            "LEVEL": {
                "low": "0",
                "medium": "1",
                "high": "2",
            },
            "FLAG": {"enable": "1", "disable": "0"},
            # Set Internal ID for each Venue. E.g. User's Pepsi will
            # interpreted as P101_East at backend
            "VENUE": {"pepsi_east": "PEPSIEASTNYC01", "pepsi_west": "PEPSIWESTSF03", "pepsi_mid": "PEPSIMIDCHI07"},
        }

        if self.Buzzer_Set.lower() in SetMap["LEVEL"]:
            self.Buzzer_Set = SetMap["LEVEL"][self.Buzzer_Set.lower()]
        elif self.Buzzer_Set == "DEFAULT":
            pass
        else:
            raise ValueError(
                f"Acceptable parameters for <Buzzer_Set> are {', '.join(SetMap['LEVEL'].keys())}"
            )

        if self.NFC_Set.lower() in SetMap["FLAG"]:
            self.NFC_Set = SetMap["FLAG"][self.NFC_Set.lower()]
        elif self.NFC_Set == "DEFAULT":
            pass
        else:
            raise ValueError(
                f"Acceptable parameters for <NFC_Set> are {', '.join(SetMap['FLAG'].keys())}"
            )

        if self.Bin_Level.lower() in SetMap["LEVEL"]:
            self.Bin_Level = SetMap["LEVEL"][self.Bin_Level.lower()]
        elif self.Bin_Level == "DEFAULT":
            pass
        else:
            raise ValueError(
                F"Acceptable parameters for <Bin_Level> are {', '.join(SetMap['LEVEL'].keys())}"
            )

        if self.UHF_Power.lower() in SetMap["LEVEL"]:
            self.UHF_Power = SetMap["LEVEL"][self.UHF_Power.lower()]
        elif self.UHF_Power == "DEFAULT":
            pass
        else:
            raise ValueError(
                f"Acceptable parameters for <UHF_Power> are {', '.join(SetMap['LEVEL'].keys())}"
            )

        if self.Display_Set.lower() in SetMap["VENUE"]:
            self.Display_Set = SetMap["VENUE"][self.Display_Set.lower()]
        elif self.Display_Set == "DEFAULT":
            pass
        else:
            raise ValueError(
                f"Acceptable parameters for <Display_Set> are {', '.join(SetMap['VENUE'].keys())}"
            )

    def payloadStruct(self):
        SEP = ","
        self.payload_raw = (
            self.Buzzer_Set
            + SEP
            + self.NFC_Set
            + SEP
            + self.Bin_Level
            + SEP
            + self.UHF_Power
            + SEP
            + self.Display_Set
            + SEP
            + self.BinID_Set
            + SEP
            + self.NFC_Merch_Set
        )
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

    def awsDownlink(self, N, freq,
                    device_id="5ac752d9-a6ab-4ba0-bef5-304a0cc41c9b"):
        self.prep()
        transmit_mode = 1

        for i in range(1, N + 1):
            wireless_metadata = {
                "Sidewalk": {
                    "Seq": i,
                    "MessageType": "CUSTOM_COMMAND_ID_NOTIFY",
                    "AckModeRetryDurationSecs": 60,
                }
            }

            response = self.aws_client.send_data_to_wireless_device(
                Id=device_id,
                TransmitMode=transmit_mode,
                PayloadData=self.payload,
                WirelessMetadata=wireless_metadata,
            )

            print(f"Payload '{self.payload}' sent to device '{device_id}'")
            time.sleep(freq)
        print("\nCompleted!\n")


def load_config(config_file, routine):
    with open(config_file, "r") as f:
        config_data = json.load(f)
    return config_data.get(routine, {})


def main():
    parser = argparse.ArgumentParser(
        description="Script to prepare Downlink Payload")
    parser.add_argument(
        "--config", default="config.json", help="Path to the config file"
    )
    parser.add_argument(
        "--routine",
        default="default",
        help="Routine to use from the config file")
    args = parser.parse_args()

    config_file = args.config
    routine = args.routine

    if not os.path.isfile(config_file):
        print(f"Config file '{config_file}' not found!")
        return

    config = load_config(config_file, routine)

    dl = Downlink(
        Buzzer_Set=config.get("Buzzer_Set", "DEFAULT"),
        NFC_Set=config.get("NFC_Set", "DEFAULT"),
        Bin_Level=config.get("Bin_Level", "DEFAULT"),
        UHF_Power=config.get("UHF_Power", "DEFAULT"),
        Display_Set=config.get("Display_Set", "DEFAULT"),
        BinID_Set=config.get("BinID_Set", "DEFAULT"),
        NFC_Merch_Set=config.get("NFC_Merch_Set", "DEFAULT"),
        BOOT_MODE=config.get("BOOT_MODE", "DEFAULT"),
        SEP=config.get("SEP", "<SEP>"),
    )

    print(dl)

    if dl.BOOT_MODE.lower() == "true":
        confirmation = input(
            "BOOT_MODE is set to TRUE. Proceed with Caution. Continue? (y/n): "
        )
        if confirmation.lower() != "y":
            print("Exiting...")
            return

    dl.awsDownlink(N=config.get("N"), freq=config.get("FREQ"))


if __name__ == "__main__":
    main()
