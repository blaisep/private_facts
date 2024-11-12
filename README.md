# Private Facts

Private Facts is a web app to track your private info. 

[//]: # (Tahoe Logo)

[//]: # (Badges: Build status,  UV, Python version, Downloads)

#### Why private facts?

The project intends to be a demonstration of how to use [Tahoe-lafs]()  "provider independent privacy".

## Installation

### Install from source

```bash
git clone https://github.com/blaisep/private_facts.git && cd private_facts
```

### Install from (Docker) Image

TBA

### 

```bash
a bash code block
```

## Usage

### Run using a (OCI) container

```python
A Python code block
```

## Feedback

The project issue tracker is getting migrated. For now, feel free to open an issue and let us know how how to improve.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

### Set up the developer environment

Initiate Tahoe-LAFS servers (one introducer, two storage servers and a client server):

Introducer server:

```sh
.venv/bin/tahoe create-introducer --listen=tcp --port=5555 --location=tcp:localhost:5555 ./introducer
.venv/bin/tahoe -d introducer run &>/dev/null &
```

Two storage servers:

```sh
.venv/bin/tahoe create-node --introducer $(cat introducer/private/introducer.furl) --nickname storage0 --webport 6001 --location tcp:localhost:6003 --port 6003 ./storage0
.venv/bin/tahoe create-node --introducer $(cat introducer/private/introducer.furl) --nickname storage1 --webport 6101 --location tcp:localhost:6103 --port 6103 ./storage1
.venv/bin/tahoe -d storage0 run &>/dev/null &
.venv/bin/tahoe -d storage1 run &>/dev/null &
```

Client:

```sh
.venv/bin/tahoe create-client --introducer $(cat introducer/private/introducer.furl) --nickname webapp --webport 6401 --shares-total=3 --shares-needed=2 --shares-happy=3 ./webapp
.venv/bin/tahoe -d webapp run &>/dev/null &
```

The commands should return four PIDs. Note them down to kill them later, when finished, with:

```sh
kill -9 <PID>
```

### Getting ready for your first pull request

Please make sure to update tests as appropriate.

We Manage the project with [uv](https://docs.astral.sh/uv/), you don't have to.

## License

[MIT](https://choosealicense.com/licenses/mit/)

[//]: # ( This file was inspired by https://www.makeareadme.com/ )
