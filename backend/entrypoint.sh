#!/bin/sh
set -e

echo "Waiting for MySQL..."

until python -c "
import pymysql, sys
try:
    pymysql.connect(
        host='db',
        user='${MYSQL_USER}',
        password='${MYSQL_PASSWORD}',
        database='${MYSQL_DATABASE}',
        connect_timeout=3,
    )
    sys.exit(0)
except Exception:
    sys.exit(1)
"; do
    echo "MySQL not ready, retrying in 3s..."
    sleep 3
done

echo "MySQL is UP!"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload