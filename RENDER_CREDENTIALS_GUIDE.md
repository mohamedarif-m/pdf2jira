# How to Handle Jira Credentials on Render.com

## ✅ Good News: No Credentials Needed in Render!

The PDF to Jira web application is designed with security in mind. **You do NOT need to set Jira credentials as environment variables on Render.com.**

## How It Works

### For End Users:
1. **Users enter their own credentials** through the web interface
2. **Credentials are NOT stored** on the server
3. **Each request uses the provided credentials** temporarily
4. **Credentials are discarded** after the request completes

### Web Interface Flow:
```
User opens app → Enters credentials in form → Uploads PDF → 
App processes → Creates Jira tasks → Credentials discarded
```

## Deployment Steps on Render.com

### 1. Deploy Your Application
```bash
# Already done - your code is pushed to GitHub
git push origin main
```

### 2. Configure Render (Optional Environment Variables)
Only ONE optional environment variable is recommended:

**SECRET_KEY** (for Flask session security)
- Generate a secure key:
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
- Add it in Render Dashboard:
  - Go to your service → **Environment** tab
  - Click **"Add Environment Variable"**
  - Key: `SECRET_KEY`
  - Value: `<paste-your-generated-key>`

### 3. That's It!
Your app is ready to use. No Jira credentials needed in Render.

## How Users Will Use the Deployed App

### Step 1: Access the Web App
```
https://your-app-name.onrender.com
```

### Step 2: Enter Jira Credentials in the Form
Users will see a form with these fields:
- **Jira URL**: `https://your-domain.atlassian.net`
- **Email**: `user@example.com`
- **API Token**: `<their-personal-token>`
- **Project Key**: `PROJ`

### Step 3: Test Connection
Click "Test Connection" to verify credentials work.

### Step 4: Upload PDF
Upload the PDF file and configure task settings.

### Step 5: Create Tasks
Click "Create Tasks" - the app will use the provided credentials to create tasks in Jira.

## Security Features

✅ **Credentials are never stored**
- Sent with each request only
- Not saved in database or files
- Not logged or cached

✅ **HTTPS by default**
- Render provides SSL certificates automatically
- All data encrypted in transit

✅ **No hardcoded secrets**
- No API tokens in code
- No credentials in environment variables
- Each user uses their own token

## Generating Jira API Tokens

Users need to generate their own API tokens:

1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click **"Create API token"**
3. Give it a name (e.g., "PDF to Jira App")
4. Copy the token (it won't be shown again)
5. Use it in the web form

## For Multiple Users

Each user should:
- Use their own Jira account email
- Generate their own API token
- Have appropriate permissions in the Jira project

## Alternative: Pre-configured Credentials (Not Recommended)

If you want to pre-configure credentials for a single user/team, you CAN set environment variables on Render, but this is **NOT recommended** for security reasons:

```bash
# In Render Dashboard → Environment
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=team@example.com
JIRA_TOKEN=your-token-here
JIRA_PROJECT_KEY=PROJ
```

Then modify `app.py` to read from environment variables as defaults. However, this means:
- ❌ All users share the same credentials
- ❌ Token is exposed in Render dashboard
- ❌ Less secure
- ❌ Harder to manage multiple projects

## Best Practice: Keep Current Design

The current design (users enter credentials) is the **most secure and flexible** approach:
- ✅ Each user has their own access
- ✅ No shared credentials
- ✅ Easy to revoke individual access
- ✅ Audit trail per user
- ✅ No secrets in deployment

## Troubleshooting

### "Authentication Failed" Error
- User should verify their email and API token
- Check if token is still valid
- Regenerate token if needed

### "Project Not Found" Error
- Verify project key is correct
- Check user has access to the project
- Ensure project exists in Jira

### Connection Timeout
- Check Jira URL is correct
- Verify network connectivity
- Try again (Render free tier may have cold starts)

## Summary

**For Render.com deployment:**
1. ✅ Push code to GitHub (already done)
2. ✅ Deploy on Render (no Jira credentials needed)
3. ✅ Optionally set SECRET_KEY for session security
4. ✅ Share the app URL with users
5. ✅ Users enter their own credentials when using the app

**No Jira credentials needed in Render environment variables!**

---

Need help? Check:
- [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Full deployment guide
- [WEB_APP_README.md](WEB_APP_README.md) - Application documentation
- [RENDER_ENV_SETUP.md](RENDER_ENV_SETUP.md) - Environment variables reference