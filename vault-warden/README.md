# Vaultwarden Self-Hosted Setup Guide

A comprehensive guide to set up Vaultwarden (Bitwarden RS) on a Debian-based system.

## Prerequisites
- Debian-based system (Ubuntu/Debian)
- Domain name
- Root/sudo access
- GCP Instance (or any cloud provider)

## Overview
- Vaultwarden is a bitwarden server implementation written in Rust.
- This setup includes a backup script and a restore script.
- The admin token can be toggled on and off.
- Nginx is used as a reverse proxy.
- SSL is terminated at the Nginx level.
- Domain is configured in the Nginx setup which is used to access Vaultwarden.

## Backups
- Backups are stored in `/opt/vaultwarden/backups`.
- Backups are compressed using `tar.gz`.
- Backups are automatically cleaned up after 7 days.

## Directory Structure
```
/opt/vaultwarden/
├── docker-compose.yml
├── backup.sh
├── data/
├── config/
│   └── .env
├── backups/
├── restore.sh
└── toggle-admin.sh
```

## Step-by-Step Installation

### 1. Initial Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    nginx \
    fail2ban
```

### 2. Docker Installation
```bash
# Add Docker's GPG key
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

### 3. Create Directory Structure
```bash
sudo mkdir -p /opt/vaultwarden/{data,config,backups}
cd /opt/vaultwarden
```

### 4. Docker Compose Configuration
Create `docker-compose.yml` 

### 5. Environment Configuration
Create `config/.env`:
```env
# Domain Settings
DOMAIN=https://vault.yourdomain.com

# Admin Settings
ADMIN_TOKEN=$argon2id$v=19$m=65540,t=3,p=4$YOUR_HASH
ADMIN_SESSION_LIFETIME=20
SIGNUPS_ALLOWED=false

# Security
LOGIN_ATTEMPTS=3
DISABLE_ADMIN_TOKEN=false
ENABLE_DB_WAL=true
WEB_VAULT_ENABLED=true
```

### 6. Nginx Configuration
Create `/etc/nginx/sites-available/vaultwarden`:
```nginx
server {
    server_name vault.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    listen 80;
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/vaultwarden /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

### 7. SSL Certificate
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d vault.yourdomain.com
```

### 8. Backup Configuration
Create `backup.sh`:
```bash                                                                                       
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
```

Make executable:
```bash
sudo chmod +x /opt/vaultwarden/backup.sh
```

### 9. Schedule Backup
Add to crontab:
```bash
(crontab -l 2>/dev/null; echo "0 0 * * * /opt/vaultwarden/backup.sh") | crontab -
```

### 10. Generate Admin Credentials
```bash
# Generate password
openssl rand -base64 32 | tr -dc 'a-zA-Z0-9' | head -c 32

# Generate hash
echo -n "YOUR_PASSWORD" | argon2 "$(openssl rand -base64 32)" -e -id -k 65540 -t 3 -p 4
```

### 11. Start Services
```bash
cd /opt/vaultwarden
sudo docker compose up -d
```

## Important Notes

### Security Checklist
- [ ] Update domain DNS settings
- [ ] Save admin password securely
- [ ] Enable GCP firewall rules
- [ ] Test backups
- [ ] Test restore process
- [ ] Save configuration files securely

### Maintenance
- Regular backups check
- Monitor logs
- Keep system updated
- Check SSL certificate renewal

### Backup and Restore
To force backup:
```bash
sudo /opt/vaultwarden/backup.sh
```

To restore:
```bash
cd /opt/vaultwarden
docker compose down
tar -xzf backups/vault_DATE.tar.gz
docker compose up -d
```

### Useful Commands
```bash
# Check services
sudo systemctl status nginx
docker ps
crontab -l

# Check logs
sudo tail -f /var/log/nginx/error.log
docker compose logs -f
```

## Troubleshooting
- Check Nginx logs: `/var/log/nginx/error.log`
- Check Docker logs: `docker compose logs -f`
- Verify SSL: `certbot certificates`
- Check backup logs: `/opt/vaultwarden/backups/backup.log`

## References
- [Vaultwarden Wiki](https://github.com/dani-garcia/vaultwarden/wiki)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)

Need help? Create an issue or refer to the documentation.