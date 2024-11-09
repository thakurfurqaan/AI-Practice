#!/bin/bash

ENV_FILE="/opt/vaultwarden/config/.env"
CONFIG_JSON="/opt/vaultwarden/data/config.json"
BACKUP_FILE="/opt/vaultwarden/data/config.json.adminbackup"

# Function to disable admin
disable_admin() {
    echo "Disabling admin portal..."
    
    # Backup current config if backup doesn't exist
    if [ ! -f "$BACKUP_FILE" ]; then
        cp "$CONFIG_JSON" "$BACKUP_FILE"
        echo "Backed up config.json"
    fi
    
    # Update config.json
    jq 'del(.admin_token)' "$CONFIG_JSON" > "$CONFIG_JSON.tmp"
    mv "$CONFIG_JSON.tmp" "$CONFIG_JSON"
    
    echo "Admin portal disabled in config.json"
}

# Function to enable admin
enable_admin() {
    echo "Enabling admin portal..."
    
    # Restore from backup if exists
    if [ -f "$BACKUP_FILE" ]; then
        cp "$BACKUP_FILE" "$CONFIG_JSON"
        echo "Restored admin configuration from backup"
    else
        echo "No backup found, cannot enable admin"
        exit 1
    fi
}

# Install jq if not present
if ! command -v jq &> /dev/null; then
    echo "Installing jq..."
    sudo apt-get update && sudo apt-get install -y jq
fi

# Main script
case "$1" in
    "disable")
        disable_admin
        ;;
    "enable")
        enable_admin
        ;;
    "status")
        if jq -e '.admin_token' "$CONFIG_JSON" &>/dev/null; then
            echo "Admin portal is currently DISABLED"
        else
            echo "Admin portal is currently ENABLED"
        fi
        exit 0
        ;;
    *)
        echo "Usage: $0 {enable|disable|status}"
        exit 1
        ;;
esac

# Restart Vaultwarden
cd /opt/vaultwarden
docker compose down
docker compose up -d

# Verify current status
if jq -e '.disable_admin_token == true' "$CONFIG_JSON" &>/dev/null; then
    echo "Status: Admin portal is now DISABLED"
else
    echo "Status: Admin portal is now ENABLED"
fi