# 🚀 ExamGuard Deployment Guide

This guide will help you deploy ExamGuard to production environments.

## 📋 Table of Contents

- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
  - [Option 1: Traditional Server (VPS)](#option-1-traditional-server-vps)
  - [Option 2: Docker Deployment](#option-2-docker-deployment)
  - [Option 3: Cloud Platforms](#option-3-cloud-platforms)
- [Environment Configuration](#environment-configuration)
- [Security Best Practices](#security-best-practices)
- [Performance Optimization](#performance-optimization)
- [Monitoring & Maintenance](#monitoring--maintenance)

---

## 🔧 Local Development

### Prerequisites
- Python 3.8+
- Webcam
- 4GB RAM minimum (8GB recommended)
- GPU (optional, for better performance)

### Setup
```bash
# Clone repository
git clone https://github.com/yourusername/exam-guard.git
cd exam-guard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py
```

Visit `http://localhost:5000`

---

## 🌐 Production Deployment

### Option 1: Traditional Server (VPS)

#### 1. Server Setup (Ubuntu 20.04+)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.8 python3-pip python3-venv -y
sudo apt install libgl1-mesa-glx libglib2.0-0 -y  # OpenCV dependencies

# Install Nginx
sudo apt install nginx -y

# Install Supervisor (for process management)
sudo apt install supervisor -y
```

#### 2. Application Setup

```bash
# Create application directory
sudo mkdir -p /var/www/examguard
cd /var/www/examguard

# Clone repository
git clone https://github.com/yourusername/exam-guard.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn  # Production WSGI server
```

#### 3. Configure Gunicorn

Create `/var/www/examguard/gunicorn_config.py`:

```python
import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 300
keepalive = 2

# Logging
accesslog = "/var/log/examguard/access.log"
errorlog = "/var/log/examguard/error.log"
loglevel = "info"

# Process naming
proc_name = "examguard"

# Server mechanics
daemon = False
pidfile = "/var/run/examguard.pid"
user = "www-data"
group = "www-data"
```

#### 4. Configure Supervisor

Create `/etc/supervisor/conf.d/examguard.conf`:

```ini
[program:examguard]
directory=/var/www/examguard
command=/var/www/examguard/venv/bin/gunicorn -c gunicorn_config.py main:app
user=www-data
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/examguard/err.log
stdout_logfile=/var/log/examguard/out.log
```

Start the service:
```bash
sudo mkdir -p /var/log/examguard
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start examguard
```

#### 5. Configure Nginx

Create `/etc/nginx/sites-available/examguard`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (for future features)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    location /static {
        alias /var/www/examguard/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/examguard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

---

### Option 2: Docker Deployment

#### 1. Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 examguard && chown -R examguard:examguard /app
USER examguard

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "--timeout", "300", "main:app"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models
      - ./logs:/app/logs
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./static:/var/www/static:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - web
    restart: unless-stopped
```

#### 3. Build and Run

```bash
# Build image
docker-compose build

# Run containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

---

### Option 3: Cloud Platforms

#### AWS Elastic Beanstalk

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize EB:
```bash
eb init -p python-3.8 examguard
```

3. Create environment:
```bash
eb create examguard-env
```

4. Deploy:
```bash
eb deploy
```

#### Google Cloud Platform (App Engine)

1. Create `app.yaml`:
```yaml
runtime: python39
entrypoint: gunicorn -b :$PORT main:app

instance_class: F2

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

2. Deploy:
```bash
gcloud app deploy
```

#### Heroku

1. Create `Procfile`:
```
web: gunicorn main:app
```

2. Deploy:
```bash
heroku create examguard-app
git push heroku main
```

---

## ⚙️ Environment Configuration

### Production Settings

Create `.env` file:

```env
# Flask
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this

# Server
HOST=0.0.0.0
PORT=8000

# Detection Settings
DETECTION_CONFIDENCE=0.55
GAZE_THRESHOLD=3.0
POSE_THRESHOLD=2.0

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/examguard/app.log

# Database (for future use)
DATABASE_URL=postgresql://user:pass@localhost/examguard

# Email (for alerts)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

Update `main.py` to use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
```

---

## 🔒 Security Best Practices

### 1. HTTPS Only
- Always use SSL/TLS in production
- Redirect HTTP to HTTPS
- Use HSTS headers

### 2. Authentication
- Implement user authentication
- Use JWT tokens for API access
- Add rate limiting

### 3. Input Validation
- Validate all user inputs
- Sanitize file uploads
- Implement CSRF protection

### 4. Secure Headers

Add to Nginx config:
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

### 5. Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## ⚡ Performance Optimization

### 1. Use GPU Acceleration

Install CUDA and GPU-enabled libraries:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### 2. Enable Caching

Add Redis for session management:
```bash
pip install redis flask-caching
```

### 3. Optimize Video Processing

- Reduce frame rate if needed
- Use hardware acceleration
- Implement frame skipping for non-critical detection

### 4. CDN for Static Assets

Use CloudFlare, AWS CloudFront, or similar for:
- CSS/JS files
- Images
- Fonts

---

## 📊 Monitoring & Maintenance

### 1. Application Monitoring

Install monitoring tools:
```bash
pip install prometheus-flask-exporter
```

### 2. Log Management

Use ELK Stack or similar:
- Elasticsearch for storage
- Logstash for processing
- Kibana for visualization

### 3. Health Checks

Add health endpoint to `main.py`:
```python
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})
```

### 4. Backup Strategy

```bash
# Backup script
#!/bin/bash
BACKUP_DIR="/backups/examguard"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup database
pg_dump examguard > "$BACKUP_DIR/db_$DATE.sql"

# Backup logs
tar -czf "$BACKUP_DIR/logs_$DATE.tar.gz" /var/log/examguard/

# Keep only last 30 days
find $BACKUP_DIR -mtime +30 -delete
```

### 5. Update Procedure

```bash
# Pull latest code
cd /var/www/examguard
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Restart application
sudo supervisorctl restart examguard

# Check logs
sudo tail -f /var/log/examguard/out.log
```

---

## 🆘 Troubleshooting

### Common Issues

1. **Camera not detected**
   - Check camera permissions
   - Verify OpenCV installation
   - Test with `v4l2-ctl --list-devices` (Linux)

2. **High CPU usage**
   - Enable GPU acceleration
   - Reduce detection frequency
   - Optimize worker count

3. **Memory leaks**
   - Monitor with `htop`
   - Restart workers periodically
   - Check for unclosed resources

4. **Slow response times**
   - Enable caching
   - Optimize database queries
   - Use CDN for static files

---

## 📞 Support

For deployment assistance:
- 📧 Email: devops@examguard.com
- 💬 Discord: [Join our community](https://discord.gg/examguard)
- 📖 Docs: [docs.examguard.com/deployment](https://docs.examguard.com/deployment)

---

**Happy Deploying! 🚀**
