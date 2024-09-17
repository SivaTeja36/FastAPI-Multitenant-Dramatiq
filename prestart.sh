# prestart.sh

echo "Waiting for postgres connection"

while ! nc -z postgres 5432; do
    sleep 0.1
done

echo "PostgreSQL started"
alembic upgrade head
exec "$@"