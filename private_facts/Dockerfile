FROM python:3.11-bookworm
EXPOSE 80
EXPOSE 3456

RUN pip install attrs==23.2.0 "cryptography<42" tahoe-lafs
    # workaround https://tahoe-lafs.org/trac/tahoe-lafs/ticket/4102

RUN echo "1. The current directory is $(pwd)"
RUN echo "Finished installing tahoe"
# for now, build a new client in the container
RUN tahoe --node-directory=client0 create-client \
    --shares-happy=1 \
    --shares-needed=1 \
    --shares-total=1 \
    --nickname=client0
RUN echo "initial tahoe run"

ENTRYPOINT ["tahoe", "run", "client0/"]

# TODO: If the client config does not exist, then create it.


# Build an image: tahoe-lafs-dev for local deployment
# First build the image with `podman image build -t tahoe-lafs-dev . `
# Then use the image to run a container with:
#