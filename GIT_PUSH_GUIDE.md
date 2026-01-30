# Step-by-Step Guide: Push Code to GitHub and Deploy to Render

## Prerequisites
- Git installed on your computer
- GitHub account created
- Changes made to your code (already done!)

## Step 1: Check Current Git Status

```bash
cd /Users/arif/Downloads/pdf2jira
git status
```

This shows which files have been modified.

## Step 2: Initialize Git Repository (if not already done)

```bash
# Only run this if you haven't initialized git yet
git init
```

## Step 3: Add All Changes to Git

```bash
# Add all modified and new files
git add .

# Or add specific files:
git add runtime.txt Procfile pdf_to_jira_tasks.py RENDER_ENV_SETUP.md static/.gitkeep templates/.gitkeep
```

## Step 4: Commit Your Changes

```bash
git commit -m "Fix Render deployment: update Python version, add port binding, remove credentials"
```

## Step 5: Create GitHub Repository

### Option A: Using GitHub Website
1. Go to https://github.com/new
2. Repository name: `pdf2jira` (or your preferred name)
3. Description: "PDF to Jira Task Converter Web Application"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README (you already have files)
6. Click **"Create repository"**

### Option B: Using GitHub CLI (if installed)
```bash
gh repo create pdf2jira --public --source=. --remote=origin
```

## Step 6: Connect Local Repository to GitHub

After creating the GitHub repository, you'll see instructions. Use these commands:

```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/pdf2jira.git

# Verify the remote was added
git remote -v
```

## Step 7: Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main
```

If prompted for credentials:
- **Username:** Your GitHub username
- **Password:** Use a Personal Access Token (not your GitHub password)

### Creating a Personal Access Token (if needed):
1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Name: "Render Deployment"
4. Select scopes: `repo` (full control)
5. Click **"Generate token"**
6. **Copy the token** (you won't see it again!)
7. Use this token as your password when pushing

## Step 8: Verify Push Was Successful

```bash
# Check if push succeeded
git log --oneline -5

# Or visit your GitHub repository in browser
# https://github.com/YOUR_USERNAME/pdf2jira
```

## Step 9: Deploy to Render.com

### 9.1: Go to Render Dashboard
1. Visit https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**

### 9.2: Connect GitHub Repository
1. Click **"Connect account"** if not connected
2. Authorize Render to access your GitHub
3. Select your repository: `pdf2jira`
4. Click **"Connect"**

### 9.3: Configure Web Service
Fill in these settings:

- **Name:** `pdf2jira-app` (or your preferred name)
- **Region:** Choose closest to you
- **Branch:** `main`
- **Root Directory:** (leave blank)
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
- **Instance Type:** `Free`

### 9.4: Add Environment Variables (Optional)
Click **"Advanced"** → **"Add Environment Variable"**

```
Key: SECRET_KEY
Value: (generate with: python -c "import secrets; print(secrets.token_hex(32))")
```

### 9.5: Create Web Service
1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Watch the logs for any errors

### 9.6: Access Your Application
Once deployed, Render provides a URL like:
```
https://pdf2jira-app.onrender.com
```

## Troubleshooting

### Problem: "Permission denied (publickey)"
**Solution:** Use HTTPS instead of SSH, or set up SSH keys:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/pdf2jira.git
```

### Problem: "Authentication failed"
**Solution:** Use a Personal Access Token instead of password

### Problem: "Updates were rejected"
**Solution:** Pull first, then push:
```bash
git pull origin main --rebase
git push origin main
```

### Problem: Render build fails
**Solution:** Check these files exist and are correct:
- `requirements.txt`
- `Procfile`
- `runtime.txt`
- `app.py`

## Quick Reference Commands

```bash
# Check status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main

# View commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

## Complete Workflow Example

```bash
# 1. Navigate to project
cd /Users/arif/Downloads/pdf2jira

# 2. Check what changed
git status

# 3. Add all changes
git add .

# 4. Commit with message
git commit -m "Fix Render deployment configuration"

# 5. Push to GitHub (first time)
git remote add origin https://github.com/YOUR_USERNAME/pdf2jira.git
git branch -M main
git push -u origin main

# 6. For subsequent pushes
git add .
git commit -m "Your changes"
git push
```

## Next Steps After Deployment

1. ✅ Test your application at the Render URL
2. ✅ Upload a sample PDF
3. ✅ Test Jira connection
4. ✅ Create test tasks
5. ✅ Share the URL with your team!

## Important Security Reminder

⚠️ **Before pushing to GitHub:**
- Verify no credentials are in the code
- Check `.gitignore` is working
- Never commit API tokens or passwords

✅ **Your code is now safe** - credentials were removed!

---

Need help? 
- GitHub Docs: https://docs.github.com/
- Render Docs: https://render.com/docs/
- Git Basics: https://git-scm.com/book/en/v2/Getting-Started-Git-Basics