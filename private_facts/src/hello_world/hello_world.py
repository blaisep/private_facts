
"""smallest possible session: save and retrieve some data.

    (CLI only for now)
    Send a string  to Tahoe
    receive a fURL
    retrieve string using the fURL
    print the fURL
    print the string

    Example:
    ```
        $ python -m private_facts.hello-world
        ...
        fURL=
        string = "Hello World"
    ```
"""
import urllib3

# If TEST_STRING is under a certain number of bytes, it will be encoded in the URL.
TEST_STRING = "Hello, world! You now have data in Tahoe-lafs, encoded outside of the URL."
# By default, the Tahoe client listens on port 3456 of the local host.
BASE_URL="http://127.0.0.1:3456/uri/"

http = urllib3.PoolManager()

class TahoeClient:
    def __init__(self, base_url):
        self.base_url = BASE_URL

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
    Upload the contents of the test string via the Tahoe client and return the URI.
    """
    uri = tahoe_client.upload_data(data)
    print(uri)
    return uri
    


def get_string(tahoe_client):
    """
    Retrieve and return the contents of the string uploaded by upload_string.
    """
    uri = upload_string(tahoe_client, TEST_STRING)

    retrieved_string = tahoe_client.retrieve_data(uri)

    print(retrieved_string)
    return retrieved_string

def main():
    get_string(tahoe_client)


if __name__ == "__main__":
    main()
