# Private facts hello world: save a string of personal data to a locally running Tahoe storage server using a Tahoe client, then retrieve it.

import sys
import urllib3


# If the string passed in is under a certain number of bytes, it will be encoded in the URL rather than stored in the server.
# You can see this by passing SHORT_TEST_STRING instead of TEST_STRING; the capability string will have a LIT instead of a CHK prefix.
SHORT_TEST_STRING = "Hello, world!"
TEST_STRING = "name:Abigail, heart_rate:82, bp:110/75, flow_rate:0, temp: 36.8"

# By default, the Tahoe client listens on port 3456 of the local host.
BASE_URL="http://127.0.0.1:3456/uri/"

http = urllib3.PoolManager()

class TahoeClient:
    """
    The TahoeClient object makes requests to and returns responses from a locally running Tahoe client.
    """
    def __init__(self, base_url):
        self.base_url = base_url

    def upload_data(self, data):
        try:
            response = http.request(
            "PUT",
            self.base_url,
            data
            )
        except Exception:
            raise

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


def upload_string(tahoe_client, data):
    """
    Upload the contents of the test string via tahoe_client and return its capability string.
    """
    
    cap_string = tahoe_client.upload_data(data)
    if cap_string is None:
        print(f"An error occurred during upload.")
        return None
    
    print(cap_string)
    return cap_string

def get_string(tahoe_client, cap_string):
    """
    Retrieve the contents of the string by passing the capability string to the tahoe_client.
    """

    retrieved_string, status = tahoe_client.retrieve_data(cap_string)


    if status != 200:
        print(f"An error occurred retrieving the data with error code: {status}")
        return None


    print(retrieved_string)
    return retrieved_string


def main():
    try:
        tahoe_client.get_welcome()
    except Exception:
        print("Cannot access Tahoe welcome page. Are you sure the client is running?")
        sys.exit(1)
    cap_string = upload_string(tahoe_client, TEST_STRING)
    if cap_string is None:
        print("Are you sure the client and storage are running and properly configured?")
        sys.exit(1)
    if get_string(tahoe_client, cap_string) is None:
        print("Are you sure the storage is running?")
        sys.exit(1)


if __name__ == "__main__":
    main()
