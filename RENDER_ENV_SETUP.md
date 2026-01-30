# Setting Up Environment Variables on Render.com

## For the Web Application (app.py)

The web application **does NOT require** environment variables because users enter their Jira credentials directly through the web interface. However, you can optionally set:

### Optional Environment Variables:

1. **SECRET_KEY** (Recommended for production)
   - Used for Flask session security
   - Generate a secure random string

## For Command-Line Scripts (pdf_to_jira_tasks.py)

If you want to run the command-line script on Render, you'll need to set these environment variables:

### Required Environment Variables:

1. **JIRA_URL** - Your Jira instance URL
   - Example: `https://your-domain.atlassian.net`

2. **JIRA_EMAIL** - Your Jira account email
   - Example: `your-email@example.com`

3. **JIRA_TOKEN** - Your Jira API token
   - Generate at: https://id.atlassian.com/manage-profile/security/api-tokens

4. **JIRA_PROJECT_KEY** - Your Jira project key
   - Example: `PROJ` or `INT`

## How to Set Environment Variables on Render.com

### Step-by-Step Instructions:

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com/
   - Select your web service

2. **Navigate to Environment Tab**
   - Click on your service name
   - Click **"Environment"** in the left sidebar

3. **Add Environment Variables**
   - Click **"Add Environment Variable"** button
   - Enter the key-value pairs:

   ```
   Key: SECRET_KEY
   Value: your-random-secret-key-here
   ```

   ```
   Key: JIRA_URL
   Value: https://your-domain.atlassian.net
   ```

   ```
   Key: JIRA_EMAIL
   Value: your-email@example.com
   ```

   ```
   Key: JIRA_TOKEN
   Value: your-jira-api-token-here
   ```

   ```
   Key: JIRA_PROJECT_KEY
   Value: PROJ
   ```

4. **Save Changes**
   - Click **"Save Changes"** button
   - Render will automatically redeploy your service with the new variables

### Alternative: Using .env File Locally (NOT for Render)

For local development only, create a `.env` file:

```bash
# .env (DO NOT COMMIT THIS FILE)
SECRET_KEY=your-random-secret-key
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_TOKEN=your-jira-api-token
JIRA_PROJECT_KEY=PROJ
```

**Note:** The `.env` file is already in `.gitignore` and will NOT be uploaded to Git.

## Security Best Practices

✅ **DO:**
- Use environment variables for sensitive data
- Generate strong, random SECRET_KEY values
- Revoke and regenerate API tokens if exposed
- Use HTTPS (Render provides this automatically)

❌ **DON'T:**
- Commit credentials to Git
- Share API tokens in code or documentation
- Use the same token across multiple environments

## Generating a Secure SECRET_KEY

Run this Python command to generate a secure random key:

```python
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use it as your SECRET_KEY value.

## For the Web Application Users

**Important:** The web application (app.py) is designed so that:
- Users enter their own Jira credentials through the web form
- Credentials are NOT stored on the server
- Each user uses their own API token
- No environment variables needed for basic operation

This means you can deploy the web app without setting any Jira-related environment variables, and users will provide their credentials when they use the application.

## Verifying Environment Variables

After setting environment variables on Render:

1. Check the **Logs** tab in Render dashboard
2. Look for any startup errors
3. The app should start successfully
4. Test the application to ensure it works

## Troubleshooting

**Problem:** Environment variables not working
- **Solution:** Make sure you clicked "Save Changes" and the service redeployed

**Problem:** App still shows old values
- **Solution:** Trigger a manual redeploy from the Render dashboard

**Problem:** Can't find Environment tab
- **Solution:** Make sure you're viewing the specific web service, not the dashboard home

---

Need help? Check the Render documentation: https://render.com/docs/environment-variables