class TahoeClient:
    """
    The TahoeClient object makes requests to and returns responses from a locally running Tahoe client.
    """
    def __init__(self, base_url, http):
        self.base_url = base_url
        self.http = http

    def upload_data(self, data, dir_cap=None):
        if dir_cap:
            url = self.base_url + dir_cap + "/my_data.txt"
        else:
            url = self.base_url
        try:
            response = self.http.request(
            "PUT",
            url,
            data
            )
        except Exception:
            raise
            
        if response.status != 200 and response.status != 201:
            return None

        return response.data.decode("utf-8")

    def retrieve_data(self, cap_string, dir_cap=None):
        if dir_cap:
            url = self.base_url + dir_cap + "/my_data.txt"
        else:
            url = self.base_url + cap_string

        response = self.http.request(
        "GET",
        url
        )

        if response.status != 200:
            return None, response.status

        return response.data.decode("utf-8"), response.status
    
    

    def make_dir(self):
        try:
            response = self.http.request(
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
            response = self.http.request(
            "GET",
            "http://127.0.0.1:3456/?t=json"
            )
        except Exception:
            raise

        return response