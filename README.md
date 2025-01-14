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

Install dependencies.

```sh
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml
```

Setup a grid:

```sh
grid-manager --config ./gm0 create
```

Initiate Tahoe-LAFS servers (one introducer, two storage servers and a client server, each in a separate terminal window):

Introducer server:

```sh
.venv/bin/tahoe create-introducer --listen=tcp --port=6001 --location=tcp:localhost:6001 ./introducer
.venv/bin/tahoe -d introducer run
```

Two storage servers:

```sh
.venv/bin/tahoe create-node --introducer $(cat introducer/private/introducer.furl) --nickname storage0 --webport 6101 --location tcp:localhost:6102 --port 6102 ./storage0
.venv/bin/tahoe create-node --introducer $(cat introducer/private/introducer.furl) --nickname storage1 --webport 6201 --location tcp:localhost:6202 --port 6202 ./storage1
.venv/bin/tahoe -d storage0 run
.venv/bin/tahoe -d storage1 run
```

Add storage servers to grid and create certificates:

```sh
grid-manager --config ./gm0 add storage0 $(cat storage0/node.pubkey)
grid-manager --config ./gm0 add storage1 $(cat storage1/node.pubkey)
grid-manager --config ./gm0 sign storage0 > ./storage0/gridmanager.cert 30
grid-manager --config ./gm0 sign storage1 > ./storage1/gridmanager.cert 30
```

Edit storage servers to make them announce their certificates to the grid. Edit the `tahoe.cfg` file in `storage0` and `storage1`:

```sh
[storage]
grid_management = true

[grid_manager_certificates]
default = gridmanager.cert
```

Re-start storage servers.

Client:

```sh
.venv/bin/tahoe create-client --introducer $(cat introducer/private/introducer.furl) --nickname webapp --webport 6301 --shares-total=3 --shares-needed=2 --shares-happy=3 ./webapp
.venv/bin/tahoe -d webapp run
```

### Install from (Docker) Image

TBA

### 

```bash
a bash code block
```

### SvelteKit

Requirements

- NodeJs > 20.0
- Pnpm

Install dependencies and run:

```sh
cd packages
pnpm install
pnpm dev --open
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

### Getting ready for your first pull request

Please make sure to update tests as appropriate.

We manage the project with [uv](https://docs.astral.sh/uv/), you don't have to.

## License

[GNU General Public License v3](https://choosealicense.com/licenses/gpl-3.0/)
[//]: # ( This file was inspired by https://www.makeareadme.com/ )
