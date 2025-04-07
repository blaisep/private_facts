# Hello Local Filesystem: Create a Tahoe directory, save a string of personal data to it, then retrieve it.
import sys
import urllib3

from .tahoe_client import TahoeClient

# If the string passed in is under a certain number of bytes, it will be encoded in the URL rather than stored in the server.
# You can see this by passing SHORT_TEST_STRING instead of TEST_STRING; the capability string will have a LIT instead of a CHK prefix.
SHORT_TEST_STRING = "Hello, world!"
TEST_STRING = "name:Abigail, heart_rate:82, bp:110/75, flow_rate:0, temp: 36.8"
# By default, the Tahoe client listens on port 3456 of the local host.
BASE_URL="http://127.0.0.1:3456/uri/"
HTTP = urllib3.PoolManager()

tahoe_client = TahoeClient(base_url=BASE_URL, http=HTTP)

def upload_string(tahoe_client, data, dir_cap=None):
    """
    Upload the contents of the test string via tahoe_client and return its capability string.
    """
    cap_string = tahoe_client.upload_data(data, dir_cap)

    if cap_string is None:
        print(f"An error occurred during upload.")
        return None
    
    print(f"Data cap string: {cap_string}")
    return cap_string

def get_string(tahoe_client, cap_string, dir_cap=None):
    """
    Retrieve the contents of the string by passing the capability string to the tahoe_client.
    """
    retrieved_string, status = tahoe_client.retrieve_data(cap_string, dir_cap)

    if status != 200:
        print(f"An error occurred retrieving the data with error code: {status}")
        return None


    print(f"Retrieved data: {retrieved_string}")
    return retrieved_string



def create_directory(tahoe_client):
    dir_cap = tahoe_client.make_dir()
    print(f"Directory cap string: {dir_cap}")
    return dir_cap

def main():
    try:
        tahoe_client.get_welcome()
    except Exception:
        print("Cannot access Tahoe welcome page. Are you sure the client is running?")
        sys.exit(1)
    dir_cap = create_directory(tahoe_client)
    if dir_cap is None:
        print("Could not create directory.")
        sys.exit(1)
    cap_string = upload_string(tahoe_client, TEST_STRING, dir_cap)
    if cap_string is None:
        print("No capability string retrieved; are you sure the client and storage are running and properly configured?")
        sys.exit(1)
    if get_string(tahoe_client, cap_string) is None:
        print("Are you sure the storage is running?")
        sys.exit(1)


if __name__ == "__main__":
    main()
