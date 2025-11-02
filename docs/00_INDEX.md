# Documentation Index

Welcome to the Raspberry Pi Dashboard documentation! This index will help you find exactly what you need.

---

## 📂 Complete Documentation Structure

```
dashboard/
├── README.md                          # Main project README
├── docs/                              # All documentation
│   ├── 00_INDEX.md                   # This file - documentation navigation
│   ├── README.md                     # Full technical documentation
│   ├── GETTING_STARTED.md            # Complete setup guide (quick + detailed)
│   ├── API.md                        # Complete API reference with performance details
│   ├── DEPLOYMENT.md                 # Production deployment (nginx + systemd)
│   ├── ADDING_SERVICES.md            # Adding new services guide
│   ├── GPIO.md                       # GPIO control setup and usage guide
│   ├── GPIO_WIRING_GUIDE.md          # Breadboard wiring diagrams and LED setup
│   ├── GPIO_PIN_REFERENCE.md         # GPIO pin reference and hardware details
│   ├── GPIO_IMPLEMENTATION.md        # GPIO technical implementation details
│   ├── SYSTEM_CONFIGURATION.md       # System config and IP detection
│   ├── STRUCTURE.md                  # Project structure reference
│   ├── PROJECT_HISTORY.md            # Migration guide and project evolution
│   ├── GIT_SETUP_GUIDE.md           # Git workflow and best practices
│   ├── SECURITY_AUDIT.md            # Security scan report
│   └── GITHUB_UPLOAD_COMMANDS.md    # GitHub upload guide
└── scripts/                           # Utility scripts
    └── test_new_endpoints.sh         # API testing script
```

---

## 🚀 Quick Start - Where Do I Begin?

### I'm brand new to this project
→ Start with **[GETTING_STARTED.md](GETTING_STARTED.md)**
- 1-minute quick start section
- 5-minute detailed setup guide
- Troubleshooting common issues

### I want to deploy to production
→ Read **[DEPLOYMENT.md](DEPLOYMENT.md)**
- Nginx configuration
- Systemd service setup
- Security recommendations
- Monitoring and maintenance

### I want to use the API
→ Check **[API.md](API.md)**
- Fast endpoints for real-time data
- Cached endpoints for expensive operations
- Performance optimization details
- Complete API reference with examples

### I want to add a new service
→ Follow **[ADDING_SERVICES.md](ADDING_SERVICES.md)**
- Step-by-step integration guide
- Template code provided
- Examples: Home Assistant, Camera, MQTT

### I want to control GPIO pins
→ Read **[GPIO.md](GPIO.md)**
- Complete GPIO setup guide
- Hardware connection instructions
- REST API examples
- Troubleshooting guide
- See also: [GPIO_PIN_REFERENCE.md](GPIO_PIN_REFERENCE.md) for pin details

### I want to understand the project structure
→ Review **[STRUCTURE.md](STRUCTURE.md)**
- Complete directory tree
- File descriptions
- Architecture patterns
- Import conventions

### I'm migrating from the old version
→ See **[PROJECT_HISTORY.md](PROJECT_HISTORY.md)**
- What changed from old structure
- Breaking changes
- Migration steps
- Implementation summary

### I want comprehensive technical details
→ Read **[README.md](README.md)**
- Full feature list
- API endpoints summary
- Configuration options
- Technical documentation

### I want to upload to GitHub
→ Read **[GITHUB_UPLOAD_COMMANDS.md](GITHUB_UPLOAD_COMMANDS.md)**
- Security audit complete
- Step-by-step upload guide
- Git best practices
- Repository setup

---

## 📚 Documentation by Category

### Getting Started (New Users)

**[GETTING_STARTED.md](GETTING_STARTED.md)** - Complete setup guide
- ⚡ Quick start (1 minute)
- 📖 Detailed setup (5 minutes)
- 🔧 Configuration options
- 🆘 Troubleshooting
- ✅ Getting started checklist

**Use when:** You're setting up the dashboard for the first time

---

### API Documentation (Developers)

**[API.md](API.md)** - Complete API reference
- 🚀 Quick reference table
- 📊 Performance metrics and improvements
- ⚡ Fast endpoints (~10ms)
- 🐌 Cached endpoints (with TTL)
- 💻 Usage examples (JavaScript, Python, cURL)
- ✅ Best practices
- 🧪 Testing guide

**Use when:** You're integrating with the API or building custom clients

---

### Deployment & Production (DevOps)

**[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment
- 📋 Prerequisites and installation steps
- 🔧 Systemd service configuration
- 🌐 Nginx reverse proxy setup
- 📊 Monitoring and logging
- 🛠️ Maintenance procedures
- 🆘 Troubleshooting guide
- 🔒 Security recommendations
- ⚡ Performance tuning
- 💾 Backup strategies

**Use when:** You're deploying for 24/7 production use

---

### Development & Extension (Contributors)

**[ADDING_SERVICES.md](ADDING_SERVICES.md)** - Service integration guide
- Step-by-step guide for adding services
- Module creation templates
- Route handler setup
- Frontend integration
- Examples: Home Assistant, Camera, MQTT
- Best practices and patterns

**Use when:** You're extending the dashboard with new IoT devices

**[GPIO.md](GPIO.md)** - GPIO control guide
- Complete setup and configuration
- Hardware connection instructions
- REST API usage examples
- Troubleshooting common issues
- Safety guidelines

**[GPIO_WIRING_GUIDE.md](GPIO_WIRING_GUIDE.md)** - Breadboard wiring guide
- Step-by-step LED wiring instructions
- Breadboard layout diagrams
- Component requirements
- Testing procedures
- Safety checklist

**[GPIO_PIN_REFERENCE.md](GPIO_PIN_REFERENCE.md)** - GPIO pin reference
- Complete pin layout for Raspberry Pi 3B
- Safe vs unsafe pins
- Physical pin mapping
- BCM numbering reference
- Electrical specifications

**[GPIO_IMPLEMENTATION.md](GPIO_IMPLEMENTATION.md)** - GPIO technical details
- Architecture overview
- Implementation details
- Code structure
- Future enhancements

**Use when:** You're working with GPIO pins or hardware control

**[STRUCTURE.md](STRUCTURE.md)** - Project organization
- Complete directory tree
- File-by-file descriptions
- Architecture patterns
- Import conventions
- Naming conventions

**Use when:** You're navigating the codebase or contributing

---

### Migration & History (Reference)

**[PROJECT_HISTORY.md](PROJECT_HISTORY.md)** - Project evolution
- Migration from old structure
- What changed and why
- Breaking changes list
- Implementation summary
- Plan vs. implementation comparison

**Use when:** You're understanding the project's evolution or migrating

**[README.md](README.md)** - Technical documentation
- Project overview
- Feature list
- Installation instructions
- API endpoint summary
- Configuration guide
- Quick start commands

**Use when:** You want a comprehensive technical overview

---

## 🎯 Common Tasks

| I want to... | Go to... |
|--------------|----------|
| **Set up the dashboard** | [GETTING_STARTED.md](GETTING_STARTED.md) |
| **Deploy to production** | [DEPLOYMENT.md](DEPLOYMENT.md) |
| **Use the API** | [API.md](API.md) |
| **Control GPIO pins** | [GPIO.md](GPIO.md) |
| **Add a new service** | [ADDING_SERVICES.md](ADDING_SERVICES.md) |
| **Understand the code** | [STRUCTURE.md](STRUCTURE.md) |
| **Migrate from old version** | [PROJECT_HISTORY.md](PROJECT_HISTORY.md) |
| **Fix an issue** | [GETTING_STARTED.md](GETTING_STARTED.md#troubleshooting) or [DEPLOYMENT.md](DEPLOYMENT.md#troubleshooting) |
| **Configure settings** | [GETTING_STARTED.md](GETTING_STARTED.md#configuration) |
| **Monitor the system** | [DEPLOYMENT.md](DEPLOYMENT.md#monitoring-and-logs) |
| **Secure the dashboard** | [DEPLOYMENT.md](DEPLOYMENT.md#security-recommendations) |

---

## 🔍 Quick Command Reference

### Development
```bash
# Start development server
python run.py

# Test API
curl http://localhost:5050/api/system/health
```

### Production
```bash
# Start/stop service
sudo systemctl start dashboard
sudo systemctl stop dashboard
sudo systemctl restart dashboard

# View logs
sudo journalctl -u dashboard -f

# Check status
sudo systemctl status dashboard
```

### Testing
```bash
# Test all endpoints
./scripts/test_new_endpoints.sh

# Test specific endpoint
curl http://localhost:5050/api/system/stats | jq
```

---

## 📊 Documentation Stats

- **Total Documentation Files:** 17 files (including GitHub guides)
- **API Documentation:** Complete reference with performance details
- **Getting Started Guide:** Quick + detailed setup in one file
- **GPIO Documentation:** Complete hardware control guide with pin reference and visual wiring
- **GitHub Guides:** Git setup, security audit, upload commands
- **Deployment Guide:** Includes nginx + systemd configuration
- **Code Examples:** JavaScript, Python, cURL
- **Lines of Documentation:** 5000+ lines

---

## 🔄 Recently Consolidated

### October 29, 2025 - Documentation Streamlining

The documentation has been consolidated from 17 files to 8 files for better organization:

**Merged Files:**
- `GETTING_STARTED.md` + `QUICK_START.md` → **GETTING_STARTED.md**
- `API_ENDPOINTS.md` + `QUICK_API_REFERENCE.md` + `NEW_ENDPOINTS_SUMMARY.md` + `PERFORMANCE_IMPROVEMENTS.md` → **API.md**
- `DEPLOYMENT.md` + `SYSTEMD_SERVICE.md` → **DEPLOYMENT.md**
- `00_INDEX.md` + `DOCUMENTATION_STRUCTURE.md` → **00_INDEX.md** (this file)
- `MIGRATION.md` + `OLD_FILES_INFO.md` + `PLAN_IMPLEMENTATION.md` + `PROJECT_SUMMARY.md` → **PROJECT_HISTORY.md**

### GPIO Documentation Added

GPIO documentation has been organized under `docs/`:
- `GPIO_SETUP.md` + `GPIO_QUICK_START.md` → **GPIO.md** (consolidated guide)
- `GPIO_PIN_REFERENCE.md` → **GPIO_PIN_REFERENCE.md** (hardware reference)
- `GPIO_IMPLEMENTATION_SUMMARY.md` → **GPIO_IMPLEMENTATION.md** (technical details)

**Benefits:**
- ✅ 58% fewer files to navigate
- ✅ Less duplication
- ✅ Easier to maintain
- ✅ Clearer organization
- ✅ All important information preserved
- ✅ GPIO docs properly organized in docs/ directory

---

## 📝 Documentation Guidelines

When adding new documentation:

1. **Choose the right file:**
   - Getting started info → `GETTING_STARTED.md`
   - API details → `API.md`
   - Deployment instructions → `DEPLOYMENT.md`
   - Service integration → `ADDING_SERVICES.md`

2. **Update this index** if adding major sections

3. **Use clear headings** and consistent formatting

4. **Include examples** where appropriate

5. **Cross-reference** related documentation

6. **Test all code examples** before adding them

---

## 🛠️ Utility Scripts

### Testing
```bash
# Test all API endpoints
./scripts/test_new_endpoints.sh
```

Located in: `scripts/test_new_endpoints.sh`

---

## 📖 Reading Order for New Users

If you're completely new, we recommend this reading order:

1. **[GETTING_STARTED.md](GETTING_STARTED.md)** - Get it running (10 minutes)
2. **[API.md](API.md)** - Understand the endpoints (15 minutes)
3. **[GPIO.md](GPIO.md)** - Control GPIO pins (10 minutes) - *if using GPIO*
4. **[STRUCTURE.md](STRUCTURE.md)** - Navigate the code (10 minutes)
5. **[ADDING_SERVICES.md](ADDING_SERVICES.md)** - Extend it (when needed)
6. **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deploy it (when ready)

**Total time to full understanding:** ~45-55 minutes

---

## 🔗 External Links

- **Flask Documentation:** https://flask.palletsprojects.com/
- **Gunicorn Documentation:** https://docs.gunicorn.org/
- **Nginx Documentation:** https://nginx.org/en/docs/
- **Raspotify:** https://github.com/dtcooper/raspotify
- **Shairport Sync:** https://github.com/mikebrady/shairport-sync

---

## 💡 Tips for Using This Documentation

1. **Use the search function** (Ctrl+F / Cmd+F) to find specific topics
2. **Follow the links** - all documentation is cross-referenced
3. **Check the troubleshooting sections** if something doesn't work
4. **Code examples are tested** - copy and run them directly
5. **Update paths** in examples to match your username/setup

---

## 🆘 Still Can't Find What You Need?

1. **Check the README.md** in the project root
2. **Look at the code examples** in `app/modules/` and `app/routes/`
3. **Review the troubleshooting sections** in GETTING_STARTED.md and DEPLOYMENT.md
4. **Test the API** with the provided test script
5. **Check the logs** for error messages

---

## ✨ What Makes This Dashboard Special

- **Fast API** - Main stats endpoint responds in ~10ms (950x faster than before!)
- **Smart Caching** - Expensive operations are cached with appropriate TTLs
- **Mobile-Friendly** - Fully responsive glassmorphism UI
- **Extensible** - Easy to add new services and integrations
- **Production-Ready** - Includes nginx, systemd, and monitoring setup
- **Well-Documented** - Comprehensive guides for every aspect
- **Resource-Efficient** - Optimized for Raspberry Pi 3B (1GB RAM)

---

**Happy monitoring! 🚀**

---

*Last updated: October 29, 2025*
*Documentation consolidated and streamlined for better organization*
