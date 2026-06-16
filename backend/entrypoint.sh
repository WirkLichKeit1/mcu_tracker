#!/bin/sh
set -e

echo "Waiting for database..."

until python -c "
import os, sys
try:
    import pymysql
    from urllib.parse import urlparse
    url = urlparse(os.environ['DATABASE_URL'].replace('mysql+pymysql://', 'mysql://'))
    pymysql.connect(
        host=url.hostname,
        port=url.port or 3306,
        user=url.username,
        password=url.password,
        database=url.path.lstrip('/'),
        connect_timeout=3,
    )
    sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(1)
"; do
  echo "Database not ready, retrying in 3s..."
  sleep 3
done

echo "Database is up!"

echo "Running migrations..."
alembic upgrade head

echo "Running seed..."
python -m app.seed

if [ "${ENV}" = "development" ]; then
  exec uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
else
  exec uvicorn app.main:app --host 0.0.0.0 --port 8080
fi