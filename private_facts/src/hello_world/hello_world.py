
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

TEST_STRING = "Hello, world! You now have data in Tahoe-lafs."
# By default, the Tahoe client listens on port 3456 of the local host.
BASE_URL="http://127.0.0.1:3456/uri/"

http = urllib3.PoolManager()


def upload_string():
    """
    Upload the contents of the test string via the Tahoe client and return fURL.
    """
    resp = http.request(
    "PUT",
    BASE_URL,
    TEST_STRING
)

    furl = resp.data.decode("utf-8")
    print(furl)
    return furl


def get_string(uri=""):
    """
    Retrieve and return the contents of the string uploaded by upload_string.
    """
    uri = upload_string()

    resp = http.request(
    "GET",
    BASE_URL + uri
)

    retrieved_str = resp.data.decode("utf-8")
    print(retrieved_str)
    return retrieved_str

def main():
    get_string()


if __name__ == "__main__":
    main()