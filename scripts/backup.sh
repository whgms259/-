#!/bin/bash

# Load environment variables from .env file
if [ -f ./.env ]; then
  export $(cat ./.env | grep -v '#' | awk '/=/ {print $1}')
fi

# Database credentials (from .env)
DB_USER=${POSTGRES_USER}
DB_NAME=${POSTGRES_DB}
DB_HOST=${DB_HOST:-db} # 'db' is the service name in docker-compose.yml
DB_PORT=${DB_PORT:-5432}
DB_PASSWORD=${POSTGRES_PASSWORD}

# Backup directory
BACKUP_DIR="/app/backups" # This will be mounted to a volume

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Backup filename
TIMESTAMP=$(date +%Y%m%d%H%M%S)
BACKUP_FILE="$BACKUP_DIR/$DB_NAME-$TIMESTAMP.sql"

echo "Starting PostgreSQL database backup for $DB_NAME..."

# Perform the backup using pg_dump
PGPASSWORD=$DB_PASSWORD pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -F p -d $DB_NAME > $BACKUP_FILE

if [ $? -eq 0 ]; then
  echo "Backup successful: $BACKUP_FILE"
else
  echo "Backup failed!"
  exit 1
fi

# Optional: Clean up old backups (e.g., keep last 7 days)
# find $BACKUP_DIR -type f -name "*.sql" -mtime +7 -delete

echo "Database backup completed."
