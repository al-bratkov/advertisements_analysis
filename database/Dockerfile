FROM postgres:7.2

ENV POSTGRES_DB parse_avito_cars
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres

ADD cars.sql /docker-entrypoint-initdb.d
RUN echo "host all all 0.0.0.0/0 md5" >> /var/lib/postgresql/data/pg_hba.conf
RUN echo "listen_addresses='*'" >> /var/lib/postgresql/data/postgresql.conf

EXPOSE 5432
