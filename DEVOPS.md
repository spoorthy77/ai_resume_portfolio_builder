# DevOps Documentation

## Overview

This document outlines the DevOps setup for the AI Resume & Portfolio Builder application, including containerization, CI/CD pipelines, and deployment strategies.

## Architecture

```
                    GitHub Repository
                          |
                          v
                   GitHub Actions CI/CD
                    /          |        \
                   /           |         \
            Test Backend   Test Frontend  Docker Build
                   \           |         /
                    \          |        /
                     Security Scan & Review
                          |
                          v
                    Manual Approval (Production)
                          |
                          v
            Deploy to Heroku / AWS EC2 / Custom VPS
```

## Docker Setup

### Dockerfile Details

The Dockerfile uses multi-stage builds for optimization:

**Stage 1: Backend Builder**
- Based on `python:3.11-slim`
- Installs Python dependencies in isolated layer
- Reduces final image size

**Stage 2: Final Image**
- Includes Python runtime and Node.js
- Copies pre-compiled Python packages
- Includes both backend and frontend

### Running with Docker

**Development:**
```bash
docker-compose up --build
```

**Production:**
```bash
docker build -t ai-resume-portfolio:prod .
docker run -p 5000:5000 \
  --env-file .env \
  -v generated_resumes:/app/generated_resumes \
  ai-resume-portfolio:prod
```

### Docker Compose Services

- **app**: Main Flask + React application
- **redis**: Caching and session management (optional)

## GitHub Actions Workflows

### CI/CD Pipeline (`.github/workflows/ci-cd.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

**Jobs:**

1. **test-backend**
   - Runs on Python 3.10 & 3.11
   - Lints code with flake8
   - Runs pytest tests
   - Generates coverage reports

2. **test-frontend**
   - Sets up Node.js 18
   - Installs npm dependencies
   - Lints with ESLint
   - Builds React application

3. **docker-build**
   - Builds Docker image
   - Uses GitHub Actions cache for faster builds
   - Doesn't push to registry (use deploy.yml for that)

4. **security-scan**
   - Runs Trivy filesystem scanner
   - Checks for vulnerabilities in dependencies
   - Uploads results to GitHub Security tab

### Deployment Pipeline (`.github/workflows/deploy.yml`)

**Triggers:**
- Push to `main` branch only
- Manual trigger via `workflow_dispatch`

**Deployment Options:**

1. **Heroku Deployment** (Primary)
   - Automatic on main branch push
   - Uses Heroku CLI via GitHub Actions
   - Requires: `HEROKU_API_KEY`, `HEROKU_APP_NAME`, `HEROKU_EMAIL`

2. **AWS EC2 Deployment** (Fallback)
   - Connects via SSH
   - Pulls latest code
   - Rebuilds Docker containers
   - Requires: `EC2_HOST`, `EC2_USER`, `EC2_PRIVATE_KEY`

3. **Slack Notifications**
   - Sends deployment status updates
   - Requires: `SLACK_WEBHOOK`

## Environment Configuration

### Development (`.env`)

```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key
DATABASE_URL=sqlite:///dev.db
GROK_API_KEY=sk_...
```

### Production (`.env`)

```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<strong-random-key>
DATABASE_URL=<postgresql-or-mysql-url>
GROK_API_KEY=sk_...
```

### Example variables in `.env.example`

Copy `.env.example` to `.env` and fill in actual values.

## GitHub Secrets Setup

### For CI/CD:
No secrets required - these jobs run on default permissions.

### For Heroku Deployment:

1. Go to Repository Settings → Secrets and variables → Actions
2. Add these secrets:

```
HEROKU_API_KEY     = <API key from Heroku account>
HEROKU_APP_NAME    = <your-heroku-app-name>
HEROKU_EMAIL       = <your-heroku-email>
```

Get Heroku API key:
```bash
heroku authorizations:create --description="GitHub Actions"
```

### For AWS EC2 Deployment:

```
EC2_HOST           = ec2-user@your-instance.compute.amazonaws.com
EC2_USER           = ec2-user
EC2_PRIVATE_KEY    = <contents of private key file>
```

### For Slack Notifications:

```
SLACK_WEBHOOK      = https://hooks.slack.com/services/T00000000/B00000000/...
```

Create webhook at: https://api.slack.com/messaging/webhooks

## Deployment Strategies

### Strategy 1: Heroku (Recommended for simplicity)

**Pros:**
- Zero infrastructure management
- Automatic SSL/TLS
- Built-in logging and monitoring
- Simple GitHub integration

**Cons:**
- Less control over environment
- Can be expensive at scale

**Setup:**
1. Create Heroku account
2. Create new app
3. Set GitHub secrets
4. Push to main branch

### Strategy 2: AWS EC2 (Full control)

**Pros:**
- Full control over infrastructure
- Cost-effective at scale
- Custom configurations

**Cons:**
- Manual infrastructure management
- Requires security best practices

**Setup:**
1. Launch EC2 instance (Ubuntu 22.04+ recommended)
2. Install Docker & Docker Compose
3. Clone repository
4. Set environment variables
5. Run `docker-compose up -d`
6. Configure reverse proxy (Nginx/Apache)

**Sample EC2 User Data Script:**
```bash
#!/bin/bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose nginx
sudo systemctl start docker
sudo usermod -aG docker $USER
```

### Strategy 3: Custom VPS/Dedicated Server

Similar to EC2, but on any Linux VPS provider:
- DigitalOcean
- Linode
- Vultr
- Oracle Cloud

## Monitoring & Logging

### GitHub Actions Logs
- View in Actions tab of repository
- Each workflow run shows real-time logs
- Logs retained for 90 days

### Application Logs

**Docker:**
```bash
docker logs <container-id>
docker logs -f <container-id>  # Follow logs
```

**Heroku:**
```bash
heroku logs --tail
```

**EC2:**
```bash
tail -f /var/log/application.log
```

## Database Migrations

For production deployments, ensure database migrations run:

**In docker-compose.yml:**
```yaml
app:
  command: >
    sh -c "flask db upgrade &&
           gunicorn -w 4 -b 0.0.0.0:5000 app:app"
```

## SSL/TLS Configuration

### Heroku
- Automatic with `*.herokuapp.com`
- Custom domain: Set CNAME records

### AWS EC2
```bash
# Using Let's Encrypt via Certbot
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com
```

Configure Nginx to use certificates.

## Scaling Considerations

### Horizontal Scaling
- Load balancer (AWS ALB, Nginx)
- Multiple app instances
- Shared database (RDS)
- Redis for sessions/caching

### Vertical Scaling
- Increase instance size
- More CPU/memory
- Database optimization

## Performance Optimization

### Frontend
```bash
# Already configured in docker-compose
# npm run build produces optimized bundle
```

### Backend
- Enable caching with Redis
- Database query optimization
- Connection pooling
- Implement rate limiting

### Docker
- Use slim base images (already done)
- Multi-stage builds (already done)
- Remove unnecessary dependencies

## Security Best Practices

✅ **Implemented:**
- Environment variables for secrets
- .gitignore excludes .env files
- Trivy vulnerability scanning in CI/CD
- Docker layer caching

⚠️ **Recommended:**
- Enable branch protection on main
- Require PR reviews before merge
- Use HTTPS everywhere
- Regular dependency updates
- Implement WAF (Web Application Firewall)
- Regular security audits

## Maintenance Tasks

### Weekly
- Monitor application logs
- Check for failed GitHub Actions

### Monthly
- Update dependencies
- Review security advisories
- Database backups verification

### Quarterly
- Full security audit
- Performance review
- Cost optimization

## Troubleshooting

### Deployment Fails on GitHub Actions

1. Check workflow logs in GitHub Actions tab
2. Verify GitHub secrets are set correctly
3. Ensure branch protection rules allow deployments

### Docker Build Fails

```bash
# Clear cache and rebuild
docker-compose build --no-cache
```

### Application Won't Start

```bash
# Check logs
docker logs <container-id>

# Verify environment variables
docker inspect <container-id> | grep -A 20 Env

# Test manually
docker run -it <image-id> /bin/bash
```

### Out of Disk Space on Server

```bash
# Clean Docker
docker system prune -a

# Check disk usage
df -h

# Remove old logs
sudo find /var/log -name "*.log" -mtime +30 -delete
```

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/latest/deploying/)
- [Heroku Documentation](https://devcenter.heroku.com/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Trivy Vulnerability Scanner](https://aquasecurity.github.io/trivy/)

---

Last Updated: February 2026
