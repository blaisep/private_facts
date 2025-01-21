
# Tahoe hello world: save and retrieve a string to a Tahoe storage server using a Tahoe client.

import sys
import urllib3

# If TEST_STRING is under a certain number of bytes, it will be encoded in the URL.
# You can test this by uploading SHORT_TEST_STRING instead of TEST_STRING to Tahoe.
SHORT_TEST_STRING = "Hello, world!"
TEST_STRING = "Hello, world! You now have data in Tahoe-lafs, encoded outside of the URL."
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
        response = http.request(
        "PUT",
        self.base_url,
        data
        )

        return response.data.decode("utf-8")

    def retrieve_data(self, uri):
        resp = http.request(
        "GET",
        self.base_url + uri
        )

        return resp.data.decode("utf-8")

tahoe_client = TahoeClient(base_url=BASE_URL)

def upload_string(tahoe_client, data):
    """
    Upload the contents of the test string via tahoe_client and return its URI.
    """
    try:
        uri = tahoe_client.upload_data(data)
        print(uri)
        return uri
    except Exception as e:
        print(f"An error occurred during upload: {e.reason}")
        return None

def get_string(tahoe_client, uri):
    """
    Retrieve the contents of the string by passing the uri to the tahoe_client.
    """

    retrieved_string = tahoe_client.retrieve_data(uri)

    print(retrieved_string)
    return retrieved_string

def main():
    uri = upload_string(tahoe_client, TEST_STRING)
    if uri is None:
        print("Upload error: are you sure the client and storage are running?")
        sys.exit(1)
    get_string(tahoe_client, uri)

if __name__ == "__main__":
    main()