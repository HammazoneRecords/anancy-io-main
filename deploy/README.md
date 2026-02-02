# AnancyIO Deployment Pipeline

This directory contains all the deployment configurations and scripts for deploying AnancyIO to various environments.

## 📁 Directory Structure

```
deploy/
├── scripts/          # Deployment automation scripts
│   ├── deploy.sh     # Main deployment script
│   ├── rollback.sh   # Rollback to previous version
│   ├── backup.sh     # Backup data and volumes
│   └── health-check.sh  # Health check script
├── k8s-deployment.yml   # Kubernetes deployment configuration
```

## 🚀 Quick Start

### Docker Compose Deployment

#### Staging Environment
```bash
# Using docker-compose
docker-compose -f docker-compose.staging.yml up -d

# Or using deployment script
cd deploy/scripts
chmod +x deploy.sh
./deploy.sh staging
```

#### Production Environment
```bash
# Using docker-compose
docker-compose -f docker-compose.prod.yml up -d

# Or using deployment script
cd deploy/scripts
chmod +x deploy.sh
./deploy.sh production
```

## 📦 Available Deployment Methods

### 1. Docker Compose (Recommended for single server)

**Files:**
- `docker-compose.prod.yml` - Production configuration
- `docker-compose.staging.yml` - Staging configuration

**Features:**
- Multi-container orchestration
- Persistent volumes
- Redis caching
- Nginx reverse proxy
- Auto-restart policies
- Health checks

### 2. Kubernetes (Recommended for scalable deployments)

**Files:**
- `deploy/k8s-deployment.yml` - Complete K8s configuration

**Features:**
- Auto-scaling (2-10 replicas)
- Rolling updates with zero downtime
- Persistent storage
- Load balancing
- SSL/TLS with cert-manager
- Resource limits and requests

**Deploy to Kubernetes:**
```bash
# Apply configuration
kubectl apply -f deploy/k8s-deployment.yml

# Check status
kubectl get pods -n anancyio

# View logs
kubectl logs -f deployment/anancyio -n anancyio
```

### 3. GitHub Actions CI/CD

**File:** `.github/workflows/ci-cd.yml`

**Pipeline stages:**
1. **Lint & Code Quality** - Code formatting and linting checks
2. **Test** - Run test suite across multiple Python versions
3. **Security** - Safety and Bandit security scans
4. **Build** - Build and push Docker images
5. **Deploy Staging** - Auto-deploy to staging on `develop` branch
6. **Deploy Production** - Deploy on version tags (e.g., `v1.0.0`)
7. **Rollback** - Automatic rollback on deployment failure

**Trigger deployment:**
```bash
# Deploy to staging
git push origin develop

# Deploy to production
git tag v1.0.0
git push origin v1.0.0
```

## 🔧 Configuration

### Environment Variables

Create environment-specific files:
- `.env.production` (from `.env.production.example`)
- `.env.staging` (from `.env.staging.example`)

**Required variables:**
```bash
ENVIRONMENT=production
SECRET_KEY=your-secret-key
FLASK_SECRET_KEY=your-flask-secret
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
REDIS_PASSWORD=your-redis-password
```

### GitHub Secrets

For CI/CD pipeline, configure these secrets in GitHub repository settings:

**Docker Registry:**
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub password/token

**Staging Deployment:**
- `STAGING_HOST` - Staging server hostname/IP
- `STAGING_USERNAME` - SSH username
- `STAGING_SSH_KEY` - SSH private key

**Production Deployment:**
- `PRODUCTION_HOST` - Production server hostname/IP
- `PRODUCTION_USERNAME` - SSH username
- `PRODUCTION_SSH_KEY` - SSH private key

**Notifications (optional):**
- `SLACK_WEBHOOK_URL` - Slack webhook for notifications

## 🛠️ Deployment Scripts

### Deploy Script (`deploy.sh`)

Deploy application to specified environment with automatic health checks.

```bash
./deploy.sh [environment]

# Examples
./deploy.sh staging
./deploy.sh production
```

**Features:**
- Pulls latest Docker images
- Creates backups (production only)
- Performs rolling update
- Health check verification
- Automatic rollback on failure
- Cleanup old images

### Rollback Script (`rollback.sh`)

Rollback to previous version or specific backup.

```bash
./rollback.sh [environment] [backup_date]

# Examples
./rollback.sh production
./rollback.sh production 20260131_140000
```

### Backup Script (`backup.sh`)

Create backups of all volumes and data.

```bash
./backup.sh [environment]

# Examples
./backup.sh production
./backup.sh staging
```

**Backups include:**
- Data volume
- Logs volume
- Memory volume
- Knowledge volume
- Metadata file

**Retention:** Automatically keeps last 7 days of backups

### Health Check Script (`health-check.sh`)

Verify deployment health and system resources.

```bash
./health-check.sh [environment]

# Examples
./health-check.sh production
./health-check.sh staging
```

**Checks:**
- Container status
- HTTP endpoint availability
- Disk space usage
- Memory usage
- Recent error logs

## 🔄 Deployment Workflow

### Standard Deployment Flow

1. **Pre-deployment:**
   ```bash
   # Create backup
   ./deploy/scripts/backup.sh production
   
   # Check current health
   ./deploy/scripts/health-check.sh production
   ```

2. **Deploy:**
   ```bash
   # Deploy new version
   ./deploy/scripts/deploy.sh production
   ```

3. **Verify:**
   ```bash
   # Health check
   ./deploy/scripts/health-check.sh production
   
   # Check logs
   docker-compose -f docker-compose.prod.yml logs -f
   ```

4. **Rollback (if needed):**
   ```bash
   ./deploy/scripts/rollback.sh production
   ```

### Zero-Downtime Deployment

For production deployments with zero downtime:

**Using Docker Compose:**
```bash
docker-compose -f docker-compose.prod.yml up -d --no-deps --build anancyio
```

**Using Kubernetes:**
```bash
kubectl set image deployment/anancyio anancyio=anancyioai/anancyio:v1.0.0 -n anancyio
kubectl rollout status deployment/anancyio -n anancyio
```

## 📊 Monitoring

### View Logs

**Docker Compose:**
```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f anancyio

# Last 100 lines
docker-compose -f docker-compose.prod.yml logs --tail=100
```

**Kubernetes:**
```bash
# All pods
kubectl logs -f deployment/anancyio -n anancyio

# Specific pod
kubectl logs -f anancyio-xxxxx-xxxxx -n anancyio

# Previous crashed pod
kubectl logs --previous anancyio-xxxxx-xxxxx -n anancyio
```

### Check Status

**Docker Compose:**
```bash
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml top
```

**Kubernetes:**
```bash
kubectl get all -n anancyio
kubectl describe deployment anancyio -n anancyio
kubectl top pods -n anancyio
```

## 🔐 Security Best Practices

1. **Secrets Management:**
   - Never commit `.env.production` or `.env.staging`
   - Use secret management tools (e.g., HashiCorp Vault, AWS Secrets Manager)
   - Rotate secrets regularly

2. **SSL/TLS:**
   - Use Let's Encrypt for free SSL certificates
   - Configure cert-manager for Kubernetes
   - Enable HSTS headers

3. **Network Security:**
   - Use private networks for inter-service communication
   - Implement rate limiting
   - Configure firewalls

4. **Updates:**
   - Regular security updates
   - Automated vulnerability scanning
   - Monitor CVE databases

## 🚨 Troubleshooting

### Common Issues

**Container won't start:**
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs anancyio

# Check for port conflicts
netstat -tulpn | grep :80
```

**Out of disk space:**
```bash
# Clean up Docker
docker system prune -a
docker volume prune

# Check disk usage
df -h
```

**Memory issues:**
```bash
# Check memory usage
docker stats

# Restart services
docker-compose -f docker-compose.prod.yml restart
```

**Health check failing:**
```bash
# Manual health check
curl http://localhost/health

# Check container logs
docker-compose logs --tail=50 anancyio
```

## 📞 Support

For deployment issues:
1. Check logs first
2. Review configuration files
3. Run health check script
4. Consult main documentation
5. Open GitHub issue

## 🔄 Updates

To update the deployment pipeline:
1. Test changes in staging first
2. Update documentation
3. Notify team members
4. Deploy to production
5. Monitor for issues

---

**Last Updated:** 2026-01-31
**Version:** 1.0.0
