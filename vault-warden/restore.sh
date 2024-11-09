#!/bin/bash

cd /opt/vaultwarden
docker compose down
sudo tar -xzf backups/vaultwarden_backup_YYYYMMDD_HHMM.tar.gz -C /opt/vaultwarden/
docker compose up -d