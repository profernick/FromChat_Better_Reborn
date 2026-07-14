FROM postgres:15

RUN apt-get update && apt-get install -y gettext-base && rm -rf /var/lib/apt/lists/*

COPY sql.template /docker-entrypoint-initdb.d/init-postgres.sql.template
COPY entrypoint.sh /usr/local/bin/postgres-entrypoint.sh
RUN chmod +x /usr/local/bin/postgres-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/postgres-entrypoint.sh"]
CMD ["postgres"]
