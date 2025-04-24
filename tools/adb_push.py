from adb_shell.adb_device import AdbDeviceUsb
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.auth.keygen import keygen
from util import ensure_directory
from pathlib import Path
import os

ARG_PARSER = {
    "prog": "adb_push",
    "description": "Push files to an android phone using adb",
    "help": "Push files to an android phone using adb"
}
ARGS = {
    "-i;--input": {
        "help": "Input directory",
        "required": True},
    "-o;--output": {
        "help": "Output directory on the phone. Assumes root path if no /"
                " prefix",
        "required": True},
}

ADBKEY_DIR = "data/adbkeys/"
ADBKEY_NAME = "keys"


def progress_callback(device_path, bytes_written, total_bytes):
    print(f"pushing {device_path} {bytes_written}/{total_bytes}")


def run(args):
    ensure_directory(ADBKEY_DIR)

    adb_pv_key = ADBKEY_DIR+ADBKEY_NAME
    adb_pb_key = ADBKEY_DIR+ADBKEY_NAME+".pub"
    if not (os.path.exists(adb_pv_key)
            and os.path.exists(adb_pb_key)):
        if os.path.exists(adb_pv_key):
            os.remove(adb_pv_key)
        if os.path.exists(adb_pb_key):
            os.remove(adb_pb_key)

        keygen(ADBKEY_DIR+ADBKEY_NAME)

    with open(adb_pv_key) as f:
        priv = f.read()
    with open(adb_pb_key) as f:
        pub = f.read()

    signer = PythonRSASigner(pub, priv)

    device = AdbDeviceUsb()
    device.connect(rsa_keys=[signer])

    input_dir_path = Path(args.input)
    output_dir_path = Path((
        '' if args.output.startswith('/') else '/') + args.output)
    input_files = [str(x) for x in input_dir_path.glob("./**") if x.is_file()]
    output_files = [str(output_dir_path / str(
        x).removeprefix(str(input_dir_path)+'/')) for x in input_files]

    for i in range(len(input_files)):
        device.push(input_files[i], output_files[i],
                    progress_callback=progress_callback)

    device.close()
