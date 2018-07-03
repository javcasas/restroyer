FROM postgres:10.5-alpine

RUN apk update && apk upgrade &&  apk add --no-cache git openssh make && \
    cd ~ && git clone https://github.com/michelp/pgjwt.git && \
    cd pgjwt && make install && \
    apk del git openssh make
