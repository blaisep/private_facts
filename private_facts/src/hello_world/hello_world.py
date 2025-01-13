
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

def get_string():
    """
    For now, set uri to the fURL of some file you've uploaded 
    """
    # Two sample URIs:
    # uri = "URI:LIT:k5ugc5dfozsxeiijbi"
    # uri = "URI:CHK:k5a6fm7527ayjcrhblng3k6lpq:7vau4zhhuun52uibdrs6bfqhvcjwcnldt7rwm3jds3v2zthtlnhq:1:1:152225"
    resp = http.request(
    "GET",
    BASE_URL + uri
)
    return resp


def upload_string(fURL="http://127.0.0.1:3456/uri/URI%3ADIR2%3Adjrdkfawoqihigoett4g6auz6a%3Ajx5mplfpwexnoqff7y5e4zjus4lidm76dcuarpct7cckorh2dpgq/"):
    return fURL


def main(test_string=TEST_STRING):
    print(f"The contents of the test string are: {test_string}")


if __name__ == "__main__":
    main()
