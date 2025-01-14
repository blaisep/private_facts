
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

TEST_STRING = "Hello, world!"
BASE_URL="http://127.0.0.1:3456/uri/"

http = urllib3.PoolManager()

def get_string(uri=""):
    """
    Retrieve the contents of the string uploaded by upload_string
    """
    # Two sample URIs:
    # uri = "URI:LIT:k5ugc5dfozsxeiijbi"
    # uri = "URI:CHK:k5a6fm7527ayjcrhblng3k6lpq:7vau4zhhuun52uibdrs6bfqhvcjwcnldt7rwm3jds3v2zthtlnhq:1:1:152225"
    uri = upload_string().data.decode("utf-8")
    resp = http.request(
    "GET",
    BASE_URL + uri
)
    return resp.data.decode("utf-8")


def upload_string():
    """
    Upload the contents of the test string via the Tahoe client.
    """
    resp = http.request(
    "PUT",
    BASE_URL,
    TEST_STRING
)

    return resp


def main():
    print(get_string())


if __name__ == "__main__":
    main()