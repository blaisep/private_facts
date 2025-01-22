
# Tahoe hello world: save a string to a locally running Tahoe storage server using a Tahoe client, then retrieve it.

import ipdb
import json
import sys
import urllib3


# If the string passed in is under a certain number of bytes, it will be encoded in the URL
SHORT_TEST_STRING = "Hello, world!"
TEST_STRING = "Hello, world! You now have data in Tahoe-lafs, but only in your client, not yet on any grid."

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

    def retrieve_data(self, uri):
        response = http.request(
        "GET",
        self.base_url + uri
        )

        if response.status != 200:
            return None, response.status

        return response.data.decode("utf-8"), response.status
    
    def get_welcome(self):
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
    Upload the contents of the test string via tahoe_client and return its URI.
    """
    
    # try:
    uri = tahoe_client.upload_data(data)
    if uri is None:
        print(f"An error occurred during upload.")
        return None
    
    print(uri)
    return uri

def get_string(tahoe_client, uri):
    """
    Retrieve the contents of the string by passing the uri to the tahoe_client.
    """

    retrieved_string, status = tahoe_client.retrieve_data(uri)

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
    uri = upload_string(tahoe_client, TEST_STRING)
    if uri is None:
        print("Are you sure the client and storage are running and properly configured?")
        sys.exit(1)
    if get_string(tahoe_client, uri) is None:
        print("Are you sure the storage is running?")
        sys.exit(1)


if __name__ == "__main__":
    main()
