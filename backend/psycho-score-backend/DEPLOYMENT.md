# 🚀 Psycho Score Backend Deployment Guide

*"The deployment must be flawless. Absolutely flawless."*

## Quick Start (Development)

### Windows Setup
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (PowerShell)
venv\Scripts\Activate.ps1

# If you get execution policy error, run this first:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Alternative: Use Command Prompt instead
# venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

### Linux/macOS Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration
1. Copy `.env.example` to `.env`
2. Add your API keys:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key
   ELEVENLABS_API_KEY=your_actual_elevenlabs_api_key
   ```

### Create Required Directories
```bash
# Create upload and output directories
mkdir -p uploads/images outputs/audio
```

### Start Development Server
```bash
cd src
uvicorn main:app --reload
```

Visit: `http://localhost:8000`

## 🧪 Testing

### Automated Testing
```bash
# Basic API tests
python test_api.py

# Test with business card image
python test_api.py /path/to/business_card.jpg
```

### Manual Testing
- **API Documentation**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`
- **API Info**: `http://localhost:8000/api`

## 🌐 Production Deployment

### Environment Variables
```env
# Required
GEMINI_API_KEY=your_production_gemini_key
ELEVENLABS_API_KEY=your_production_elevenlabs_key

# Optional Production Settings
DEBUG=false
LOG_LEVEL=WARNING
MAX_FILE_SIZE=5242880  # 5MB for production
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    client_max_body_size 10M;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
    }
    
    location /audio/ {
        alias /path/to/outputs/audio/;
        expires 1h;
        add_header Cache-Control "public, immutable";
    }
}
```

### SSL with Let's Encrypt
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Systemd Service
```ini
# /etc/systemd/system/psycho-score.service
[Unit]
Description=Psycho Score Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/psycho-score-backend
Environment=PATH=/opt/psycho-score-backend/venv/bin
Environment=PYTHONPATH=/opt/psycho-score-backend/src
ExecStart=/opt/psycho-score-backend/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable psycho-score
sudo systemctl start psycho-score
sudo systemctl status psycho-score
```

## 📊 Monitoring

### Health Checks
- **Endpoint**: `GET /health`
- **Expected**: `{"status": "healthy"}`

### Logging
```python
# Add to main.py for production logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Metrics (Optional)
```bash
# Add prometheus metrics
pip install prometheus-fastapi-instrumentator

# In main.py:
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)
```

## 🔒 Security

### API Keys
- Store in environment variables, never in code
- Use different keys for development/production
- Rotate keys regularly

### Rate Limiting
```python
# Add to requirements.txt: slowapi
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add to endpoints:
@limiter.limit("10/minute")
@router.post("/business-card")
async def analyze_business_card(request: Request, ...):
```

### File Upload Security
- Validate file types and sizes
- Scan for malware (production)
- Use temporary storage with cleanup

## 🚨 Troubleshooting

### Common Issues

**1. PowerShell Execution Policy (Windows)**
```powershell
# If you can't run venv\Scripts\Activate.ps1, fix execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again:
venv\Scripts\Activate.ps1

# Alternative: Use Command Prompt instead of PowerShell
# cmd
# venv\Scripts\activate.bat
```

**2. Import Errors**
```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=/path/to/psycho-score-backend/src
```

**3. API Key Issues**
```bash
# Check environment variables
echo $GEMINI_API_KEY
echo $ELEVENLABS_API_KEY
```

**4. Permission Issues**
```bash
# Fix directory permissions
chmod -R 755 uploads/ outputs/
```

**5. Port Already in Use**
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8001
```

### Performance Optimization

**1. Async Configuration**
```python
# Increase worker processes for production
uvicorn main:app --workers 4 --host 0.0.0.0 --port 8000
```

**2. File Caching**
```python
# Add Redis for caching (optional)
pip install redis aioredis
```

**3. Database (Future)**
```python
# For storing analysis results
pip install sqlalchemy alembic asyncpg
```

## 📈 Scaling

### Horizontal Scaling
- Load balancer (nginx, HAProxy)
- Multiple server instances
- Shared file storage (NFS, S3)

### Vertical Scaling
- Increase server resources
- Optimize memory usage
- Cache frequently accessed data

### Cloud Deployment
- **AWS**: EC2, App Runner, Elastic Beanstalk
- **GCP**: Compute Engine, App Engine, Cloud Run
- **Azure**: App Service, Container Instances
- **Vercel**: Serverless deployment with custom domains
- **Railway**: Simple deployment with automatic SSL
- **Render**: Easy deployment with free tier options

### Platform-Specific Deployment

#### **Vercel (Recommended for Web)**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

#### **Railway**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway deploy
```

#### **Render**
- Connect GitHub repository
- Set build command: `pip install -r requirements.txt`
- Set start command: `cd src && uvicorn main:app --host 0.0.0.0 --port $PORT`

---

*"The deployment strategy is not just about code... it's about perfection."* - Patrick Bateman, if he were a DevOps engineer