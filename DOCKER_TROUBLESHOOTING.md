# Docker Build Troubleshooting Guide

## Pre-Build Checks

Run the validation script first:
```powershell
.\check-docker.ps1
```

## Common Issues & Solutions

### 1. **Fortran Compiler Error (scipy build failure)**
**Error:** `Unknown compiler(s): [['gfortran']`

**Solution:** The robust Dockerfile already includes gfortran. If still failing:
```powershell
# Use the pre-built wheels approach
docker-compose -f docker-compose.robust.yml up --build
```

### 2. **Out of Memory During Build**
**Error:** `ERROR: failed to solve: process exited with code: 137`

**Solutions:**
- Increase Docker memory in Docker Desktop Settings → Resources → Memory (set to 6GB+)
- Close other applications during build
- Build with limited parallelism:
```powershell
docker-compose -f docker-compose.robust.yml build --no-cache --memory=6g
```

### 3. **Network Timeout (pip packages)**
**Error:** `ReadTimeoutError` or `Could not fetch URL`

**Solutions:**
- Check internet connection
- Retry build (Docker caches successful layers)
- Use longer timeout:
```powershell
$env:PIP_DEFAULT_TIMEOUT=300
docker-compose -f docker-compose.robust.yml up --build
```

### 4. **Disk Space Issues**
**Error:** `no space left on device`

**Solutions:**
```powershell
# Clean up Docker
docker system prune -a --volumes

# Check space
docker system df

# Remove old images
docker image prune -a
```

### 5. **Port Already in Use**
**Error:** `bind: address already in use`

**Solutions:**
```powershell
# Find what's using port 50080
netstat -ano | findstr :50080

# Kill the process (replace PID)
taskkill /PID <pid> /F

# Or change the port in docker-compose.robust.yml
# Change "50080:80" to "50081:80"
```

### 6. **WSL 2 Backend Issues**
**Error:** `The WSL 2 distribution has not been started`

**Solutions:**
```powershell
# Restart WSL
wsl --shutdown
# Restart Docker Desktop
```

### 7. **BuildKit Errors**
**Error:** `failed to solve with frontend dockerfile.v0`

**Solutions:**
```powershell
# Disable BuildKit temporarily
$env:DOCKER_BUILDKIT=0
docker-compose -f docker-compose.robust.yml up --build
```

### 8. **Playwright Install Fails**
**Error:** `playwright install chromium failed`

**This is non-critical and won't stop the build.** The Dockerfile has `|| true` to continue.

### 9. **Permission Denied (Windows)**
**Error:** `PermissionError: [Errno 13]`

**Solutions:**
```powershell
# Run PowerShell as Administrator
# Or adjust Docker Desktop file sharing settings
```

## Build Strategies

### Strategy 1: Quick Build (Recommended)
```powershell
# Validate first
.\check-docker.ps1

# Build and run
docker-compose -f docker-compose.robust.yml up --build -d

# Follow logs
docker-compose -f docker-compose.robust.yml logs -f
```

### Strategy 2: Step-by-Step Build
```powershell
# Build only (no run)
docker-compose -f docker-compose.robust.yml build

# Then run
docker-compose -f docker-compose.robust.yml up -d
```

### Strategy 3: Clean Build (if cache issues)
```powershell
# Remove old containers/images
docker-compose -f docker-compose.robust.yml down -v
docker rmi anancy-io-main-anancyio

# Build fresh
docker-compose -f docker-compose.robust.yml up --build --force-recreate
```

### Strategy 4: Debug Build
```powershell
# Build with verbose output
docker-compose -f docker-compose.robust.yml build --progress=plain --no-cache
```

## Monitoring Build Progress

### Check what's happening:
```powershell
# In another terminal, monitor Docker
docker ps -a

# Check resource usage
docker stats

# View build logs in detail
docker-compose -f docker-compose.robust.yml logs --tail=100
```

## Post-Build Verification

```powershell
# Check if container is running
docker ps

# Check logs
docker-compose -f docker-compose.robust.yml logs --tail=50

# Test health endpoint (wait 60 seconds after start)
curl http://localhost:50080/health

# Access web interface
# Open browser: http://localhost:50080
```

## Emergency: Start Fresh

If nothing works, complete reset:

```powershell
# Stop everything
docker-compose -f docker-compose.robust.yml down -v

# Remove all AnancyIO images
docker images | findstr anancy | ForEach-Object { docker rmi $_.Split()[2] -f }

# Prune system
docker system prune -a --volumes -f

# Restart Docker Desktop

# Try again
.\check-docker.ps1
docker-compose -f docker-compose.robust.yml up --build
```

## Getting Help

If issues persist:

1. Save build output:
```powershell
docker-compose -f docker-compose.robust.yml build > build-log.txt 2>&1
```

2. Share build-log.txt for assistance

3. Check Docker Desktop logs:
   - Docker Desktop → Troubleshoot → View logs

## Alternative: Use Original Setup

If the simplified build doesn't work, use the original base image approach:

```powershell
# Build base image (one time, 20-30 minutes)
docker-compose build anancyio-base

# Build app
docker-compose build anancyio

# Run
docker-compose up -d
```

## Expected Build Time

- **First build:** 15-25 minutes
- **With cache:** 2-5 minutes  
- **Clean build:** 20-30 minutes

## Success Indicators

✓ Build completes without errors
✓ Container shows as "Up" in `docker ps`
✓ Health check passes
✓ Web interface accessible at http://localhost:50080
✓ No error loops in logs

## Still Having Issues?

The robust Dockerfile handles:
- ✓ Fortran compiler for scipy
- ✓ PDF processing libraries
- ✓ OCR dependencies
- ✓ Image processing tools
- ✓ Playwright browsers
- ✓ All Python dependencies with error handling
- ✓ Proper permissions
- ✓ Health checks

If you encounter specific errors not covered here, share the exact error message for targeted help.
