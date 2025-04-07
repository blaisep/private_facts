# Hello Local: save a string of personal data to a locally running Tahoe storage server using a Tahoe client, then retrieve it.
import sys
import urllib3

from tahoe_client import TahoeClient

# If the string passed in is under a certain number of bytes, it will be encoded in the URL rather than stored in the server.
# You can see this by passing SHORT_TEST_STRING instead of TEST_STRING; the capability string will have a LIT instead of a CHK prefix.
SHORT_TEST_STRING = "Hello, world!"
TEST_STRING = "name:Abigail, heart_rate:82, bp:110/75, flow_rate:0, temp: 36.8"
# By default, the Tahoe client listens on port 3456 of the local host.
BASE_URL="http://127.0.0.1:3456/uri/"
HTTP = urllib3.PoolManager()

tahoe_client = TahoeClient(base_url=BASE_URL, http=HTTP)


def upload_string(tahoe_client, data):
    """
    Upload the contents of the test string via tahoe_client and return its capability string.
    """

    cap_string = tahoe_client.upload_data(data)
    if cap_string is None:
        print(f"An error occurred during upload.")
        return None
    
    print(f"Capability string: {cap_string}")
    return cap_string

def get_string(tahoe_client, cap_string):
    """
    Retrieve the contents of the string by passing the capability string to the tahoe_client.
    """

    retrieved_string, status = tahoe_client.retrieve_data(cap_string)

    if status != 200:
        print(f"An error occurred retrieving the data with error code: {status}")
        return None


    print(f"Retrieved data: {retrieved_string}")
    return retrieved_string


def main():
    try:
        tahoe_client.get_welcome()
    except Exception:
        print("Cannot access Tahoe welcome page. Are you sure the client is running?")
        sys.exit(1)
    print("Welcome to Private Facts! (powered by Tahoe-LAFS)\n")
    cap_string = upload_string(tahoe_client, TEST_STRING)
    if cap_string is None:
        print("No capability string retrieved; are you sure the client and storage are running and properly configured?")
        sys.exit(1)
    if get_string(tahoe_client, cap_string) is None:
        print("Are you sure the storage is running?")
        sys.exit(1)
    print("\nCongratulations! You just stored and retrieved your first data using Private Facts!")


if __name__ == "__main__":
    main()
