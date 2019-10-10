FROM justb4/jmeter

LABEL maintainer "franck.chauvel@sintef.no"

WORKDIR /tests
RUN chmod 777 -R /tests

COPY ./Forms-test.jmx /tests/Forms-test.jmx

RUN ls -lR /tests
