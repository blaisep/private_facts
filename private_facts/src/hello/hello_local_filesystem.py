# Hello Local: save a string of personal data to a locally running Tahoe storage server using a Tahoe client, then retrieve it.
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

    def upload_data(self, data, dir_cap=None):
        if dir_cap:
            url = self.base_url + dir_cap + "/foo.txt"
        else:
            url = self.base_url
        try:
            response = http.request(
            "PUT",
            url,
            data
            )
        except Exception:
            raise
            
        if response.status != 200 and response.status != 201:
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
    
    def put_using_filecap(self, cap_string):
        """
        According to docs this only works for a writecap on a mutable file.
        """
        try:
            response = http.request(
            "PUT",
            self.base_url+cap_string,
            )
        except Exception:
            raise

        if response.status != 200:
            return None

        return response.data.decode("utf-8")

    def make_dir(self):
        try:
            response = http.request(
                "POST",
                self.base_url[:-1]+"?t=mkdir"
            )
        except Exception:
            raise

        if response.status != 200:
            return None

        return response.data.decode("utf-8")


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


def upload_string(tahoe_client, data, dir_cap=None):
    """
    Upload the contents of the test string via tahoe_client and return its capability string.
    """
    if dir_cap:
        cap_string = tahoe_client.upload_data(data, dir_cap=dir_cap)
    else:
        cap_string = tahoe_client.upload_data(data)
    breakpoint()
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

def upload_using_filecap(tahoe_client, cap_string):
    return tahoe_client.put_using_filecap(cap_string)

def main():
    try:
        tahoe_client.get_welcome()
    except Exception:
        print("Cannot access Tahoe welcome page. Are you sure the client is running?")
        sys.exit(1)
    new_dir = tahoe_client.make_dir()
    dir_string = upload_string(tahoe_client, TEST_STRING, new_dir)
    # cap_string = upload_string(tahoe_client, TEST_STRING)
    # if cap_string is None:
    #     print("No capability string retrieved; are you sure the client and storage are running and properly configured?")
    #     sys.exit(1)
    # if get_string(tahoe_client, cap_string) is None:
    #     print("Are you sure the storage is running?")
    #     sys.exit(1)


if __name__ == "__main__":
    main()
