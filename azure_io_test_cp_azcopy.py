#! python

""" 
# azure_io_test_cp_azcopy.py
# Usage:
#     py azure_io_test_cp_azcopy.py <source_path> <destination_path> <copy_method> <test_file_name> <test_file_size> <repeat_times>
#
# simple script to test Azure Files IO speed depends on 
#     windows
#     python 3.6 or later
# script runs windows commands:
#     copy /Y <source_file_ path> <destination_file_path> 
# or
#     azcopy cp "<source_file_share>" "<source_file_share>" --recursive --force-if-read-only
"""

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

def get_path_and_location(user_input):
    """
    # parse the user input and return the path and file location of source or destination
    """
    root = user_input.split("\\")[0]
    if len(user_input.split("\\")) > 1:
        sub_folder = user_input.split ("\\")[1]
    if root in ["C:", "D:", "F:", "G:", "U:", "V:", "X:", "Y:"]:
        output_path = file_location = f"{user_input}\\{sname}"
    else:
        output_path = f"{azcopy_url_dict[root]}/{user_input}/{sname}{sas_dict[root]}"
        file_location = f"{disk_label_dict[root]}\\{sub_folder}\\{sname}"
    return output_path, file_location

print("START")

source      = sys.argv[1]
destination = sys.argv[2]
method      = sys.argv[3]
sname       = sys.argv[4]
fsize_mb    = int(sys.argv[5])
N           = int(sys.argv[6])

disk_label_dict = {
    "io-test" : "X:",
    "io-test-10" : "Y:",
    "io-test-premium" : "U:",
    "io-test-premium-10" : "V:"
    }

sas_dict = {
    "io-test" : "<replace with your SAS token for io-test>",
    "io-test-10" : "<replace with your SAS token for io-test-10>",
    "io-test-premium" : "<replace with your SAS token for io-test-premium>",
    "io-test-premium-10" : "<replace with your SAS token for io-test-premium-10>"
    }

azcopy_url_dict = {
    "io-test" : "<replace with your Azure Files url for io-test>",
    "io-test-10" : "<replace with your Azure Files url for io-test-10>",
    "io-test-premium" : "<replace with your Azure Files url for io-test-premium>",
    "io-test-premium-10" : "<replace with your Azure Files url for io-test-premium-10>",
    }

mb       = 1024*1024
fsize_b  = fsize_mb * mb # Bytes

# string 1 MBytes
mystr = "0123456789ABCDEF" * 65535 + "0123456789ABCDE\n" # 1MB

source_path, source_file_location = get_path_and_location(source)
destination_path, dest_file_location = get_path_and_location(destination)

print(f"Creating temporary file {sname} of size {fsize_mb} MBytes")

fh = open(source_file_location, "w")
for ii in range(fsize_mb):
    fh.write(mystr)
fh.close()

print(f"Starting the test using the {method} command")

print(f"Source: {source_path}")
print(f"Mount location: {source_file_location}")
print(f"Destination: {destination_path}")
print(f"Mount location: {dest_file_location}")

if method == "copy":
    mycmd = f"copy /Y {source_path} {destination_path}"
elif method == "azcopy":
    mycmd = f"azcopy cp \"{source_path}\" \"{destination_path}\" --recursive --force-if-read-only"

time_start = time.time()

for ii in range(1,N+1):
    run_cmd(mycmd)
    dt = time.time() - time_start
    speed = (1.0 * ii * fsize_b / dt) / mb  # in MBytes/sec
    print(f"({ii:2d} of {N:2d}) average {speed:.2f} MBytes/sec")
    
print("Removing temporary files")
for fname in [source_file_location, dest_file_location]:
    if os.path.isfile(fname):
        os.remove(fname)

print('DONE')