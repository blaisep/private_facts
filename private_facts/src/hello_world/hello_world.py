
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

def main():
    print(f"The contents of the test string are: {TEST_STRING}")

if __name__ == "__main__":
    main()
