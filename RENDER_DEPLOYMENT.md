# PDF to Jira Web Application - Render Deployment Guide

## Quick Deploy to Render

### Step 1: Prepare Your Repository
1. Make sure all files are committed to Git:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for web app"
   ```

2. Push to GitHub:
   ```bash
   git remote add origin <your-github-repo-url>
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `pdf-to-jira-app` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free` (or upgrade as needed)

5. Add Environment Variables (Optional):
   - Click **"Advanced"**
   - Add environment variable:
     - Key: `SECRET_KEY`
     - Value: (generate a random string for session security)

6. Click **"Create Web Service"**

### Step 3: Access Your Application

Once deployed, Render will provide you with a URL like:
```
https://pdf-to-jira-app.onrender.com
```

Your application will be live at this URL!

## Features

- ✅ Upload PDF files (up to 16MB)
- ✅ Configure Jira credentials
- ✅ Test connection before processing
- ✅ Preview mode (dry run)
- ✅ Automatic task creation
- ✅ Real-time progress tracking
- ✅ Responsive design

## Environment Variables

Optional environment variables for production:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask session secret key | Auto-generated |
| `PORT` | Port number | 5000 |

## Render Configuration Files

- **Procfile**: Tells Render how to start the app
- **runtime.txt**: Specifies Python version
- **requirements.txt**: Lists all dependencies

## Local Testing

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Visit http://localhost:5000
```

## Troubleshooting

### Build Fails
- Check that all dependencies are in `requirements.txt`
- Verify Python version in `runtime.txt`

### App Crashes on Startup
- Check Render logs in the dashboard
- Ensure all required files are committed

### File Upload Issues
- Free tier has memory limits
- Large PDFs might timeout (upgrade plan if needed)

## Security Notes

⚠️ **Important**: Never commit your Jira API tokens to Git!
- Users enter credentials through the web interface
- Credentials are not stored on the server
- Use HTTPS in production (Render provides this automatically)

## Support

For issues or questions:
1. Check Render logs in the dashboard
2. Review error messages in the browser console
3. Verify Jira credentials and permissions

## Next Steps

After deployment:
1. Test the application with a sample PDF
2. Verify Jira connection works
3. Create a few test tasks
4. Share the URL with your team!

---

Enjoy your PDF to Jira web application! 🎉
