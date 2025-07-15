# GCP SSL Certificate Renewal Guide

## Quick Steps

### 1. Login to GCP
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Select your project

### 2. Enable HTTP Access
- **Compute Engine** → **VM instances**
- Click instance name → **Edit**
- Check **Allow HTTP traffic** → **Save**

### 3. SSH into Instance
- Click **SSH** button next to your instance

### 4. Renew Certificate
```bash
sudo certbot renew --cert-name vault.furqaanthakur.com
```

### 5. Check Expiry
```bash
echo | openssl s_client -servername vault.furqaanthakur.com -connect vault.furqaanthakur.com:443 2>/dev/null | openssl x509 -noout -dates
```

### 6. Disable HTTP Access
- Return to GCP Console
- Instance → **Edit**
- Uncheck **Allow HTTP traffic** → **Save**

### 7. Set a reminder to renew within 15 days of expiry
- TickTick

## Notes
- Let's Encrypt certificates valid for 90 days
- Always disable HTTP after renewal for security