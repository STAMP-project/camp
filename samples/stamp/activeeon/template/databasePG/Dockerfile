FROM postgres:9.6.3

COPY init_postgres.sql docker-entrypoint-initdb.d/init_database.sql

RUN chmod 755 /docker-entrypoint-initdb.d/init_database.sql

EXPOSE 5432
