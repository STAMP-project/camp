FROM debian:9-slim

ENV NODE_VERSION 8.9.3
ENV DISPLAY :99.0
ENV CC clang-3.8
ENV CXX clang++-3.8
ENV npm_config_clang 1
ENV ATOM_JASMINE_REPORTER list
RUN mkdir /usr/local/nvm && chmod 755 /usr/local/nvm
ENV NVM_DIR /usr/local/nvm

RUN apt-get update && apt-get install -y curl build-essential clang-3.8 gconf2 libnotify4 xvfb gvfs-bin xdg-utils libgtk-3-dev libgconf-2-4 libasound2 libx11-xcb-dev libxss1 python git libsecret-1-dev fakeroot rpm libx11-dev libxkbfile-dev

RUN curl https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash && . $NVM_DIR/nvm.sh && nvm install $NODE_VERSION && nvm use --delete-prefix $NODE_VERSION && npm install --global npm@6.2.0 \
    && cd /root && mkdir github && cd /root/github && git clone https://github.com/atom/atom.git && chmod -R 755 /root/github/atom \
    && cd /root/github/atom/script && ./bootstrap \
    && cd /root/github/atom/script && ./build --no-bootstrap \
    && Xvfb :99 -ac -screen 0 1280x1024x16 && cd /root/github/atom/script && ./test
