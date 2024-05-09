# jatan pandya
# script to parse

import sys,base64, codecs, struct

def hex_to_dict(hex_string):
    struct_format = "<2s 3s 4s 6s B 13s 2s B"
    hex_bytes = bytes.fromhex(hex_string)
    unpacked_data = struct.unpack(struct_format, hex_bytes)
    keys = ["header", "data_id", "time", "bin_id", "event_id", "data", "crc", "footer"]
    hex_dict = dict(zip(keys, unpacked_data)) # type: ignore
    hex_dict = {k: v.decode('ascii') if isinstance(v, bytes) else v for k, v in hex_dict.items()}
    return hex_dict



mqtt = {"PayloadData":"MDAwMDAwMDAxYjUyNzQwMjE2NTQzMzRhNGQ0ZDU2MDMzMDMwMzkzMTQ1NDIzMjM5MzkzNzM2MzM0MjAwMDAwMA==",
        "Seq":"886"}


payload = str("MDAwMDAwMDAxYjUyNzQwMjE2NTQzMzRhNGQ0ZDU2MDMzMDMwMzkzMTQ1NDIzMjM5MzkzNzM2MzM0MjAwMDAwMA==")
decoded = base64.b64decode(payload.encode('utf-8')).decode('utf-8')
print(decoded)
hex2dict = hex_to_dict(decoded)


# print(hex2dict)


# STRUCT
"""
og data: U3000E2806890000050091EB299763B14
64 payload: MDAwMDAwMDAxYjUyNzQwMjE2NTQzMzRhNGQ0ZDU2MDMzMDMwMzkzMTQ1NDIzMjM5MzkzNzM2MzM0MjAwMDAwMA==
decoded: 000000001b5274021654334a4d4d560330303931454232393937363342000000 (HEX)
decoded to ascii: tT3JMMV0091EB299763B


data struct:
typedef struct turn_data{
    uint8_t header[2];
    uint8_t data_id[3];
    uint8_t time[4];
    uint8_t bin_id[6];
    uint8_t event_id;
    char data[13];
    uint8_t crc[2];
    uint8_t footer;
}

0000
00001b
52740216
54334a4d4d56
03
30303931454232393937363342
0000
00


Bin ID: T3JMMV
"""

hex_string = "000000001b5274021654334a4d4d560330303931454232393937363342000000"
hex_bytes = bytes.fromhex(hex_string)
