#! python3

""" 
# azure_io_test_files_client.py
# Usage:
#     py azure_io_test_files_client.py <source_disk> <test_file_size>
#
# simple script to test Azure Files IO speed depends on 
#     windows
#     python 3.6 or later
#     Python liabrary: azure-storage-file-share
"""

from azure.storage.fileshare import ShareServiceClient, ShareClient, ShareFileClient
import os, subprocess, sys, time

os.environ["PYTHONDONTWRITEBYTECODE"] = "1" 
os.environ["PYTHONUNBUFFERED"] = "1" 

def run_cmd(mycmd, verbose=True):
    """
    # simple wrapper to run a system command
    """
    if verbose :
        print(mycmd)
    rc = subprocess.call(mycmd, shell=True)
    return rc

def test_azure_files_ingress(conn_str, share_name, source_disk, file_to_upload):
    time_start = time.time()

    file_client = ShareFileClient.from_connection_string(conn_str, share_name, file_to_upload)

    with open(f"{source_disk}\\{file_to_upload}", "rb") as source_file:
        file_client.upload_file(source_file)

    dt = time.time() - time_start
    speed = (1.0 * fsize_b / dt) / mb  # in MBytes/sec
    print(f"Ingress speed: {speed:.2f} MBytes/sec")

print("START")

source_disk = sys.argv[1]
fsize_mb    = int(sys.argv[2])

myfile = "io_test.img"

mb       = 1024*1024
fsize_b  = fsize_mb * mb # Bytes

print(f"creating temporary file {myfile} of size {fsize_mb} MBytes")
mystr   = "0123456789ABCDEF" * 65535 + "0123456789ABCDE\n" # 1MB

fh = open(f"{source_disk}\\{myfile}", "w")
for ii in range(fsize_mb):
    fh.write(mystr)
fh.close()

# Azure Files standard
connection_string_standard = "<replace with your connection string for Azure Files standard>"

# Azure Files standard - large file enabled
connection_string_standard_large = "<replace with your connection string for Azure Files standard with large file enabled>"

# Azure Files premium
connection_string_premium = "<replace with your connection string for Azure Files premium>"

share_name_standard = "io-test"
share_name_standard_large = "io-test-10"
share_name_premium = "io-test-premium"
share_name_premium_large = "io-test-premium-10"

print("starting the test - Azure Files standard")
test_azure_files_ingress(connection_string_standard, share_name_standard, source_disk, myfile)

print("starting the test - Azure Files standard with large quota")
test_azure_files_ingress(connection_string_standard_large, share_name_standard_large, source_disk, myfile)

print("starting the test - Azure Files premium")
test_azure_files_ingress(connection_string_premium, share_name_premium, source_disk, myfile)

print("starting the test - Azure Files premium with large quota")
test_azure_files_ingress(connection_string_premium, share_name_premium_large, source_disk, myfile)

print("removing temporary files")
if os.path.isfile(f"{source_disk}\\{myfile}"):
    os.remove(f"{source_disk}\\{myfile}")

print('DONE')