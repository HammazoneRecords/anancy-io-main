# 🚀 Quick Start - AnancyIO

## Option A: Run with Conda (No Docker)

**Requires Conda (Miniconda or Anaconda).**

- **Windows:** `.\run-web.ps1`
- **macOS / Linux:** `chmod +x run-web.sh && ./run-web.sh`

Then open **http://localhost:5000** in your browser. See **[RUN_WITHOUT_DOCKER.md](RUN_WITHOUT_DOCKER.md)** for manual setup and configuration.

---

## Option B: Run with Docker

### Step 1: Validate Your System
```powershell
.\check-docker.ps1
```

### Step 2: Build and Start
```powershell
.\build.ps1 -Start
```

### Step 3: Access the App
Open your browser: **http://localhost:50080**

---

## Docker Command Reference

### Using the Helper Script (`build.ps1`)

```powershell
# Check system readiness
.\build.ps1 -Check

# Start AnancyIO (builds automatically)
.\build.ps1 -Start

# View logs
.\build.ps1 -Logs

# Stop container
.\build.ps1 -Stop

# Clean everything and rebuild
.\build.ps1 -Clean -Start

# Get help
.\build.ps1 -Help
```

### Direct Docker Commands

```powershell
# Build and start
docker-compose -f docker-compose.robust.yml up -d --build

# View logs
docker-compose -f docker-compose.robust.yml logs -f

# Stop
docker-compose -f docker-compose.robust.yml down

# Restart
docker-compose -f docker-compose.robust.yml restart

# Check status
docker ps
```

---

## What to Expect

### Build Time
- **First build:** 15-25 minutes ⏱️
- **Subsequent builds:** 2-5 minutes (uses cache)

### During Build You'll See:
1. ✓ Installing system packages (2-3 min)
2. ✓ Installing Python packages (10-15 min)
3. ✓ Installing Playwright browsers (2-3 min)
4. ✓ Copying application files (1 min)

### Success Indicators:
- ✅ Build completes without red errors
- ✅ Container shows as "Up" in Docker Desktop
- ✅ http://localhost:50080 loads successfully
- ✅ No error loops in logs

---

## Troubleshooting

### Build Failed?
```powershell
# Check the troubleshooting guide
Get-Content DOCKER_TROUBLESHOOTING.md

# Try clean build
.\build.ps1 -Clean -Start
```

### Can't Access http://localhost:50080?
```powershell
# Check if container is running
docker ps

# Check logs for errors
.\build.ps1 -Logs

# Wait 60 seconds after start (initialization time)
Start-Sleep -Seconds 60
```

### Port Already in Use?
```powershell
# Check what's using port 50080
netstat -ano | findstr :50080

# Option 1: Kill that process
taskkill /PID <pid> /F

# Option 2: Change port
# Edit docker-compose.robust.yml
# Change "50080:80" to "50081:80"
```

### Out of Memory?
1. Open Docker Desktop
2. Settings → Resources → Memory
3. Increase to 6GB or higher
4. Apply & Restart
5. Try build again

### Still Having Issues?
See **DOCKER_TROUBLESHOOTING.md** for comprehensive solutions.

---

## What Got Installed?

The robust Docker setup includes:

### System Dependencies
- ✅ Python 3.11
- ✅ Build tools (gcc, g++, gfortran)
- ✅ PDF processing (poppler, mupdf)
- ✅ OCR (tesseract)
- ✅ Image processing libraries
- ✅ Math libraries (BLAS, LAPACK)

### Python Packages
- ✅ Flask web framework
- ✅ AI/ML libraries (transformers, torch)
- ✅ Document processing (pypdf, pymupdf)
- ✅ Browser automation (playwright)
- ✅ All requirements from requirements.txt

### Configuration
- ✅ Persistent volumes for data
- ✅ Health checks
- ✅ Resource limits
- ✅ Proper logging

---

## Daily Usage

### Start your work session:
```powershell
.\build.ps1 -Start
# Wait 30 seconds
# Open http://localhost:50080
```

### End your work session:
```powershell
.\build.ps1 -Stop
```

### Update code and restart:
```powershell
# Pull latest changes
git pull

# Rebuild and restart
.\build.ps1 -Clean -Start
```

---

## Files Created for You

- ✅ **Dockerfile.robust** - Production-ready Dockerfile
- ✅ **docker-compose.robust.yml** - Complete Docker Compose config  
- ✅ **build.ps1** - Helper script for all operations
- ✅ **check-docker.ps1** - Pre-build validation
- ✅ **DOCKER_TROUBLESHOOTING.md** - Comprehensive troubleshooting

---

## Next Steps After First Start

1. **Configure API Keys** (if needed)
   - Create `.env` file
   - Add your OpenAI/Anthropic API keys

2. **Explore the Interface**
   - Navigate to http://localhost:50080
   - Check the dashboard
   - Try example prompts

3. **Check Logs** (optional)
   ```powershell
   .\build.ps1 -Logs
   ```

---

## Need Help?

- 📖 See **DOCKER_TROUBLESHOOTING.md**
- 📖 See **DEPLOYMENT.md** for advanced deployment
- 🐛 Check logs: `.\build.ps1 -Logs`
- 💬 Ask in project Discord/GitHub issues

---

**Ready to start?** Just run:
```powershell
.\build.ps1 -Check
.\build.ps1 -Start
```

Then open **http://localhost:50080** in your browser! 🎉
