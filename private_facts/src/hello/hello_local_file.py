# Hello Local File: save an input txt file of personal data to a locally running Tahoe storage server using a Tahoe client,
# then retrieve the contents and write them to an output txt file.
from pathlib import Path
import sys
import urllib3

from .tahoe_client import TahoeClient

# By default, the Tahoe client listens on port 3456 of the local host.
BASE_URL="http://127.0.0.1:3456/uri/"
# FILEPATH points to hello_world_in.txt, which contains the same string used in the hello_local module.
FILEPATH = Path("./private_facts/src/hello/hello_world_in.txt")
OUTPUT_FILEPATH = Path("./private_facts/src/hello/hello_world_out.txt")
HTTP = urllib3.PoolManager()

tahoe_client = TahoeClient(base_url=BASE_URL, http=HTTP)

def upload_file(tahoe_client, file_path):
    """
    Upload the input file via tahoe_client and return its capability string.
    """
    try:
        with open(file_path, "rb") as f: 
            cap_string = tahoe_client.upload_data(f)

        if cap_string is None:
            print(f"An error occurred during upload.")
            return None

        print(f"Capability string: {cap_string}")
        return cap_string

    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

    except Exception as e:
        print(f"An error occurred during upload: {e}")
        return None

def get_file(tahoe_client, cap_string, output_path):
    """
    Retrieve the contents of a file by passing the capability string to the tahoe_client and write them to output_path.
    """
    retrieved_data, status = tahoe_client.retrieve_data(cap_string)

    if status != 200:
        print(f"An error occurred retrieving the data with error code: {status}")
        return None

    print(f"Retrieved data: {retrieved_data}")

    try:
        with open(output_path, "w") as f:
            f.write(retrieved_data)
        print(f"Data written to {OUTPUT_FILEPATH}.")
    except Exception as e:
        print(f"Error writing data to {OUTPUT_FILEPATH}: {e}.")

    return retrieved_data


def main():
    try:
        tahoe_client.get_welcome()
    except Exception:
        print("Cannot access Tahoe welcome page. Are you sure the client is running?")
        sys.exit(1)
    cap_string = upload_file(tahoe_client, FILEPATH)
    if cap_string is None:
        print("No capability string retrieved; are you sure the client and storage are running and properly configured?")
        sys.exit(1)
    if get_file(tahoe_client, cap_string, OUTPUT_FILEPATH) is None:
        print("Are you sure the storage is running?")
        sys.exit(1)


if __name__ == "__main__":
    main()
