FROM node:6-jessie-slim

RUN apt-get update && apt-get install -y build-essential libgtk-3-dev libx11-xcb-dev libxss1 python git libsecret-1-dev fakeroot rpm libx11-dev libxkbfile-dev

RUN git clone https://github.com/atom/atom.git

RUN chmod -R 755 /atom

RUN cd /atom/script && ./bootstrap

RUN cd /atom/script && ./build

ENV ATOM_DEV_RESOURCE_PATH /atom

RUN atom --test spec && ls -la
