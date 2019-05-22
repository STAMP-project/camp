FROM debian:9-slim

ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 8.9.3

RUN apt-get update && apt-get install -y curl build-essential libtinfo-dev libgmp-dev zlib1g-dev python git libghc-gitrev-dev

ADD src /purescript

RUN mkdir $NVM_DIR && curl https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash && . $NVM_DIR/nvm.sh && nvm install $NODE_VERSION && nvm use --delete-prefix $NODE_VERSION && npm install --global npm@6.2.0 \
    && curl -sSL https://get.haskellstack.org/ | sh && cd /purescript && make && make test
