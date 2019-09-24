FROM mysql:5

ENV MYSQL_DATABASE lutece

ENV MYSQL_ROOT_PASSWORD motdepasse

COPY ./sql-scripts/ /docker-entrypoint-initdb.d/
