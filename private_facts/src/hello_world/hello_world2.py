
"""
Same as hello_world.py but sending a file instead of a string.
"""
from pathlib import Path
import urllib3


# By default, the Tahoe client listens on port 3456 of the local host.
BASE_URL="http://127.0.0.1:3456/uri/"
FILEPATH=Path(__file__).parent / "hello_world.txt"

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

def upload_file(tahoe_client, data):
    """
    Upload the contents of the test string via tahoe_client and return its URI.
    """
    uri = tahoe_client.upload_data(data)
    print(uri)
    return uri


def get_string(tahoe_client, uri):
    """
    Retrieve the contents of the string by passing the uri to the tahoe_client.
    """

    retrieved_string = tahoe_client.retrieve_data(uri)

    print(retrieved_string)
    return retrieved_string



if __name__ == "__main__":
    # get_string(tahoe_client, upload_string(tahoe_client, TEST_STRING))
    upload_file(tahoe_client, FILEPATH)