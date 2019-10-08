FROM selenium/node-chrome-debug

RUN pip install selenium pytest

COPY ./citygo.jmx citygo-tests/citygo.jmx

CMD echo "Ready!"
