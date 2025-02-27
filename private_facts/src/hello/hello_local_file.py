# Hello Local File: save an input txt file of personal data to a locally running Tahoe storage server using a Tahoe client,
# then retrieve the contents and write them to an output txt file.
from pathlib import Path
import sys
import urllib3
from urllib3.filepost import encode_multipart_formdata


# By default, the Tahoe client listens on port 3456 of the local host.
BASE_URL="http://127.0.0.1:3456/uri/"
# FILEPATH points to hello_world_in.txt, which contains the same string used in the hello_local module.
FILEPATH = Path("./private_facts/src/hello/hello_world_in.txt")
OUTPUT_FILEPATH = Path("./private_facts/src/hello/hello_world_out.txt")
http = urllib3.PoolManager()

class TahoeClient:
    """
    The TahoeClient object makes requests to and returns responses from a locally running Tahoe client.
    """
    def __init__(self, base_url):
        self.base_url = base_url


    def upload_file(self, file_path):
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
            fields = {
                "file": (file_path.name, file_data, "application/octet-stream")
            }
            body, content_type = encode_multipart_formdata(fields)
            headers = {"Content-Type": content_type}
            response = http.request("PUT", self.base_url, body=body, headers=headers)

        except Exception as e:
            raise RuntimeError(f"Upload failed: {e}")

        if response.status != 200:
            return None

        return response.data.decode("utf-8")


    def retrieve_data(self, cap_string):
        response = http.request(
        "GET",
        self.base_url + cap_string
        )

        if response.status != 200:
            return None, response.status

        return response.data.decode("utf-8"), response.status
    
    def get_welcome(self):
        """
        Get the Tahoe Welcome page in json format. Inspired by meejah's magic folder tahoe client: https://github.com/tahoe-lafs/magic-folder/blob/main/src/magic_folder/tahoe_client.py
        """
        try:
            response = http.request(
            "GET",
            "http://127.0.0.1:3456/?t=json"
            )
        except Exception:
            raise

        return response

tahoe_client = TahoeClient(base_url=BASE_URL)


def upload_file(tahoe_client, file_path):
    """
    Upload the input file via tahoe_client and return its capability string.
    """
    try:
        cap_string = tahoe_client.upload_file(file_path)

        if cap_string is None:
            print(f"An error occurred during upload.")
            return None

        print(cap_string)
        return cap_string

    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_file(tahoe_client, cap_string, output_path):
    """
    Retrieve the contents of a file by passing the capability string to the tahoe_client and write them to output_path.
    """
    retrieved_data, status = tahoe_client.retrieve_data(cap_string)

    if status != 200:
        print(f"An error occurred retrieving the data with error code: {status}")
        return None

    # Separate the data from the metadata
    retrieved_data = retrieved_data.split("\n")[4]
    print(retrieved_data)

    try:
        with open(output_path, "w") as f:
            f.write(retrieved_data)
        print(f"Data written to {OUTPUT_FILEPATH}.")
    except Exception as e:
        print(f"Error writing data to {OUTPUT_FILEPATH}.")

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
