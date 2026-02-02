# 🚀 AnancyIO Deployment Guide

Complete guide for deploying AnancyIO to various environments with comprehensive CI/CD pipeline.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Deployment Methods](#deployment-methods)
- [CI/CD Pipeline](#cicd-pipeline)
- [Configuration](#configuration)
- [Monitoring & Maintenance](#monitoring--maintenance)
- [Troubleshooting](#troubleshooting)

## Overview

This deployment pipeline provides:

- ✅ **Automated CI/CD** with GitHub Actions
- ✅ **Multiple deployment targets** (Docker Compose, Kubernetes)
- ✅ **Environment separation** (staging, production)
- ✅ **Zero-downtime deployments**
- ✅ **Automatic rollbacks** on failure
- ✅ **Backup and restore** capabilities
- ✅ **Health monitoring** and alerts
- ✅ **Security scanning** and best practices

## Prerequisites

### Required Software

- **Docker** (20.10+) and Docker Compose (2.0+)
- **Git** for version control
- **Make** (optional, for convenience commands)

### For Kubernetes Deployment

- **kubectl** configured with cluster access
- **Helm** (optional, for package management)
- **cert-manager** for SSL certificates

### Server Requirements

#### Minimum (Staging)
- 2 CPU cores
- 4GB RAM
- 20GB disk space
- Ubuntu 20.04+ or similar Linux distribution

#### Recommended (Production)
- 4+ CPU cores
- 8GB+ RAM
- 50GB+ disk space
- Ubuntu 22.04 LTS or similar

## Quick Start

### 1. Local Development

```bash
# Clone repository
git clone https://github.com/anancyioai/anancyio.git
cd anancyio

# Run locally
make run
# or
docker-compose up -d

# Access at http://localhost:50080
```

### 2. Deploy to Staging

```bash
# Setup environment
cp .env.staging.example .env.staging
# Edit .env.staging with your values

# Deploy
make deploy-staging
# or
./deploy/scripts/deploy.sh staging
```

### 3. Deploy to Production

```bash
# Setup environment
cp .env.production.example .env.production
# Edit .env.production with your values

# Deploy
make deploy-production
# or
./deploy/scripts/deploy.sh production
```

## Deployment Methods

### Method 1: Docker Compose (Recommended for Single Server)

**Best for:** Small to medium deployments, simple infrastructure

```bash
# Production
docker-compose -f docker-compose.prod.yml up -d

# Staging
docker-compose -f docker-compose.staging.yml up -d
```

**Features:**
- Easy setup and management
- Persistent volumes for data
- Redis for caching
- Nginx reverse proxy
- Health checks
- Auto-restart

**Files:**
- `docker-compose.prod.yml` - Production configuration
- `docker-compose.staging.yml` - Staging configuration

### Method 2: Kubernetes (Recommended for Scale)

**Best for:** Large deployments, high availability, auto-scaling

```bash
# Deploy
kubectl apply -f deploy/k8s-deployment.yml

# Check status
kubectl get all -n anancyio

# Scale
kubectl scale deployment/anancyio --replicas=5 -n anancyio
```

**Features:**
- Auto-scaling (2-10 replicas)
- Rolling updates
- Self-healing
- Load balancing
- Persistent storage
- SSL/TLS automated

**File:** `deploy/k8s-deployment.yml`

### Method 3: Manual Deployment

```bash
# Build image
docker build -f DockerfileLocal -t anancyio:latest .

# Run container
docker run -d \
  -p 80:80 \
  -v anancyio-data:/a_io/usr \
  -e OPENAI_API_KEY=your-key \
  anancyio:latest
```

## CI/CD Pipeline

### GitHub Actions Workflow

The automated pipeline is triggered on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Version tags (e.g., `v1.0.0`)

**Pipeline Stages:**

```
┌─────────────┐
│    Lint     │ ← Code quality checks
└──────┬──────┘
       │
┌──────▼──────┐
│    Test     │ ← Run test suite
└──────┬──────┘
       │
┌──────▼──────┐
│  Security   │ ← Security scanning
└──────┬──────┘
       │
┌──────▼──────┐
│    Build    │ ← Build Docker image
└──────┬──────┘
       │
       ├─────────────────────┐
       │                     │
┌──────▼──────┐      ┌──────▼──────┐
│   Staging   │      │ Production  │
│  (develop)  │      │   (tags)    │
└─────────────┘      └─────────────┘
```

**File:** `.github/workflows/ci-cd.yml`

### Triggering Deployments

**Deploy to Staging:**
```bash
git checkout develop
git add .
git commit -m "Your changes"
git push origin develop
# Automatically deploys to staging
```

**Deploy to Production:**
```bash
git checkout main
git merge develop
git tag v1.0.0
git push origin main --tags
# Automatically deploys to production
```

### Required GitHub Secrets

Configure in **Settings → Secrets and variables → Actions**:

```
DOCKER_USERNAME          - Docker Hub username
DOCKER_PASSWORD          - Docker Hub token
STAGING_HOST            - Staging server IP/hostname
STAGING_USERNAME        - SSH username
STAGING_SSH_KEY         - SSH private key
PRODUCTION_HOST         - Production server IP/hostname
PRODUCTION_USERNAME     - SSH username
PRODUCTION_SSH_KEY      - SSH private key
SLACK_WEBHOOK_URL       - (Optional) Slack notifications
```

## Configuration

### Environment Variables

Create `.env.production` from template:

```bash
cp .env.production.example .env.production
```

**Essential Variables:**

```bash
# Application
ENVIRONMENT=production
LOG_LEVEL=info
WORKERS=4

# Security (generate strong random values)
SECRET_KEY=your-secret-key-here
FLASK_SECRET_KEY=your-flask-secret-here

# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Redis
REDIS_PASSWORD=strong-password-here
```

### SSL/TLS Configuration

#### Option 1: Let's Encrypt (Recommended)

```bash
# Install certbot
sudo apt-get install certbot

# Get certificate
sudo certbot certonly --standalone -d anancyio.ai -d www.anancyio.ai

# Copy certificates
sudo cp /etc/letsencrypt/live/anancyio.ai/fullchain.pem ./certs/
sudo cp /etc/letsencrypt/live/anancyio.ai/privkey.pem ./certs/
```

#### Option 2: Custom Certificates

Place your certificates in `./certs/`:
- `fullchain.pem` - Full certificate chain
- `privkey.pem` - Private key

### Nginx Configuration

Edit `nginx/conf.d/anancyio.conf` to customize:
- Server names
- SSL settings
- Rate limiting
- Proxy settings

## Monitoring & Maintenance

### Health Checks

```bash
# Check application health
make health-prod
# or
./deploy/scripts/health-check.sh production

# Manual check
curl https://anancyio.ai/health
```

### View Logs

```bash
# Production logs
make logs-prod
# or
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f anancyio

# Last 100 lines
docker-compose -f docker-compose.prod.yml logs --tail=100
```

### Backups

**Automatic Backups:**
```bash
# Create backup
make backup-prod
# or
./deploy/scripts/backup.sh production
```

**Backup includes:**
- Application data
- User files
- Memory/knowledge base
- Configuration

**Restore from Backup:**
```bash
# List available backups
make list-backups

# Restore specific backup
./deploy/scripts/rollback.sh production 20260131_140000
```

### Updates

**Zero-Downtime Update:**
```bash
# Pull latest image
docker-compose -f docker-compose.prod.yml pull

# Rolling update
docker-compose -f docker-compose.prod.yml up -d --no-deps anancyio
```

**With Downtime:**
```bash
make deploy-production
```

### Rollback

```bash
# Quick rollback
make rollback-prod

# Rollback to specific backup
./deploy/scripts/rollback.sh production 20260131_140000
```

## Make Commands Reference

```bash
# Development
make build              # Build Docker image
make run                # Run locally
make stop               # Stop containers
make shell              # Open container shell

# Staging
make deploy-staging     # Deploy to staging
make rollback-staging   # Rollback staging
make backup-staging     # Backup staging
make health-staging     # Health check
make logs-staging       # View logs

# Production
make deploy-production  # Deploy to production
make rollback-prod      # Rollback production
make backup-prod        # Backup production
make health-prod        # Health check
make logs-prod          # View logs

# Kubernetes
make k8s-deploy         # Deploy to K8s
make k8s-status         # Check status
make k8s-logs           # View logs

# Utilities
make clean              # Clean Docker resources
make test               # Run tests
make monitor            # Monitor resources
```

## Troubleshooting

### Common Issues

#### Container Won't Start

```bash
# Check logs
docker-compose logs anancyio

# Check if port is in use
netstat -tulpn | grep :80

# Restart
docker-compose restart
```

#### Out of Memory

```bash
# Check memory usage
docker stats

# Increase container limits in docker-compose.yml
# Restart services
docker-compose restart
```

#### Database Connection Failed

```bash
# Check Redis
docker-compose exec redis redis-cli ping

# Check environment variables
docker-compose exec anancyio env | grep REDIS

# Restart Redis
docker-compose restart redis
```

#### SSL Certificate Issues

```bash
# Verify certificate
openssl x509 -in certs/fullchain.pem -text -noout

# Check Nginx config
docker-compose exec nginx nginx -t

# Reload Nginx
docker-compose exec nginx nginx -s reload
```

### Performance Issues

**High CPU Usage:**
```bash
# Check running processes
docker-compose top

# Reduce workers
# Edit WORKERS in .env file
docker-compose restart
```

**High Memory Usage:**
```bash
# Check memory
docker stats

# Restart application
docker-compose restart anancyio
```

**Slow Response:**
```bash
# Check Redis cache
docker-compose exec redis redis-cli info stats

# Clear cache
docker-compose exec redis redis-cli FLUSHALL
```

### Emergency Procedures

**Complete System Failure:**
```bash
# Stop everything
docker-compose -f docker-compose.prod.yml down

# Restore from backup
./deploy/scripts/rollback.sh production [backup_date]

# Start services
docker-compose -f docker-compose.prod.yml up -d
```

**Data Corruption:**
```bash
# Stop application
docker-compose stop anancyio

# Restore data from backup
# (see backup script)

# Start application
docker-compose start anancyio
```

## Security Best Practices

### 1. Secrets Management
- Never commit `.env` files
- Use environment variables
- Rotate secrets regularly
- Use secret management tools (Vault, AWS Secrets Manager)

### 2. Network Security
- Use private networks
- Enable firewall
- Implement rate limiting
- Use HTTPS only

### 3. Updates
- Regular security updates
- Monitor CVE databases
- Automated scanning (included in CI/CD)

### 4. Backups
- Daily automated backups
- Test restore procedures
- Off-site backup storage

### 5. Monitoring
- Set up alerts
- Monitor logs
- Track resource usage
- Regular health checks

## Support & Documentation

- **Main Documentation:** [/docs/README.md](../docs/README.md)
- **Deployment Docs:** [/deploy/README.md](../deploy/README.md)
- **GitHub Issues:** [Report Issues](https://github.com/anancyioai/anancyio/issues)
- **Discord:** [Join Community](https://discord.gg/B8KZKNsPpj)

## Additional Resources

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [GitHub Actions Guide](https://docs.github.com/en/actions)
- [Nginx Configuration](https://nginx.org/en/docs/)

---

**Version:** 1.0.0  
**Last Updated:** 2026-01-31  
**Maintained By:** AnancyIO Team
