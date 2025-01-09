
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
TEST_STRING = "Hello, world!"

def upload_string(fURL="http://127.0.0.1:3456/uri/URI%3ADIR2%3Adjrdkfawoqihigoett4g6auz6a%3Ajx5mplfpwexnoqff7y5e4zjus4lidm76dcuarpct7cckorh2dpgq/"):
    return fURL

def main(test_string=TEST_STRING):
    print(f"The contents of the test string are: {test_string}")

if __name__ == "__main__":
    main()
