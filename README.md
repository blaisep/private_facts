## Note:
Development of Private Facts has moved to a [new repo](https://github.com/private-facts/private-facts). This one is kept up for historical interest only.

# Private Facts

Private Facts is a web app to track your private info. 

[//]: # (Tahoe Logo)

[//]: # (Badges: Build status,  UV, Python version, Downloads)

#### Why private facts?

This repo holds the source code and resource files for the project described at [private-facts.readthedocs.io](https://private-facts.readthedocs.io/en/latest/index.html)
The code intends to be a demonstration of how to use [Tahoe-lafs](https://tahoe-lafs.readthedocs.io/en/latest/about-tahoe.html#what-is-tahoe-lafs) and better
understand the concept of "provider-independent privacy" as it pertains to Tahoe-lafs.

## How to use this repo

There are several ways you can use this repo:
- as a companion to the tutorials at [private-facts.readthedocs.io](https://private-facts.readthedocs.io/en/latest/tutorials/index.html)
- as the starting point for a project of your own
- as a practical guide to setting up a local development instance of Tahoe-lafs

We encourage you to read through the docs first and get an overall sense of the narrative arc. 
Later, if you want the hands-on experience, clone the repo and go through the instructions.

## Installation

If you have never created a dev environment for Tahoe-lafs, do not follow these instructions before completing the tutorial. 
These instructions assume you know how the various subsystems work. If you follow the tutorials, we expect you to arrive 
at your destination qith fewer delays.

### Install from source

```bash
git clone https://github.com/blaisep/private_facts.git && cd private_facts
```

#### Install dependencies.

```sh
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml
```

#### Setup a storage grid:

```sh
grid-manager --config ./gm0 create
```

Initiate Tahoe-LAFS servers (one introducer, two storage servers and a client server, each in a separate terminal window):

#### Setup the introducer server:

```sh
.venv/bin/tahoe create-introducer \
--listen=tcp --port=6001 \
--location=tcp:localhost:6001 ./introducer \
.venv/bin/tahoe -d introducer run
```

#### Two storage servers, the first you will call `storage0`:

```sh
$ .venv/bin/tahoe create-node --introducer $(cat introducer/private/introducer.furl) \
--nickname storage0 \
--webport 6101 -\
-location tcp:localhost:6102 \
--port 6102 \
./storage0
```

The second you will call `storage1`, notice that the traffic is running on a different TCP port:

```
$ .venv/bin/tahoe create-node --introducer $(cat introducer/private/introducer.furl) \
--nickname storage1 \
--webport 6201 \
--location tcp:localhost:6202 \
--port 6202 ./storage1
```

Now, start each of the two storage servers. Pro tip: run them in separate terminal windows so that you can easily see the console output.
```
$ .venv/bin/tahoe -d storage0 run
$ .venv/bin/tahoe -d storage1 run
```

Add the storage servers to the local grid and create certificates:

```sh
$ grid-manager --config ./gm0 add storage1 $(cat storage1/node.pubkey)
$ grid-manager --config ./gm0 sign storage0 > ./storage0/gridmanager.cert 30
$ grid-manager --config ./gm0 sign storage1 > ./storage1/gridmanager.cert 30
$ grid-manager --config ./gm0 add storage0 $(cat storage0/node.pubkey)
```

Edit storage servers to make them announce their certificates to the grid. 
Edit the `tahoe.cfg` file in `storage0` and `storage1` to include these changes:

```sh
[storage]
grid_management = true

[grid_manager_certificates]
default = gridmanager.cert
```

Now, re-start storage servers.

#### Create and configure the Tahoe-lafs client:

```sh
$ .venv/bin/tahoe create-client --introducer $(cat introducer/private/introducer.furl) \
--nickname webapp --webport 6301 \
--shares-total=3 \
--shares-needed=2 \
--shares-happy=3 \
./webapp

$ .venv/bin/tahoe -d webapp run
```

### Preparing SvelteKit

To work with the TypeScript implmentation, install SvelteKit

#### Requirements

- NodeJs > 20.0
- Pnpm

#### Install dependencies and run:

```sh
cd packages
pnpm install
pnpm dev --open
```


## Feedback

The project issue tracker is getting migrated. For now, feel free to open an issue and let us know how to improve.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

### Getting ready for your first pull request

Please make sure to update tests as appropriate.

We manage the project with [uv](https://docs.astral.sh/uv/), you don't have to.

## License

[GNU General Public License v3](https://choosealicense.com/licenses/gpl-3.0/)
[//]: # ( This file was inspired by https://www.makeareadme.com/ )
