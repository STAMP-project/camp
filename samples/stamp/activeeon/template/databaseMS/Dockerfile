FROM database

COPY init_database.sql

RUN chmod 755 /docker-entrypoint-initdb.d/init_database.sql

EXPOSE PORT




