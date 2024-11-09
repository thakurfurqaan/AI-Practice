#!/bin/bash
BACKUP_DIR="/opt/vaultwarden/backups"
DATE=$(date +%Y%m%d_%H%M)
BACKUP_FILE="vaultwarden_backup_$DATE.tar.gz"

# Ensure backup directory exists
mkdir -p $BACKUP_DIR

# Go to vaultwarden directory
cd /opt/vaultwarden

# Stop containers
docker compose down

# Create backup ONLY of data and config
tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
    --exclude='backups' \
    --exclude='backup.sh' \
    data/ \
    config/

# Start containers
docker compose up -d

# Cleanup old backups (older than 7 days)
find $BACKUP_DIR -name "vaultwarden_backup_*.tar.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_FILE" >> $BACKUP_DIR/backup.log