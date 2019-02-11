#FROM mysql:5.7
#FROM postgres:9.6.3
FROM database

#COPY init_postgres.sql docker-entrypoint-initdb.d/init_database.sql
#COPY init_mysql.sql docker-entrypoint-initdb.d/init_database.sql
COPY init_database.sql

RUN chmod 755 init_database.sql

#EXPOSE 3306 
#EXPOSE 5432
EXPOSE PORT




