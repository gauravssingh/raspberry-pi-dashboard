# Git Setup Guide for GitHub

Complete guide to upload your Raspberry Pi Dashboard to GitHub.

---

## 📋 Pre-Upload Checklist

### ✅ Security Scan Complete
- [x] No credentials in code
- [x] .gitignore configured properly
- [x] Sensitive files excluded (logs, .env, venv)
- [x] README updated with security warnings
- [x] Hardcoded paths removed

### ✅ Repository Preparation
- [x] LICENSE file added (MIT)
- [x] README.md updated for public audience
- [x] GitHub templates created
- [x] Documentation complete

---

## 🚀 Step 1: Configure Git (One-Time Setup)

If you haven't configured git globally yet:

```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name
git config --global init.defaultBranch main

# Optional: Set preferred editor
git config --global core.editor "nano"
```

---

## 📦 Step 2: Create Initial Commit

```bash
cd /home/gauravs/dashboard

# Stage all files
git add .

# Create initial commit
git commit -m "Initial commit: Raspberry Pi Dashboard with GPIO control

Features:
- Real-time system monitoring
- GPIO control with web interface
- Service management (Raspotify, Shairport-Sync)
- Weather and world clocks
- Visual wiring guides for GPIO
- REST API for automation
- Mobile-responsive UI
"
```

---

## 🌐 Step 3: Create GitHub Repository

### Option A: Via GitHub Website (Easier)

1. Go to https://github.com/new
2. **Repository name**: `raspberry-pi-dashboard` (or your preferred name)
3. **Description**: "Modern web dashboard for Raspberry Pi with GPIO control"
4. **Visibility**: 
   - ✅ **Public** (recommended for sharing)
   - Private (if you prefer)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

### Option B: Via GitHub CLI (if installed)

```bash
gh repo create raspberry-pi-dashboard --public --source=. --remote=origin
```

---

## 🔗 Step 4: Connect Local Repo to GitHub

After creating the GitHub repository, you'll see a page with commands. Use these:

```bash
cd /home/gauravs/dashboard

# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/raspberry-pi-dashboard.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Replace `YOUR_USERNAME`** with your actual GitHub username!

---

## 📝 Step 5: Verify Upload

Visit your repository:
```
https://github.com/YOUR_USERNAME/raspberry-pi-dashboard
```

You should see:
- ✅ All files uploaded
- ✅ README displayed
- ✅ LICENSE badge
- ✅ Documentation in docs/ folder

---

## 🎯 Daily Git Workflow (After Initial Setup)

### Making Changes

```bash
# Check status
git status

# Add specific files
git add app/routes/gpio.py
git add configs/gpio_config.json

# Or add all changes
git add .

# Commit with descriptive message
git commit -m "Add support for PWM control on GPIO pins"

# Push to GitHub
git push
```

### Commit Message Best Practices

**Good commit messages:**
```
Add GPIO PWM support for LED dimming
Fix memory leak in system stats endpoint
Update wiring guide with relay safety warnings
Improve mobile responsiveness of GPIO page
```

**Bad commit messages:**
```
update
fix bug
changes
stuff
```

### Commit Message Format (Recommended)

```
<type>: <short description>

<longer description if needed>

<footer with references if applicable>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```bash
git commit -m "feat: Add support for 5V relay modules"
git commit -m "fix: Resolve GPIO permission issues on Pi 3B"
git commit -m "docs: Update wiring guide with breadboard diagrams"
```

---

## 🌿 Branching Strategy (Simple for Hobby Projects)

### Main Branch
- `main` - stable, working code
- Always deployable

### Feature Branches
```bash
# Create feature branch
git checkout -b feature/add-camera-support

# Work on your feature
... make changes ...

# Commit changes
git add .
git commit -m "feat: Add camera stream support"

# Push feature branch
git push -u origin feature/add-camera-support

# Create Pull Request on GitHub
# Merge when ready
```

### Quick Fixes
```bash
# Create hotfix branch
git checkout -b hotfix/gpio-bug

# Fix the issue
git add .
git commit -m "fix: Resolve GPIO initialization error"

# Push and merge
git push -u origin hotfix/gpio-bug
```

---

## 🏷️ Tagging Releases

When you have a stable version:

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release v1.0.0: Initial public release

Features:
- GPIO control
- System monitoring
- Service management
"

# Push tags to GitHub
git push --tags
```

---

## 🔄 Keeping Your Fork Updated

If others contribute:

```bash
# Add upstream (original repo)
git remote add upstream https://github.com/ORIGINAL/raspberry-pi-dashboard.git

# Fetch updates
git fetch upstream

# Merge updates
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

---

## 📊 Useful Git Commands

### Check Status
```bash
git status          # See what's changed
git log --oneline   # View commit history
git diff            # See changes before staging
```

### Undo Changes
```bash
git restore <file>           # Discard changes to a file
git reset HEAD~1             # Undo last commit (keep changes)
git reset --hard HEAD~1      # Undo last commit (discard changes)
```

### View History
```bash
git log --oneline --graph    # Visual commit history
git log --since="2 days ago" # Recent commits
git blame <file>             # See who changed what
```

---

## 🛡️ .gitignore Best Practices

**Already configured** - the .gitignore excludes:
- Virtual environments (venv/)
- Log files (logs/, *.log)
- Secrets (.env, *.pem, *.key)
- Cache files (__pycache__/)
- IDE files (.vscode/, .idea/)
- Temporary files (*.tmp, *.bak)

**Never commit:**
- Passwords or API keys
- SSL certificates
- Database files with user data
- Large binary files
- Personal configuration files

---

## 🔐 GitHub Security Settings

After uploading:

1. **Enable Dependabot** (GitHub Settings → Security)
   - Auto-updates for dependency vulnerabilities
   
2. **Add Topics** (top right of repo page)
   - raspberry-pi, flask, gpio, home-automation, iot

3. **Add Description**
   - "Modern web dashboard for Raspberry Pi with GPIO control"

4. **Add Website** (if deployed publicly)
   - Your dashboard URL

---

## 📱 GitHub Best Practices for Hobby Projects

### Repository Settings

- ✅ Add description and topics
- ✅ Enable Issues for bug reports
- ✅ Enable Discussions for Q&A
- ✅ Add README with screenshots
- ✅ Include LICENSE (MIT is good for hobby projects)

### Maintenance

- Respond to issues when you can
- Merge good pull requests
- Tag releases when stable
- Update documentation

### Optional

- Add GitHub Actions for CI/CD
- Create wiki for extended docs
- Add project board for planning
- Create releases with changelogs

---

## 🎯 Quick Reference

```bash
# Daily workflow
git status
git add .
git commit -m "your message"
git push

# Start new feature
git checkout -b feature/feature-name

# Merge feature
git checkout main
git merge feature/feature-name
git push

# Create release
git tag -a v1.0.0 -m "Release message"
git push --tags
```

---

## ✅ Post-Upload Checklist

After uploading to GitHub:

- [ ] Repository is public/accessible
- [ ] README displays correctly
- [ ] Documentation links work
- [ ] No sensitive data visible
- [ ] Issues and Discussions enabled
- [ ] Topics and description added
- [ ] LICENSE is visible
- [ ] Clone and test from GitHub

---

**Your project is ready for GitHub!** 🎉

Next: Follow Step 3 to create your GitHub repository and Step 4 to push your code.

